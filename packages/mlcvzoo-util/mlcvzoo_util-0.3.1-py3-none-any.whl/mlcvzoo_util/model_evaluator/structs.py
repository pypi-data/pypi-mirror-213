# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Module for defining enums and structs that are used across the
model_evaluator package.
"""
from dataclasses import dataclass
from enum import Enum, auto


class CheckpointLoggingModes(Enum):
    BEST = "best"
    ALL = "all"
    NONE = "none"


@dataclass
class CheckpointInfo:
    """
    Dataclass for storing information about a checkpoint
    and its overall AP metric
    """

    path: str
    score: float
