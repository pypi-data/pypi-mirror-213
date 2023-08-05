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

import json
import numpy as np
from pathlib import Path
import collections
from functools import partial

from typing import Any, Dict, List, Tuple, Optional

from ....constants.constants import SaveFileConstants, MLFlowHFFlavourConstants, Tasks
from ....nlp_auto.model import AzuremlAutoModelForQnA
from ....nlp_auto.tokenizer import AzuremlAutoTokenizer
from ..preprocess.base import QnADataset
from ....utils.mlflow_utils import SaveMLflowModelCallback, replace_deepspeed_zero3_mlflow_pytorch_weights

import torch.nn as nn

from datasets.arrow_dataset import Dataset
from datasets.load import load_metric

from azureml.acft.accelerator.utils.logging_utils import get_logger_app
from azureml.acft.accelerator.utils.error_handling.exceptions import ValidationException
from azureml.acft.accelerator.utils.error_handling.error_definitions import PathNotFound, ValidationError
from azureml._common._error_definition.azureml_error import AzureMLError  # type: ignore

from azureml.acft.accelerator.finetune import AzuremlFinetuneArgs, AzuremlDatasetArgs
from azureml.acft.accelerator.finetune import AzuremlTrainer
from azureml.acft.accelerator.constants import HfTrainerType

from transformers.tokenization_utils_base import PreTrainedTokenizerBase
from transformers.trainer_utils import EvalPrediction
from transformers.deepspeed import is_deepspeed_zero3_enabled


logger = get_logger_app()


class QnAFinetune:

    def __init__(self, finetune_params: Dict[str, Any]) -> None:
        # finetune params is finetune component args + args saved as part of preprocess
        self.finetune_params = finetune_params

        logger.info(f"Task name: {Tasks.QUESTION_ANSWERING}")

        # set log_metrics_at_root=False to not to log to parent
        self.finetune_params["log_metrics_at_root"] = False

    def _get_finetune_args(self, model_type: str) -> AzuremlFinetuneArgs:

        self.finetune_params["model_type"] = model_type
        azml_trainer_finetune_args = AzuremlFinetuneArgs(
            self.finetune_params,
            trainer_type=HfTrainerType.DEFAULT
        )

        return azml_trainer_finetune_args

    def _get_dataset_args(
        self,
        tokenizer: Optional[PreTrainedTokenizerBase] = None
    ) -> Tuple[AzuremlDatasetArgs, Dataset]:

        encoded_train_ds = QnADataset(
            Path(self.finetune_params["preprocess_output"], self.finetune_params["encoded_train_data_fname"]),
            tokenizer=tokenizer
        )
        encoded_validation_ds = QnADataset(
            Path(self.finetune_params["preprocess_output"], self.finetune_params["encoded_validation_data_fname"]),
        )
        azml_trainer_dataset_args = AzuremlDatasetArgs(
            train_dataset=encoded_train_ds.dataset,
            validation_dataset=encoded_validation_ds.dataset,
            data_collator=encoded_train_ds.get_collation_function()
        )

        # load the raw validation ds
        raw_validation_ds = QnADataset(
            Path(self.finetune_params["preprocess_output"], self.finetune_params["raw_validation_data_fname"]),
        )

        return azml_trainer_dataset_args, raw_validation_ds

    def _load_model(self) -> Tuple[nn.Module, str, List[str]]:

        model_params = {
            "ignore_mismatched_sizes": self.finetune_params["ignore_mismatched_sizes"],
            "resume_from_checkpoint": self.finetune_params["resume_from_checkpoint"],
        }

        model, model_type, new_initalized_layers = AzuremlAutoModelForQnA.from_pretrained(
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
            model_name=self.finetune_params["model_name"],
            model_name_or_path=self.finetune_params["model_name_or_path"],
            **{
                "mlflow_hftransformers_misc_conf": self.finetune_params.get("mlflow_hftransformers_misc_conf", {}),
            },
        )

        model, model_type, new_initialized_params = self._load_model()
        tokenizer = self._get_tokenizer()
        dataset_args, raw_validation_ds = self._get_dataset_args(tokenizer)
        trainer = AzuremlTrainer(
            finetune_args=self._get_finetune_args(model_type),
            dataset_args=dataset_args,
            model=model,
            tokenizer=tokenizer,
            metric_func=partial(
                qna_metrics_func,
                tokenizer=tokenizer,
                raw_eval_dataset=raw_validation_ds.dataset,
                enc_eval_dataset=dataset_args.validation_dataset,
                n_best_size=self.finetune_params["n_best_size"],
                max_answer_length_in_tokens=self.finetune_params["max_answer_length_in_tokens"],
                answers_key=self.finetune_params["answers_key"],
                context_key=self.finetune_params["context_key"]
            ),
            new_initalized_layers=new_initialized_params,
            custom_trainer_callbacks=[save_mlflow_callback],
        )

        # Torch barrier is used to complete the training on a distributed setup
        # Use callbacks for adding steps to be done at the end of training
        # NOTE Avoid adding any logic after trainer.train()
        # Test the distributed scenario in case you add any logic beyond trainer.train()
        trainer.train()

        # replace pytorch weights for lora / deep speed zero3 optimization
        if trainer.should_save and (self.finetune_params["apply_lora"] or is_deepspeed_zero3_enabled()):
            logger.info("Replacing dummy MLflow weights ")
            replace_deepspeed_zero3_mlflow_pytorch_weights(
                self.finetune_params["pytorch_model_folder"],
                self.finetune_params["mlflow_model_folder"]
            )

        # save files only once by Rank-0 process
        if trainer.should_save:
            # save finetune args
            Path(self.finetune_params["pytorch_model_folder"]).mkdir(exist_ok=True, parents=True)
            finetune_args_path = Path(self.finetune_params["pytorch_model_folder"], \
                SaveFileConstants.FINETUNE_ARGS_SAVE_PATH)
            self.finetune_params["model_name_or_path"] = str(self.finetune_params["model_name_or_path"])
            with open(finetune_args_path, 'w') as rptr:
                json.dump(self.finetune_params, rptr, indent=2)


