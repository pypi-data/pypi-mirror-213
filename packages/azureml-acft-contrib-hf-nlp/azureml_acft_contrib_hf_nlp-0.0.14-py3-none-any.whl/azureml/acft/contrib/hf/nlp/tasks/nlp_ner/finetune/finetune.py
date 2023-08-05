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

"""
NLP NER
"""

import json
import numpy as np
from pathlib import Path
from functools import partial

from typing import Any, Dict, List, Tuple, Optional

from ..preprocess.base import NLPNerDataset
from ....constants.constants import SaveFileConstants, MLFlowHFFlavourConstants, TaskConstants
from ....nlp_auto.model import AzuremlAutoModelForTokenClassification
from ....nlp_auto.tokenizer import AzuremlAutoTokenizer
from ....utils.mlflow_utils import SaveMLflowModelCallback

import torch.nn as nn

from azureml.acft.accelerator.utils.logging_utils import get_logger_app
from azureml.acft.accelerator.utils.error_handling.exceptions import ValidationException
from azureml.acft.accelerator.utils.error_handling.error_definitions import PathNotFound, ValidationError
from azureml._common._error_definition.azureml_error import AzureMLError  # type: ignore

from azureml.acft.accelerator.finetune import AzuremlFinetuneArgs, AzuremlDatasetArgs
from azureml.acft.accelerator.finetune import AzuremlTrainer
from azureml.acft.accelerator.constants import HfTrainerType

from datasets.load import load_metric

from transformers.tokenization_utils_base import PreTrainedTokenizerBase
from transformers.trainer_utils import EvalPrediction


logger = get_logger_app()


