# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Definition of the DarknetConfig that is used to configure the DarknetDetectionModel.
"""

from typing import Optional

import related
from attr import define
from config_builder import BaseConfigClass
from mlcvzoo_base.api.configuration import InferenceConfig, ModelConfiguration
from mlcvzoo_base.configuration.annotation_handler_config import AnnotationHandlerConfig
from mlcvzoo_base.configuration.class_mapping_config import ClassMappingConfig
from mlcvzoo_base.configuration.reduction_mapping_config import ReductionMappingConfig
from mlcvzoo_base.configuration.replacement_config import ReplacementConfig


@define
class DarknetDataFileConfig(BaseConfigClass):
    # Darknet's class mapping file
    __related_strict__ = True
    names: str = related.StringField()
    # Number of classes
    classes: int = related.IntegerField()
    valid: str = related.StringField(default="darknet.valid")
    backup: str = related.StringField(default="darknet.backup")
    eval: str = related.StringField(default="darknet.eval")
    train: str = related.StringField(default="darknet.train")


@define
class DarknetInferenceConfig(InferenceConfig):
    __related_strict__ = True
    hier_threshold: float = related.FloatField()
    nms_threshold: float = related.FloatField()

    data_path: str = related.StringField()

    data_file: DarknetDataFileConfig = related.ChildField(cls=DarknetDataFileConfig)

    reduction_class_mapping: Optional[ReductionMappingConfig] = related.ChildField(
        cls=ReductionMappingConfig, required=False, default=None
    )

    def check_values(self) -> bool:
        return (
            0.0 <= self.score_threshold <= 1.0
            and 0.0 <= self.nms_threshold <= 1.0
            and 0.0 <= self.hier_threshold <= 1.0
        )


@define
class DarknetTrainingConfig(BaseConfigClass):
    __related_strict__ = True
    # Path to the .cfg file for the yolo network
    config_path: str = related.StringField()

    # directory where all the output data of a training run is stored
    work_dir: str = related.StringField()

    train_annotation_handler_config: AnnotationHandlerConfig = related.ChildField(
        cls=AnnotationHandlerConfig, required=False, default=None
    )


@define
class DarknetConfig(ModelConfiguration):
    __related_strict__ = True

    darknet_commit_sha: str = related.StringField()

    class_mapping: ClassMappingConfig = related.ChildField(cls=ClassMappingConfig)

    inference_config: DarknetInferenceConfig = related.ChildField(
        cls=DarknetInferenceConfig
    )

    train_config: DarknetTrainingConfig = related.ChildField(cls=DarknetTrainingConfig)

    darknet_dir: str = related.StringField(
        required=False, default=ReplacementConfig.DARKNET_DIR_KEY
    )
