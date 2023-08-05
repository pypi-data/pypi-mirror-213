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

"""File for adding all the constants"""

from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class DatasetSplit:
    TEST = "test"
    TRAIN = "train"
    VALIDATION = "validation"


@dataclass
class SaveFileConstants:
    """
    A class to represent constants for metadata related to saving the model.
    """

    PREPROCESS_ARGS_SAVE_PATH = "preprocess_args.json"
    FINETUNE_ARGS_SAVE_PATH = "finetune_args.json"
    CLASSES_SAVE_PATH = "class_names.json"
    ID2LABEL_SAVE_PATH = "id2label.json"
    LABEL2ID_SAVE_PATH = "label2id.json"
    CLASSES_SAVE_KEY = "class_names"
    MODEL_SELECTOR_ARGS_SAVE_PATH = "model_selector_args.json"

@dataclass
class HfConstants:
    """
    A class to represent constants for hugging face files.
    """
    LARGE_MODEL_MAX_LENGTH = 1e6
    DEFAULT_MAX_SEQ_LENGTH = 512
    MODEL_MAX_LENGTH_KEY = "model_max_length"


@dataclass
class MLFlowHFFlavourConstants:
    """
    A class to represent constants for parameters of HF Flavour mlflow.
    """
    TRAIN_LABEL_LIST = "train_label_list"
    TASK_TYPE = "task_type"
    # NOTE ONLY used for Summarization and Translation tasks
    PREFIX_AND_TASK_FILE_SAVE_NAME_WITH_EXT = "azureml_tokenizer_prefix_mlflow_task.json"
    PREFIX_SAVE_KEY = "tokenizer_prefix"
    #
    TASK_SAVE_KEY = "mlflow_task"
    INFERENCE_PARAMS_SAVE_NAME_WITH_EXT = "azureml_mlflow_inference_params.json"
    INFERENCE_PARAMS_SAVE_KEY = "tokenizer_config"
    MISC_CONFIG_FILE = "MLmodel"
    MODEL_ROOT_DIRECTORY = "mlflow_model_folder"
    HUGGINGFACE_ID = "huggingface_id"
    LICENSE_FILE = "LICENSE"


@dataclass
class AzuremlConstants:
    """
    General constants
    """
    DATASET_COLUMN_PREFIX = "Azureml_"


@dataclass
class HfModelTypes:
    GPT2 = "gpt2"
    ROBERTA = "roberta"
    DEBERTA = "deberta"
    DISTILBERT = "distilbert"
    BERT = "bert"
    BART = "bart"
    MBART = "mbart"
    T5 = "t5"
    CAMEMBERT = "camembert"
    LLAMA = "llama"


@dataclass
class Tasks:
    """Supported Tasks"""
    SINGLE_LABEL_CLASSIFICATION = "SingleLabelClassification"
    MULTI_LABEL_CLASSIFICATION = "MultiLabelClassification"
    REGRESSION = "regression"
    NAMED_ENTITY_RECOGNITION = "NamedEntityRecognition"
    PARTS_OF_SPEECH_TAGGING = "PartsOfSpeechTagging"
    CHUNKING = "Chunking"
    SUMMARIZATION = "Summarization"
    TRANSLATION = "Translation"
    QUESTION_ANSWERING = "QuestionAnswering"
    NLP_NER = "NLPNER"
    NLP_MULTICLASS = "NLPMulticlass"
    NLP_MULTILABEL = "NLPMultilabel"


class MLFlowHFFlavourTasks:
    """
    A class to represent constants for MLFlow HF-Flavour supported tasks.
    """
    SINGLE_LABEL_CLASSIFICATION = "text-classification"
    MULTI_LABEL_CLASSIFICATION = "text-classification"
    NAMED_ENTITY_RECOGNITION = "token-classification"
    QUESTION_ANSWERING = "question-answering"
    SUMMARIZATION = "summarization"
    TRANSLATION = "translation"
    REGRESSION = "regression"
    CHUNKING = "chunking"
    PARTS_OF_SPEECH_TAGGING = "pos-tagging"


