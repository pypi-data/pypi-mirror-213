# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
# Copyright 2020 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ---------------------------------------------------------

"""AzureML ACFT Image Components package - finetuning component huggingface."""

import os

from collections import OrderedDict
from typing import Union
from transformers import AutoConfig
from transformers.models.auto.modeling_auto import (
    MODEL_FOR_IMAGE_CLASSIFICATION_MAPPING_NAMES,
)

from azureml.acft.image.components.finetune.factory.mappings import MODEL_FAMILY_CLS
from azureml.acft.image.components.finetune.factory.task_definitions import Tasks
from azureml.acft.image.components.finetune.common.constants.constants import HfConstants
from azureml._common._error_definition.azureml_error import AzureMLError  # type: ignore

from azureml.acft.common_components import get_logger_app
from azureml.acft.common_components.utils.error_handling.exceptions import ACFTValidationException
from azureml.acft.common_components.utils.error_handling.error_definitions import ModelIncompatibleWithTask
from azureml.acft.image.components.finetune.huggingface.classification.trainer_classes import (
    ImageClassificationTrainerClasses,
)

logger = get_logger_app(__name__)


TASK_SUPPORTED_FAMILY_MAP = OrderedDict(
    [
        (Tasks.HF_MULTI_CLASS_IMAGE_CLASSIFICATION, MODEL_FOR_IMAGE_CLASSIFICATION_MAPPING_NAMES),
        (Tasks.HF_MULTI_LABEL_IMAGE_CLASSIFICATION, MODEL_FOR_IMAGE_CLASSIFICATION_MAPPING_NAMES),
    ]
)


class TrainerClasses:
    """Class for fetching and returning trainer classes."""
    def __init__(
        self, model_family: MODEL_FAMILY_CLS, model_name_or_path: Union[str, os.PathLike], task_name: Tasks
    ) -> None:
        """ init function for TrainerClasses
        :param model_family: related model_family to which current task belongs
        :type model_family: azureml.acft.accelerator.mappings.MODEL_FAMILY_CLS
        :param model_name_or_path: Hugging face image model name or path
        :type model_name_or_path: Union[str, os.PathLike]
        :param task_name: related task_name
        :type task_name: azureml.acft.accelerator.constants.task_definitions.Tasks
        """
        self.model_family = model_family
        self.task_name = task_name
        self.model_name_or_path = model_name_or_path
        self.model_type = TrainerClasses.get_hf_model_type(self.model_name_or_path)
        self._check_task_model_family_compatibility()

    @staticmethod
    def get_hf_model_type(model_name_or_path: Union[str, os.PathLike]) -> Union[str, None]:
        """Get model_type from model_name or model_path

        :param model_name_or_path: Hugging face image model name or path
        :type model_name_or_path: Union[str, os.PathLike]
        :return: model_type
        :rtype: str
        """
        # NOTE This is done to avoid multiple readings from the config file
        if HfConstants.HFModelType in os.environ:
            logger.info(f"Found the {HfConstants.HFModelType} in environment variable")
            return os.environ[HfConstants.HFModelType]
        try:
            config = AutoConfig.from_pretrained(model_name_or_path)
        except Exception as e:
            # TO DO: differentiate between azureml supported models and user resgistered
            # models and raise system/user errors.
            # change this to invalid model data error after its support in acft.accelerator
            raise ACFTValidationException._with_error(
                AzureMLError.create(ModelIncompatibleWithTask,
                                    error=str(e),
                                    ModelName=model_name_or_path,
                                    TaskName=Tasks.HF_MULTI_CLASS_IMAGE_CLASSIFICATION,
                                    file_name="config.json")
            )
        if config is None or not hasattr(config, "model_type"):
            logger.warning("Config is None. Model type cannot be fetched")
            os.environ[HfConstants.HFModelType] = None
            return None
        # os.environ[HfConstants.HfConfig] = config
        os.environ[HfConstants.HFModelType] = getattr(config, "model_type")
        return getattr(config, "model_type")

    def _check_task_model_family_compatibility(self):
        """Check if the given model supports the given task in the case of Hugging Face Models."""
        task_supported_model_families = TASK_SUPPORTED_FAMILY_MAP[self.task_name]
        if self.model_type not in task_supported_model_families:
            raise ACFTValidationException._with_error(
                AzureMLError.create(
                    ModelIncompatibleWithTask,
                    TaskName=self.task_name,
                    ModelName=self.model_name_or_path,
                )
            )
        else:
            return

    def get_trainer_classes_mapping(self):
        """Cet trainer class based on task_name."""
        if self.task_name in [
            Tasks.HF_MULTI_CLASS_IMAGE_CLASSIFICATION,
            Tasks.HF_MULTI_LABEL_IMAGE_CLASSIFICATION,
        ]:
            return ImageClassificationTrainerClasses
