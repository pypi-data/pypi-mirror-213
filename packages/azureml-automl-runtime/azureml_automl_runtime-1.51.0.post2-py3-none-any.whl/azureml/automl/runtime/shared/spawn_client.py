# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Functionality to execute a function in a child process created using "spawn".

This file contains the client portion.
"""
import logging
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, cast
from azureml._common.exceptions import AzureMLException

import dill
from azureml._common._error_definition import AzureMLError

from azureml.automl.core._logging import log_server
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    AutoMLInternal,
    InsufficientMemory,
    InsufficientMemoryLikely,
)
from azureml.automl.core.shared.exceptions import (
    AutoMLException,
    ClientException,
    PipelineRunException,
    ResourceException,
)
from azureml.automl.core.shared.fake_traceback import FakeTraceback
from azureml.automl.core.shared.limit_function_call_exceptions import CpuTimeoutException, SubprocessException

from . import subprocess_utilities
from .types import T

logger = logging.getLogger(__name__)


def touch_file(base_path: str, filename: str) -> str:
    """
    Given the base path and the file name, touch the file.

    :param base_path: directory containing the file
    :param filename: the name of the file
    :return: the path to the file
    """
    path = Path(base_path).joinpath(filename)
    path.touch()
    return os.path.abspath(os.path.join(base_path, filename))


def serialize(
    working_dir: str,
    function: "Callable[..., Tuple[T, Optional[BaseException]]]",
    arg: Any,
    kwarg: Any,
) -> Dict[str, Any]:
    """
    Creates the command and tempfiles needed to pass into the subprocess.

    :param working_dir: The directory where tempfiles will be made
    :param function: The function to run in the subprocess
    :param arg: The arguments of the function 'function'
    :param kwarg: The kwargs of the function 'function'
    :return: The files and arguments to pass into subprocess.Popen
    """
    # Create all files used for data exchange across client and server.
    config_file_name = touch_file(working_dir, tempfile.NamedTemporaryFile(dir=working_dir).name)
    input_file_name = touch_file(working_dir, tempfile.NamedTemporaryFile(dir=working_dir).name)
    output_file_name = touch_file(working_dir, tempfile.NamedTemporaryFile(dir=working_dir).name)
    error_file_name = touch_file(working_dir, tempfile.NamedTemporaryFile(dir=working_dir).name)
    # Create a configuration object to pass to the target process. This
    # configuration is applied prior to deserialization of the input,
    # thus it can influence the environment code gets loaded in.
    config = {
        "path": sys.path,
        "logger_names": log_server.logger_names,
        "log_verbosity": log_server.verbosity,
        "custom_dimensions": log_server.custom_dimensions,
    }

    # Use dill to store configuration information needed to set up
    # the target process.
    with open(config_file_name, "wb") as file:
        dill.dump(config, file, protocol=dill.HIGHEST_PROTOCOL)

    # Use dill to store the function and arguments to run in the target
    # process.
    with open(input_file_name, "wb") as file:
        dill.dump((function, arg, kwarg), file, protocol=dill.HIGHEST_PROTOCOL)

    # Locate the Python executable, working directory, our sibling
    # spawn_server, and the environment variables.
    python_executable = sys.executable
    curdir = os.path.dirname(__file__)
    srv_script_file = os.path.join(curdir, "spawn_server.py")
    env = os.environ.copy()

    cmd = [
        python_executable,
        srv_script_file,
        config_file_name,
        input_file_name,
        output_file_name,
        error_file_name,
    ]

    configuration = {
        'cmd': cmd,
        'cwd': working_dir,
        'env': env,
        'config_file_name': config_file_name,
        'input_file_name': input_file_name,
        'output_file_name': output_file_name,
        'error_file_name': error_file_name
    }

    return configuration


def deserialize(
    process: "subprocess.Popen[bytes]",
    files: Dict[str, Any],
    stderr_file_name: str
) -> Any:
    """
    Reads from the files to check for errors in the process and kills the process.

    :param process: A completed subprocess
    :param files: The files the subprocess used to write to
    :param stderr_file_name: The stderr file the process wrote to
    :return: the result from the (result, error) tuple returned by the function if successful
    """

    check_process_success(process, stderr_file_name, files['error_file_name'])

    # Read the output and use dill to deserialize the result.
    try:
        with open(files['error_file_name'], "rb") as error_file:
            err, tb = cast(Tuple[Optional[BaseException], Optional[Dict[str, Any]]], dill.load(error_file))
    except FileNotFoundError:
        # There are some unknown situations where the error file does not exist, even though the exit code may be
        # zero. (Maybe caused by some external process deleting the file?) Normally, we shouldn't hit this because
        # the file is created before the process even spawns. Handle this case later if the output is also missing.
        err, tb = None, None

    if err is not None:
        # We MUST log the traceback here, because it is not possible to reraise with this fake traceback
        # without additional interpreter hacks involving manually constructing similar stack frames.
        # See python-tblib source code for an example of this hackery in action.
        # However, this will result in duplicate logging of child process errors.

        # For safety reasons, run this in a try-except to avoid weird edge cases that might have been missed.
        try:
            logging_utilities.log_traceback(err, logger, tb=FakeTraceback.deserialize(tb))
        except Exception as e:
            logging_utilities.log_traceback(e, logger)

        if isinstance(err, AzureMLException):
            # If it's one of ours, throw it as is
            raise err
        # We don't have the original traceback for the exception, so wrap it in one of ours and mark as PII.
        raise ClientException.from_exception(
            err,
            "Execution failed with {}: {}".format(err.__class__.__name__, str(err)),
            "spawn_client",
            has_pii=True,
        ).with_generic_msg("Execution failed with {}".format(err.__class__.__name__))

    try:
        with open(files['output_file_name'], "rb") as output_file:
            val = dill.load(output_file)
    except FileNotFoundError:
        raise ClientException._with_error(
            AzureMLError.create(
                AutoMLInternal,
                error_details="Execution failed - error in retrieving results from training subprocess",
                target="spawn_client.multiple_run_in_proc",
            )
        )
    return val


def multiple_run_in_proc(
    working_dir: Optional[str],
    timeout: Optional[int],
    functions: List["Callable[..., Tuple[T, Optional[BaseException]]]"],
    args: List[Any],
    kwargs: List[Any],
) -> List[T]:
    """
    Invoke each function in functions with its coressponding arguments in a new process.
    Each function in functions must return a (result, error) tuple.

    :param working_dir: The directory to spawn subprocesses
    :param timeout: Optional amount of time after which the process will be killed
    :param functions: The functions to run in subprocesses
    :param args: The arguments to each function in functions. Must be the same length as 'functions'
    :param kwargs: the keyword arguments to each function in functions. Must be the same length as 'functions'
    :return: All results from the (result, error) tuple returned by the functions in functions if successful
    """
    working_dir = os.path.abspath(working_dir or ".")
    configurations = []
    for function, arg, kwarg in zip(functions, args, kwargs):
        configurations.append(serialize(working_dir=working_dir, function=function, arg=arg, kwarg=kwarg))

    stdout_file_name = touch_file(working_dir, tempfile.NamedTemporaryFile(dir=working_dir).name)
    stderr_file_name = touch_file(working_dir, tempfile.NamedTemporaryFile(dir=working_dir).name)

    processes = []
    with open(stdout_file_name, 'w') as stdout, open(stderr_file_name, 'w') as stderr:
        for config in configurations:
            processes.append(subprocess.Popen(config['cmd'], cwd=config['cwd'],
                             env=config['env'], stdout=stdout, stderr=stderr))

        for process in processes:
            try:
                process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                # Attempt to kill the process and its children, and report
                # the exception.
                subprocess_utilities.kill_process_tree(process.pid)
                raise

    files_to_close = []
    for config in configurations:
        files_to_close.append({
            'config_file_name': config['config_file_name'],
            'input_file_name': config['input_file_name'],
            'output_file_name': config['output_file_name'],
            'error_file_name': config['error_file_name']
        })

    err = None
    values = []
    for process, files in zip(processes, files_to_close):
        try:
            values.append(cast(T, deserialize(process, files, stderr_file_name)))

        # If an error occured, we still want to kill the other processes and we want to
        # clean up the temp files that were made.
        except Exception as e:
            err = e
            logging_utilities.log_traceback(e, logger)
            logger.warning(
                "deserializing failed with {}, skipping".format(e.__class__.__name__)
            )

        finally:
            if process is not None:
                for i in range(5):
                    try:
                        # poll() returns None if the process is still running (no returncode)
                        if process.poll() is None:
                            subprocess_utilities.kill_process_tree(process.pid)
                        break
                    except Exception:
                        pass

            try:
                for file in files.values():
                    os.remove(file)
            except Exception as e:
                logging_utilities.log_traceback(e, logger)
                logger.warning(
                    "os.remove failed with {} during temp file cleanup, skipping.".format(e.__class__.__name__)
                )
    try:
        os.remove(stderr_file_name)
        os.remove(stdout_file_name)
    except Exception as e:
        logging_utilities.log_traceback(e, logger)
        logger.warning(
            "os.remove failed with {} during temp file cleanup, skipping.".format(e.__class__.__name__)
        )
    # Raises the last exception encountered
    if err is not None:
        raise err
    return values


def run_in_proc(
    working_dir: Optional[str],
    timeout: Optional[int],
    f: "Callable[..., Tuple[T, Optional[BaseException]]]",
    args: Any,
    **kwargs: Any,
) -> T:
    """
    Invoke f with the given arguments in a new process. f must return a (result, error) tuple.

    :param working_dir: the working directory to use
    :param timeout: optional amount of time after which the process will be killed
    :param f: the function to run
    :param args: the positional arguments for the function
    :param kwargs: the keyword arguments for the function
    :return: the result from the (result, error) tuple returned by the function if successful
    """
    process = None

    # Create a folder for temporary files, used to communicate across
    # processes and to persist stdout/stderr.
    working_dir = os.path.abspath(working_dir or ".")
    try:
        tempdir = tempfile.mkdtemp(dir=working_dir)
    except OSError as e:
        logging_utilities.log_traceback(e, logger)
        logger.warning(
            "Creating temporary folder in path specified in settings failed ([Errno {}] {}), "
            "falling back to system temporary directory.".format(e.errno, e.strerror)
        )

        # If this also fails, all bets are off
        tempdir = tempfile.mkdtemp(prefix="automl_")

    try:
        # Create all files used for data exchange across client and server.
        config_file_name = touch_file(tempdir, "config")
        input_file_name = touch_file(tempdir, "input")
        output_file_name = touch_file(tempdir, "output")
        error_file_name = touch_file(tempdir, "error")
        stdout_file_name = touch_file(tempdir, "stdout")
        stderr_file_name = touch_file(tempdir, "stderr")

        # Create a configuration object to pass to the target process. This
        # configuration is applied prior to deserialization of the input,
        # thus it can influence the environment code gets loaded in.
        config = {
            "path": sys.path,
            "logger_names": log_server.logger_names,
            "log_verbosity": log_server.verbosity,
            "custom_dimensions": log_server.custom_dimensions,
        }

        # Use dill to store configuration information needed to set up
        # the target process.
        with open(config_file_name, "wb") as file:
            dill.dump(config, file, protocol=dill.HIGHEST_PROTOCOL)

        # Use dill to store the function and arguments to run in the target
        # process.
        with open(input_file_name, "wb") as file:
            dill.dump((f, args, kwargs), file, protocol=dill.HIGHEST_PROTOCOL)

        # Locate the Python executable, working directory, our sibling
        # spawn_server, and the environment variables.
        python_executable = sys.executable
        curdir = os.path.dirname(__file__)
        srv_script_file = os.path.join(curdir, "spawn_server.py")

        # Modify the log file path used by the child.
        env = os.environ.copy()
        log_path = os.path.split(os.environ.get(log_server.LOGFILE_ENV_NAME, "debug.log"))
        log_filename_split = os.path.splitext(log_path[1])
        env[log_server.LOGFILE_ENV_NAME] = os.path.join(
            log_path[0], log_filename_split[0] + "-child" + log_filename_split[1]
        )

        # Open files to redirect stdout and stderr to.
        with open(stdout_file_name, "w") as stdout, open(stderr_file_name, "w") as stderr:
            # Spawn child process and wait for completion.
            cmd = [
                python_executable,
                srv_script_file,
                config_file_name,
                input_file_name,
                output_file_name,
                error_file_name,
            ]

            process = subprocess.Popen(cmd, cwd=tempdir, env=env, stdout=stdout, stderr=stderr)
            try:
                process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                # Attempt to kill the process and its children, and report
                # the exception.
                subprocess_utilities.kill_process_tree(process.pid)
                raise

        check_process_success(process, stderr_file_name, error_file_name)

        # Read the output and use dill to deserialize the result.
        try:
            with open(error_file_name, "rb") as error_file:
                err, tb = cast(Tuple[Optional[BaseException], Optional[Dict[str, Any]]], dill.load(error_file))
        except FileNotFoundError:
            # There are some unknown situations where the error file does not exist, even though the exit code may be
            # zero. (Maybe caused by some external process deleting the file?) Normally, we shouldn't hit this because
            # the file is created before the process even spawns. Handle this case later if the output is also missing.
            err, tb = None, None

        if err is not None:
            # We MUST log the traceback here, because it is not possible to reraise with this fake traceback
            # without additional interpreter hacks involving manually constructing similar stack frames.
            # See python-tblib source code for an example of this hackery in action.
            # However, this will result in duplicate logging of child process errors.

            # For safety reasons, run this in a try-except to avoid weird edge cases that might have been missed.
            try:
                logging_utilities.log_traceback(err, logger, tb=FakeTraceback.deserialize(tb))
            except Exception as e:
                logging_utilities.log_traceback(e, logger)

            if isinstance(err, AutoMLException):
                # If it's one of ours, throw it as is
                raise err
            # We don't have the original traceback for the exception, so wrap it in one of ours and mark as PII.
            raise PipelineRunException.from_exception(
                err,
                "Pipeline execution failed with {}: {}".format(err.__class__.__name__, str(err)),
                "spawn_client",
                has_pii=True,
            ).with_generic_msg("Pipeline execution failed with {}".format(err.__class__.__name__))

        try:
            with open(output_file_name, "rb") as output_file:
                val = cast(T, dill.load(output_file))
        except FileNotFoundError:
            raise PipelineRunException._with_error(
                AzureMLError.create(
                    AutoMLInternal,
                    error_details="Pipeline execution failed - error in retrieving results from training subprocess",
                    target="spawn_client.run_in_proc",
                )
            )

        return val

    finally:
        if process is not None:
            for i in range(5):
                try:
                    # poll() returns None if the process is still running (no returncode)
                    if process.poll() is None:
                        subprocess_utilities.kill_process_tree(process.pid)
                    break
                except Exception:
                    pass

        try:

            def onerror(func: "Callable[..., Any]", path: str, exc_info: Any) -> None:
                exception = exc_info[1]
                if isinstance(exception, FileNotFoundError):
                    # if it doesn't exist anymore, we don't have to clean it up
                    logger.info("{} failed with FileNotFoundError, skipping.".format(func.__qualname__))
                    return
                if isinstance(exception, OSError):
                    logging_utilities.log_traceback(exception, logger)
                    logger.warning(
                        "{} failed with OSError ([Errno {}] {}) during temp file cleanup, skipping.".format(
                            func.__qualname__, exception.errno, exception.strerror
                        )
                    )
                else:
                    # As far as I know, this will only get called with OSError, but have this here in case
                    logging_utilities.log_traceback(exception, logger)
                    logger.warning(
                        "{} failed with {} during temp file cleanup, skipping.".format(
                            func.__qualname__, exception.__class__.__name__
                        )
                    )

            shutil.rmtree(tempdir, onerror=onerror)
        except Exception as e:
            logging_utilities.log_traceback(e, logger)
            logger.warning(
                "shutil.rmtree failed with {} during temp file cleanup, skipping.".format(e.__class__.__name__)
            )


def check_linux_oom_killed(pid: int) -> None:
    """
    Check to see if the Linux out of memory killer sent SIGKILL to this process. Raise an exception if killed by OOM.

    :param pid: process pid
    :return: None
    """
    oom_killed = False
    mem_usage = 0
    try:
        out = subprocess.run(["dmesg", "-l", "err"], stdout=subprocess.PIPE, universal_newlines=True)
        log_lines = out.stdout.strip().lower().split("\n")
        for line in log_lines:
            match = re.search(r"out of memory: killed process {} .+? anon-rss:(\d+)kb".format(pid), line)
            if match is not None:
                oom_killed = True
                mem_usage = int(match.group(1)) * 1024
    except Exception:
        pass

    if oom_killed:
        logger.info("OOM: memory usage: {}".format(str(mem_usage)))
        raise ResourceException._with_error(AzureMLError.create(InsufficientMemory))


def check_process_success(process: "subprocess.Popen[bytes]", stderr_file_name: str, error_file_name: str) -> None:
    """
    Check to see if this process exited successfully. In case of a positive non-zero exit code, stderr is logged.

    :param process: the process object from subprocess.Popen
    :param stderr_file_name: the path to the file containing stderr
    :return:
    """
    returncode = process.returncode

    if returncode < 0:
        # Note: negative return codes only occur on POSIX platforms and are caused by unhandled signals
        errorcode = -returncode
        errorname = signal.Signals(errorcode).name

        if sys.platform == "linux" and errorcode == signal.SIGKILL:
            # On Linux, the kernel memory allocator overcommits memory by default. If we attempt to
            # actually use all that memory, then the OOM killer will kick in and send SIGKILL. We
            # have to check the kernel logs to see if this is the case.
            check_linux_oom_killed(process.pid)

        if errorname in ["SIGKILL", "SIGABRT"]:
            raise ResourceException._with_error(
                AzureMLError.create(
                    InsufficientMemoryLikely, pid=process.pid, errorcode=errorcode, errorname=errorname
                )
            )
        raise SubprocessException.create_without_pii(
            "Subprocess (pid {}) killed by unhandled signal {} ({}).".format(process.pid, errorcode, errorname)
        )
    elif returncode > 0:
        if sys.platform == "win32":
            # ntstatus.h STATUS_QUOTA_EXCEEDED
            if returncode == 0xC0000044:
                raise CpuTimeoutException()

        # Ideally we would like to capture stderr here since it will have the real exception
        # when the returncode is 1, but it might have PII.
        with open(stderr_file_name, "r") as stderr:
            message = "Subprocess (pid {}) exited with non-zero exit status {}.".format(process.pid, returncode)
            message_with_stderr = "{} stderr output: \n{}".format(message, "\n".join(stderr.readlines()))
            raise SubprocessException(message_with_stderr).with_generic_msg(message)
