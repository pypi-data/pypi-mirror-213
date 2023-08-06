# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Module for parsing information from yaml in python accessible attributes for the ModelSuite class.
"""

import related
from attr import define
from config_builder import BaseConfigClass
from mlcvzoo_base.configuration.model_config import ModelConfig


@define
class ModelTrainerConfig(BaseConfigClass):
    """
    Class for parsing general information about the model suite and also further information
    in respective hierarchy
    """

    __related_strict__ = True

    model_config: ModelConfig = related.ChildField(cls=ModelConfig)
