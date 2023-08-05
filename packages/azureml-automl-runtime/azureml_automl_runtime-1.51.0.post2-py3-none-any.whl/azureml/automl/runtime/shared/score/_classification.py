# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Definitions for classification metrics."""
from azureml.training.tabular.score._classification import (
    Accuracy,
    WeightedAccuracy,
    BalancedAccuracy,
    NormMacroRecall,
    LogLoss,
    AUCBinary,
    AUCMacro,
    AUCMicro,
    AUCWeighted,
    AveragePrecisionBinary,
    AveragePrecisionMacro,
    AveragePrecisionMicro,
    AveragePrecisionWeighted,
    MatthewsCorrelation,
    F1Binary,
    F1Macro,
    F1Micro,
    F1Weighted,
    PrecisionBinary,
    PrecisionMacro,
    PrecisionMicro,
    PrecisionWeighted,
    RecallBinary,
    RecallMacro,
    RecallMicro,
    RecallWeighted,
    AccuracyTable,
    ConfusionMatrix,
    ClassificationReport,
    IOUSamples,
    IOUMicro,
    IOUMacro,
    IOUWeighted,
    PrecisionClasswise,
    RecallClasswise,
    F1Classwise,
    IOUClasswise,
    AUCClasswise,
    AveragePrecisionClasswise,
)
