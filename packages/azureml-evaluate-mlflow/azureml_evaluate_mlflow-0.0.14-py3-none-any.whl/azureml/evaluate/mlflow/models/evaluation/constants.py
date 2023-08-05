# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
""" Constants used for model evaluation."""


class EvaluationSettingLiterals:
    MULTI_LABEL = "multilabel"


class EvaluationMiscLiterals:
    IMAGE_OUTPUT_LABEL_COLUMN = "labels"
    IMAGE_OUTPUT_PROBS_COLUMN = "probs"
    THRESHOLD = "threshold"


class EvaluationDefaultSetting:
    """Default settings for model evaluation."""
    MULTI_LABEL_PRED_THRESHOLD = 0.5