class NLPNerFinetune:

    def __init__(self, finetune_params: Dict[str, Any]) -> None:
        # finetune params is finetune component args + args saved as part of preprocess
        self.finetune_params = finetune_params

        # Load class names
        class_names_load_path = Path(self.finetune_params["preprocess_output"], SaveFileConstants.CLASSES_SAVE_PATH)
        with open(class_names_load_path, 'r') as rptr:
            self.finetune_params["class_names"] = json.load(rptr)[SaveFileConstants.CLASSES_SAVE_KEY]
            self.finetune_params["num_labels"] = len(self.finetune_params["class_names"])

        # if :param `resume_from_checkpoint` is set to True
        #   - only load the weights using config while creating model object
        #   - update the `resume_from_checkpoint` to the model_name_or_path to load the model, and optimizer and
        #     scheduler states if exist
        if self.finetune_params.pop("resume_from_checkpoint", False) \
            and isinstance(self.finetune_params["model_name_or_path"], Path) \
                and self.finetune_params["model_name_or_path"].is_dir():
                self.finetune_params["resume_from_checkpoint"] = self.finetune_params["model_name_or_path"]

    def _get_finetune_args(self, model_type: str) -> AzuremlFinetuneArgs:

        self.finetune_params["model_type"] = model_type
        azml_trainer_finetune_args = AzuremlFinetuneArgs(
            self.finetune_params,
            trainer_type=HfTrainerType.DEFAULT
        )

        return azml_trainer_finetune_args

    def _get_dataset_args(self, tokenizer: Optional[PreTrainedTokenizerBase]=None) -> AzuremlDatasetArgs:

        encoded_train_ds = NLPNerDataset(
            str(Path(self.finetune_params["preprocess_output"], self.finetune_params["encoded_train_data_fname"])),
            tokenizer=tokenizer
        )
        encoded_validation_ds = NLPNerDataset(
            str(Path(self.finetune_params["preprocess_output"], self.finetune_params["encoded_validation_data_fname"])),
        )
        azml_trainer_dataset_args = AzuremlDatasetArgs(
            train_dataset=encoded_train_ds.dataset,
            validation_dataset=encoded_validation_ds.dataset,
            data_collator=encoded_train_ds.get_collation_function()
        )

        return azml_trainer_dataset_args
    
    def _load_model(self) -> Tuple[nn.Module, str, List[str]]:

        class_names = self.finetune_params["class_names"]
        id2label = {idx: lbl for idx, lbl in enumerate(class_names)}
        label2id = {lbl: idx for idx, lbl in enumerate(class_names)}
        model_params = {
            "problem_type": "single_label_classification",
            "num_labels": self.finetune_params["num_labels"],
            "id2label": id2label,
            "label2id": label2id,
            "ignore_mismatched_sizes": self.finetune_params["ignore_mismatched_sizes"],
        }

        model, model_type, new_initalized_layers = AzuremlAutoModelForTokenClassification.from_pretrained(
            self.finetune_params["model_name_or_path"], **model_params)

        return model, model_type, new_initalized_layers

    def _get_tokenizer(self) -> PreTrainedTokenizerBase:
        """This method loads the tokenizer as is w/o any modifications to it"""

        tokenizer_params = {
            "apply_adjust": False,
            "task_name": self.finetune_params["task_name"],
        }

        return AzuremlAutoTokenizer.from_pretrained(self.finetune_params["preprocess_output"], **tokenizer_params)

    def finetune(self) -> None:

        # configure MLflow save callback
        mlflow_infer_params_file_path = Path(
            self.finetune_params["preprocess_output"], MLFlowHFFlavourConstants.INFERENCE_PARAMS_SAVE_NAME_WITH_EXT
        )
        save_mlflow_callback = SaveMLflowModelCallback(
            mlflow_infer_params_file_path=mlflow_infer_params_file_path,
            mlflow_model_save_path=self.finetune_params["mlflow_model_folder"],
            mlflow_task_type=self.finetune_params["mlflow_task_type"],
            class_names=self.finetune_params["class_names"],
            model_name_or_path=self.finetune_params["model_name"]
        )

        # save finetune args
        # saving the args before the finetune to avoid issues related to distributed training
        Path(self.finetune_params["pytorch_model_folder"]).mkdir(exist_ok=True)
        finetune_args_path = Path(
            self.finetune_params["pytorch_model_folder"], SaveFileConstants.FINETUNE_ARGS_SAVE_PATH)
        self.finetune_params["model_name_or_path"] = str(self.finetune_params["model_name_or_path"])
        with open(finetune_args_path, 'w') as rptr:
            json.dump(self.finetune_params, rptr, indent=2)
        # save the classes list for azmlft inference compatability
        classes_save_path = Path(self.finetune_params["pytorch_model_folder"], SaveFileConstants.CLASSES_SAVE_PATH)
        class_names_json = {SaveFileConstants.CLASSES_SAVE_KEY: self.finetune_params["class_names"]}
        with open(classes_save_path, "w") as wptr:
            json.dump(class_names_json, wptr)
        logger.info(f"Classes file saved at {classes_save_path}")

        model, model_type, new_initialized_params = self._load_model()
        tokenizer=self._get_tokenizer()
        trainer = AzuremlTrainer(
            finetune_args=self._get_finetune_args(model_type),
            dataset_args=self._get_dataset_args(tokenizer),
            model=model,
            tokenizer=tokenizer,
            metric_func=partial(
                ner_metrics_func,
                class_names=self.finetune_params["class_names"]
            ),
            new_initalized_layers=new_initialized_params,
            custom_trainer_callbacks=[save_mlflow_callback],
        )

        # Torch barrier is used to complete the training on a distributed setup
        # Use callbacks for adding steps to be done at the end of training
        # NOTE Avoid adding any logic after trainer.train()
        # Test the distributed scenario in case you add any logic beyond trainer.train()
        trainer.train()


def ner_metrics_func(eval_pred: EvalPrediction, class_names: List[str]) -> Dict:
    """Compute and return metrics for Named Entity Recognition"""

    metric = load_metric("seqeval")

    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=2)

    # Remove ignored index (special tokens)
    true_predictions = [
        [class_names[p] for (p, l) in zip(prediction, label) if l != TaskConstants.NER_IGNORE_INDEX]
        for prediction, label in zip(predictions, labels)
    ]
    true_labels = [
        [class_names[l] for (p, l) in zip(prediction, label) if l != TaskConstants.NER_IGNORE_INDEX]
        for prediction, label in zip(predictions, labels)
    ]

    results = metric.compute(predictions=true_predictions, references=true_labels)

    if results is not None:
        return {
            "precision": results["overall_precision"],
            "recall": results["overall_recall"],
            "f1": results["overall_f1"],
            "accuracy": results["overall_accuracy"],
        }
    else:
        return {
            "precision": None,
            "recall": None,
            "f1": None,
            "accuracy": None
        }