def qna_metrics_func(
    eval_pred: EvalPrediction,
    tokenizer: PreTrainedTokenizerBase,
    raw_eval_dataset: Dataset,
    enc_eval_dataset: Dataset,
    n_best_size: int,
    max_answer_length_in_tokens: int,
    answers_key: str,
    context_key: str
):
    """
    compute the metrics for question answering
    `n_best_size` represents the top start and end logits to be considered to predict the answer
    `max_answer_length_in_tokens` represents maximum answer length to be permitted

    # NOTE the order of :param all_start_logits should be in sync with :param raw_eval_dataset and
    # :param enc_eval_dataset
    # This means that the current logic of metric calculation will FAIL in case the eval dataset is shuffled as the
    # order of :param all_start_logits will go out of sync with other two parameters after sync
    """
    # Raw predictions contain the output of the model. since the model needs to predict the start and end
    # character postions i.e. 2 labels, the `raw_predictions` dims will be 2 x num_tokens
    raw_predictions, _ = eval_pred
    all_start_logits, all_end_logits = raw_predictions

    # Tokenized evaluation dataset - output of preprocessor component
    validation_dataset_plus_features = enc_eval_dataset
    answers_validation_column_data = raw_eval_dataset[answers_key]
    context_validation_column_data = raw_eval_dataset[context_key]
    offset_mapping_validation_column_data = validation_dataset_plus_features["offset_mapping_validation"]
    input_ids_column_data = validation_dataset_plus_features["input_ids"]

    # Build a map example to its corresponding context splits
    example_split_indices_map = collections.defaultdict(list)
    for i, sample_index in enumerate(validation_dataset_plus_features["example_id"]):
        example_split_indices_map[sample_index].append(i)

    # The dictionaries we have to fill - Predictions and Ground Truths
    predictions = collections.OrderedDict()
    references = collections.OrderedDict()

    # Let's loop over all the examples!
    invalid_offset_value = [-1, -1]
    for example_index, split_indices in example_split_indices_map.items():

        # There will be atleast one feature per example, using `split_indices[0]` should be valid always
        # `answers` column is duplicated across all split indices
        references[example_index] = {
            "id": example_index,
            "answers": answers_validation_column_data[example_index]
        }
        min_null_score = None  # Only used if squad_v2 is True.
        valid_answers = []

        # Looping through all the splits associated to the current example.
        for split_index in split_indices:
            context = context_validation_column_data[example_index]
            # We grab the predictions of the model for this split.
            start_logits = all_start_logits[split_index]
            end_logits = all_end_logits[split_index]
            # This is what will allow us to map some the positions in our logits to span of texts in the original
            # context.
            offset_mapping = offset_mapping_validation_column_data[split_index]

            # Update minimum null prediction.
            if tokenizer.cls_token_id is not None:
                cls_index = input_ids_column_data[split_index].index(tokenizer.cls_token_id)
            else:
                cls_index = 0
            feature_null_score = start_logits[cls_index] + end_logits[cls_index]
            if min_null_score is None or min_null_score < feature_null_score:
                min_null_score = feature_null_score

            # Go through all possibilities for the `n_best_size` greater start and end logits.
            start_indexes = np.argsort(start_logits)[-1:-n_best_size-1:-1].tolist()
            end_indexes = np.argsort(end_logits)[-1:-n_best_size-1:-1].tolist()
            for start_index in start_indexes:
                for end_index in end_indexes:
                    # Don't consider out-of-scope answers, either because the indices are out of bounds or correspond
                    # to part of the input_ids that are not in the context.
                    if (
                        start_index >= len(offset_mapping)
                        or end_index >= len(offset_mapping)
                        or offset_mapping[start_index] == invalid_offset_value
                        or offset_mapping[end_index] == invalid_offset_value
                    ):
                        continue
                    # Don't consider answers with a length that is either < 0 or > max_answer_length_in_tokens.
                    if end_index < start_index or end_index - start_index + 1 > max_answer_length_in_tokens:
                        continue

                    start_char = offset_mapping[start_index][0]
                    end_char = offset_mapping[end_index][1]
                    valid_answers.append(
                        {
                            "score": start_logits[start_index] + end_logits[end_index],
                            "text": context[start_char: end_char]
                        }
                    )

        if len(valid_answers) > 0:
            best_answer = sorted(valid_answers, key=lambda x: x["score"], reverse=True)[0]
        else:
            # In the very rare edge case we have not a single non-null prediction, we create a fake prediction to avoid
            # failure.
            best_answer = {"text": "", "score": 0.0}

        answer = best_answer["text"] if best_answer["score"] > min_null_score else ""
        predictions[example_index] = answer

    metric = load_metric("squad_v2")
    formatted_predictions = [
        {"id": k, "prediction_text": v, "no_answer_probability": 0.0} for k, v in predictions.items()]
    formatted_references = list(references.values())
    logger.info(f"Predictions count: {len(formatted_predictions)} | References count: {len(formatted_references)}")
    metrics = metric.compute(predictions=formatted_predictions, references=formatted_references)

    return metrics