# Pyarrow ref
# https://github.com/huggingface/datasets/blob/9f9f0b536e128710115c486b0b9c319c3f0a570f/src/datasets/features/features.py#L404
INT_DTYPES = ["int8", "int16", "int32", "int64"]
STRING_DTYPES = ["string", "large_string"]
FLOAT_DTYPES = ["float16", "float32", "float64"]


@dataclass
class PreprocessArgsTemplate:
    """
    This is a template dataclass for preprocess arguments. This is inherited by respective
    task preprocess args class and most of the fields are populated there.

    placeholder_required_columns - dummy strings to represent the column names of the data. For instance,
    the dummy values for NER are `token_key`, `tag_key` i.e. placeholder_required_columns will be
    ["token_key", "tag_key"].
    """

    # init=False => this argument is not required during initialization but needs to be set in post init
    placeholder_required_columns: List[str] = field(
        init=False,
        default_factory=list
    )
    placeholder_required_column_dtypes: List[List[str]] = field(
        init=False,
        default_factory=list
    )
    placeholder_label_column: str
    required_columns: List[str] = field(
        init=False,
        default_factory=list
    )
    required_column_dtypes: List[List[str]] = field(
        init=False,
        default_factory=list
    )
    label_column: str = field(
        init=False
    )
    task_name: str
    mlflow_task_type: str
    problem_type: Optional[str]
    metric_for_best_model: str = field(
        metadata={
            "help": (
                "Use in conjunction with `load_best_model_at_end` to specify the metric to use to compare two"
                "different models. Must be the name of a metric returned by the evaluation with or without the prefix "
                '`"eval_"`. Will default to `"loss"` if unspecified and `load_best_model_at_end=True` '
                '(to use the evaluation loss). If you set this value, `greater_is_better` will default to `True`.'
                " Don't forget to set it to `False` if your metric is better when lower."
            )
        }
    )
    greater_is_better: bool = field(
        metadata={
            "help": (
                "Use in conjunction with `load_best_model_at_end` and `metric_for_best_model`"
                "to specify if better models should have a greater metric or not. Will default to:"
                '- `True` if `metric_for_best_model` is set to a value that isnt `"loss"` or `"eval_loss"`.'
                '- `False` if `metric_for_best_model` is not set, or set to `"loss"` or `"eval_loss"`.'
            )
        }
    )
    pad_to_max_length: str = field(
        metadata={
            "help": (
                "If true, all samples get padded to `max_seq_length`."
                "If false, will pad the samples dynamically when batching to the maximum length in the batch."
            )
        }
    )
    max_seq_length: int = field(
        metadata={
            "help": (
                "Max tokens of single example, set the value to -1 to use the default value."
                "Default value will be max seq length of pretrained model tokenizer"
            )
        }
    )
    batch_size: int = field(
        metadata={
            "help": (
                "Number of examples to batch before calling the tokenization function. "
                "This also controls the number of examples to batch while writing to cache and saving to the json file."
            )
        }
    )


@dataclass
class TaskConstants:
    NER_IGNORE_INDEX = -100
    TRANSLATION_IGNORE_INDEX = -100
    SUMMARIZATION_IGNORE_INDEX = -100
    MULTI_LABEL_THRESHOLD = 0.5
    MULTI_LABEL_NEW_COLUMN_SUFFIX = "_list"


@dataclass
class DataConstants:
    ENCODING = 'utf-8'
    ERRORS = "replace"


@dataclass
class AutomlConstants:
    DEFAULT_SEQ_LEN = 128
    LONG_RANGE_MAX = 256
    MIN_PROPORTION_LONG_RANGE = 0.1
    TEXT_CLASSIFICATION_COLUMN_NAME = "sentences"
    TEXT_NER_TOKEN_KEY = "tokens"
    TEXT_NER_TAG_KEY = "ner_tags_str"
    NER_IGNORE_TOKENS = ["", " ", "\n"]
    BATCH_SIZE = 32
