# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Module for configuring the parsing of information from yaml in python
accessible attributes for the Evaluation Runner (ER) class
"""

from typing import List, Optional

import related
from attr import define
from config_builder import BaseConfigClass
from mlcvzoo_base.configuration.annotation_handler_config import AnnotationHandlerConfig
from mlcvzoo_base.configuration.mlfow_config import MLFlowConfig
from mlcvzoo_base.configuration.model_config import ModelConfig
from mlcvzoo_base.evaluation.object_detection.configuration import (
    TensorboardLoggingConfig,
)

from mlcvzoo_util.model_evaluator.structs import CheckpointLoggingModes


@define
class ModelEvaluatorMLflowConfig(BaseConfigClass):
    """Class for parsing information for mlflow"""

    __related_strict__ = True

    config: MLFlowConfig = related.ChildField(cls=MLFlowConfig)

    checkpoint_log_mode: str = related.StringField(
        required=False, default=CheckpointLoggingModes.NONE.value
    )


@define
class CheckpointConfig(BaseConfigClass):
    """Class for parsing information about model checkpoints to evaluate"""

    __related_strict__ = True

    checkpoint_dir: str = related.StringField()
    checkpoint_filename_suffix: str = related.StringField()
    ignore: List[str] = related.SequenceField(cls=str, required=False, default=[])


@define
class ModelEvaluatorConfig(BaseConfigClass):
    """Class for parsing information from yaml in respective hierarchy"""

    __related_strict__ = True

    iou_thresholds: List[float] = related.SequenceField(cls=float)

    checkpoint_config: Optional[CheckpointConfig] = related.ChildField(
        cls=CheckpointConfig, required=False, default=None
    )

    mlflow_config: Optional[ModelEvaluatorMLflowConfig] = related.ChildField(
        cls=ModelEvaluatorMLflowConfig, required=False, default=None
    )

    tensorboard_logging_config: Optional[TensorboardLoggingConfig] = related.ChildField(
        cls=TensorboardLoggingConfig, required=False, default=None
    )


@define
class ModelEvaluatorCLIConfig(ModelEvaluatorConfig):
    """Class for parsing information from yaml in respective hierarchy"""

    __related_strict__ = True

    iou_thresholds: List[float] = related.SequenceField(float)

    model_config: ModelConfig = related.ChildField(cls=ModelConfig)

    checkpoint_config: CheckpointConfig = related.ChildField(cls=CheckpointConfig)

    annotation_handler_config: AnnotationHandlerConfig = related.ChildField(
        cls=AnnotationHandlerConfig
    )

    mlflow_config: Optional[ModelEvaluatorMLflowConfig] = related.ChildField(
        cls=ModelEvaluatorMLflowConfig, required=False, default=None
    )

    tensorboard_logging_config: Optional[TensorboardLoggingConfig] = related.ChildField(
        cls=TensorboardLoggingConfig, required=False, default=None
    )
