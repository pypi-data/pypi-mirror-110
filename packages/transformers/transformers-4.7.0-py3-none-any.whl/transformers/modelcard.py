# coding=utf-8
# Copyright 2018 The HuggingFace Inc. team.
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
""" Configuration base class and utilities."""


import copy
import json
import os
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import requests
import yaml
from huggingface_hub import HfApi

from . import __version__
from .file_utils import (
    CONFIG_NAME,
    MODEL_CARD_NAME,
    TF2_WEIGHTS_NAME,
    WEIGHTS_NAME,
    cached_path,
    hf_bucket_url,
    is_datasets_available,
    is_offline_mode,
    is_remote_url,
    is_tokenizers_available,
    is_torch_available,
)
from .training_args import ParallelMode
from .utils import logging
from .utils.modeling_auto_mapping import (
    MODEL_FOR_CAUSAL_LM_MAPPING_NAMES,
    MODEL_FOR_IMAGE_CLASSIFICATION_MAPPING_NAMES,
    MODEL_FOR_MASKED_LM_MAPPING_NAMES,
    MODEL_FOR_OBJECT_DETECTION_MAPPING_NAMES,
    MODEL_FOR_QUESTION_ANSWERING_MAPPING_NAMES,
    MODEL_FOR_SEQ_TO_SEQ_CAUSAL_LM_MAPPING_NAMES,
    MODEL_FOR_SEQUENCE_CLASSIFICATION_MAPPING_NAMES,
    MODEL_FOR_TABLE_QUESTION_ANSWERING_MAPPING_NAMES,
    MODEL_FOR_TOKEN_CLASSIFICATION_MAPPING_NAMES,
)


TASK_MAPPING = {
    "text-generation": MODEL_FOR_CAUSAL_LM_MAPPING_NAMES,
    "image-classification": MODEL_FOR_IMAGE_CLASSIFICATION_MAPPING_NAMES,
    "fill-mask": MODEL_FOR_MASKED_LM_MAPPING_NAMES,
    "object-detection": MODEL_FOR_OBJECT_DETECTION_MAPPING_NAMES,
    "question-answering": MODEL_FOR_QUESTION_ANSWERING_MAPPING_NAMES,
    "text2text-generation": MODEL_FOR_SEQ_TO_SEQ_CAUSAL_LM_MAPPING_NAMES,
    "text-classification": MODEL_FOR_SEQUENCE_CLASSIFICATION_MAPPING_NAMES,
    "table-question-answering": MODEL_FOR_TABLE_QUESTION_ANSWERING_MAPPING_NAMES,
    "token-classification": MODEL_FOR_TOKEN_CLASSIFICATION_MAPPING_NAMES,
}

logger = logging.get_logger(__name__)


class ModelCard:
    r"""
    Structured Model Card class. Store model card as well as methods for loading/downloading/saving model cards.

    Please read the following paper for details and explanation on the sections: "Model Cards for Model Reporting" by
    Margaret Mitchell, Simone Wu, Andrew Zaldivar, Parker Barnes, Lucy Vasserman, Ben Hutchinson, Elena Spitzer,
    Inioluwa Deborah Raji and Timnit Gebru for the proposal behind model cards. Link: https://arxiv.org/abs/1810.03993

    Note: A model card can be loaded and saved to disk.

    Parameters:
    """

    def __init__(self, **kwargs):
        warnings.warn(
            "The class `ModelCard` is deprecated and will be removed in version 5 of Transformers", FutureWarning
        )
        # Recommended attributes from https://arxiv.org/abs/1810.03993 (see papers)
        self.model_details = kwargs.pop("model_details", {})
        self.intended_use = kwargs.pop("intended_use", {})
        self.factors = kwargs.pop("factors", {})
        self.metrics = kwargs.pop("metrics", {})
        self.evaluation_data = kwargs.pop("evaluation_data", {})
        self.training_data = kwargs.pop("training_data", {})
        self.quantitative_analyses = kwargs.pop("quantitative_analyses", {})
        self.ethical_considerations = kwargs.pop("ethical_considerations", {})
        self.caveats_and_recommendations = kwargs.pop("caveats_and_recommendations", {})

        # Open additional attributes
        for key, value in kwargs.items():
            try:
                setattr(self, key, value)
            except AttributeError as err:
                logger.error(f"Can't set {key} with value {value} for {self}")
                raise err

    def save_pretrained(self, save_directory_or_file):
        """Save a model card object to the directory or file `save_directory_or_file`."""
        if os.path.isdir(save_directory_or_file):
            # If we save using the predefined names, we can load using `from_pretrained`
            output_model_card_file = os.path.join(save_directory_or_file, MODEL_CARD_NAME)
        else:
            output_model_card_file = save_directory_or_file

        self.to_json_file(output_model_card_file)
        logger.info(f"Model card saved in {output_model_card_file}")

    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path, **kwargs):
        r"""
        Instantiate a :class:`~transformers.ModelCard` from a pre-trained model model card.

        Parameters:
            pretrained_model_name_or_path: either:

                - a string, the `model id` of a pretrained model card hosted inside a model repo on huggingface.co.
                  Valid model ids can be located at the root-level, like ``bert-base-uncased``, or namespaced under a
                  user or organization name, like ``dbmdz/bert-base-german-cased``.
                - a path to a `directory` containing a model card file saved using the
                  :func:`~transformers.ModelCard.save_pretrained` method, e.g.: ``./my_model_directory/``.
                - a path or url to a saved model card JSON `file`, e.g.: ``./my_model_directory/modelcard.json``.

            cache_dir: (`optional`) string:
                Path to a directory in which a downloaded pre-trained model card should be cached if the standard cache
                should not be used.

            kwargs: (`optional`) dict: key/value pairs with which to update the ModelCard object after loading.

                - The values in kwargs of any keys which are model card attributes will be used to override the loaded
                  values.
                - Behavior concerning key/value pairs whose keys are *not* model card attributes is controlled by the
                  `return_unused_kwargs` keyword parameter.

            proxies: (`optional`) dict, default None:
                A dictionary of proxy servers to use by protocol or endpoint, e.g.: {'http': 'foo.bar:3128',
                'http://hostname': 'foo.bar:4012'}. The proxies are used on each request.

            find_from_standard_name: (`optional`) boolean, default True:
                If the pretrained_model_name_or_path ends with our standard model or config filenames, replace them
                with our standard modelcard filename. Can be used to directly feed a model/config url and access the
                colocated modelcard.

            return_unused_kwargs: (`optional`) bool:

                - If False, then this function returns just the final model card object.
                - If True, then this functions returns a tuple `(model card, unused_kwargs)` where `unused_kwargs` is a
                  dictionary consisting of the key/value pairs whose keys are not model card attributes: ie the part of
                  kwargs which has not been used to update `ModelCard` and is otherwise ignored.

        Examples::

            modelcard = ModelCard.from_pretrained('bert-base-uncased')    # Download model card from huggingface.co and cache.
            modelcard = ModelCard.from_pretrained('./test/saved_model/')  # E.g. model card was saved using `save_pretrained('./test/saved_model/')`
            modelcard = ModelCard.from_pretrained('./test/saved_model/modelcard.json')
            modelcard = ModelCard.from_pretrained('bert-base-uncased', output_attentions=True, foo=False)

        """
        # This imports every model so let's do it dynamically here.
        from transformers.models.auto.configuration_auto import ALL_PRETRAINED_CONFIG_ARCHIVE_MAP

        cache_dir = kwargs.pop("cache_dir", None)
        proxies = kwargs.pop("proxies", None)
        find_from_standard_name = kwargs.pop("find_from_standard_name", True)
        return_unused_kwargs = kwargs.pop("return_unused_kwargs", False)
        from_pipeline = kwargs.pop("_from_pipeline", None)

        user_agent = {"file_type": "model_card"}
        if from_pipeline is not None:
            user_agent["using_pipeline"] = from_pipeline

        if pretrained_model_name_or_path in ALL_PRETRAINED_CONFIG_ARCHIVE_MAP:
            # For simplicity we use the same pretrained url than the configuration files
            # but with a different suffix (modelcard.json). This suffix is replaced below.
            model_card_file = ALL_PRETRAINED_CONFIG_ARCHIVE_MAP[pretrained_model_name_or_path]
        elif os.path.isdir(pretrained_model_name_or_path):
            model_card_file = os.path.join(pretrained_model_name_or_path, MODEL_CARD_NAME)
        elif os.path.isfile(pretrained_model_name_or_path) or is_remote_url(pretrained_model_name_or_path):
            model_card_file = pretrained_model_name_or_path
        else:
            model_card_file = hf_bucket_url(pretrained_model_name_or_path, filename=MODEL_CARD_NAME, mirror=None)

        if find_from_standard_name or pretrained_model_name_or_path in ALL_PRETRAINED_CONFIG_ARCHIVE_MAP:
            model_card_file = model_card_file.replace(CONFIG_NAME, MODEL_CARD_NAME)
            model_card_file = model_card_file.replace(WEIGHTS_NAME, MODEL_CARD_NAME)
            model_card_file = model_card_file.replace(TF2_WEIGHTS_NAME, MODEL_CARD_NAME)

        try:
            # Load from URL or cache if already cached
            resolved_model_card_file = cached_path(
                model_card_file, cache_dir=cache_dir, proxies=proxies, user_agent=user_agent
            )
            if resolved_model_card_file == model_card_file:
                logger.info(f"loading model card file {model_card_file}")
            else:
                logger.info(f"loading model card file {model_card_file} from cache at {resolved_model_card_file}")
            # Load model card
            modelcard = cls.from_json_file(resolved_model_card_file)

        except (EnvironmentError, json.JSONDecodeError):
            # We fall back on creating an empty model card
            modelcard = cls()

        # Update model card with kwargs if needed
        to_remove = []
        for key, value in kwargs.items():
            if hasattr(modelcard, key):
                setattr(modelcard, key, value)
                to_remove.append(key)
        for key in to_remove:
            kwargs.pop(key, None)

        logger.info(f"Model card: {modelcard}")
        if return_unused_kwargs:
            return modelcard, kwargs
        else:
            return modelcard

    @classmethod
    def from_dict(cls, json_object):
        """Constructs a `ModelCard` from a Python dictionary of parameters."""
        return cls(**json_object)

    @classmethod
    def from_json_file(cls, json_file):
        """Constructs a `ModelCard` from a json file of parameters."""
        with open(json_file, "r", encoding="utf-8") as reader:
            text = reader.read()
        dict_obj = json.loads(text)
        return cls(**dict_obj)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.to_json_string())

    def to_dict(self):
        """Serializes this instance to a Python dictionary."""
        output = copy.deepcopy(self.__dict__)
        return output

    def to_json_string(self):
        """Serializes this instance to a JSON string."""
        return json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n"

    def to_json_file(self, json_file_path):
        """Save this instance to a json file."""
        with open(json_file_path, "w", encoding="utf-8") as writer:
            writer.write(self.to_json_string())


AUTOGENERATED_COMMENT = """
<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->
"""


TASK_TAG_TO_NAME_MAPPING = {
    "fill-mask": "Masked Language Modeling",
    "image-classification": "Image Classification",
    "multiple-choice": "Multiple Choice",
    "object-detection": "Object Detection",
    "question-answering": "Question Answering",
    "summarization": "Summarization",
    "table-question-answering": "Table Question Answering",
    "text-classification": "Text Classification",
    "text-generation": "Causal Language Modeling",
    "text2text-generation": "Sequence-to-sequence Language Modeling",
    "token-classification": "Token Classification",
    "translation": "Translation",
    "zero-shot-classification": "Zero Shot Classification",
}


METRIC_TAGS = [
    "accuracy",
    "bleu",
    "f1",
    "matthews_correlation",
    "pearsonr",
    "precision",
    "recall",
    "rouge",
    "sacrebleu",
    "spearmanr",
]


def _listify(obj):
    if obj is None:
        return []
    elif isinstance(obj, str):
        return [obj]
    else:
        return obj


def _insert_values_as_list(metadata, name, values):
    if values is None:
        return metadata
    if isinstance(values, str):
        values = [values]
    if len(values) == 0:
        return metadata
    metadata[name] = values
    return metadata


def infer_metric_tags_from_eval_results(eval_results):
    if eval_results is None:
        return {}
    result = {}
    for key in eval_results.keys():
        if key.lower().replace(" ", "_") in METRIC_TAGS:
            result[key.lower().replace(" ", "_")] = key
        elif key.lower() == "rouge1":
            result["rouge"] = key
    return result


def _insert_value(metadata, name, value):
    if value is None:
        return metadata
    metadata[name] = value
    return metadata


def is_hf_dataset(dataset):
    if not is_datasets_available():
        return False

    from datasets import Dataset

    return isinstance(dataset, Dataset)


def _get_mapping_values(mapping):
    result = []
    for v in mapping.values():
        if isinstance(v, (tuple, list)):
            result += list(v)
        else:
            result.append(v)
    return result


@dataclass
class TrainingSummary:
    model_name: str
    language: Optional[Union[str, List[str]]] = None
    license: Optional[str] = None
    tags: Optional[Union[str, List[str]]] = None
    finetuned_from: Optional[str] = None
    tasks: Optional[Union[str, List[str]]] = None
    dataset: Optional[Union[str, List[str]]] = None
    dataset_tags: Optional[Union[str, List[str]]] = None
    dataset_args: Optional[Union[str, List[str]]] = None
    eval_results: Optional[Dict[str, float]] = None
    eval_lines: Optional[List[str]] = None
    hyperparameters: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        # Infer default license from the checkpoint used, if possible.
        if (
            self.license is None
            and not is_offline_mode()
            and self.finetuned_from is not None
            and len(self.finetuned_from) > 0
        ):
            try:
                model_info = HfApi().model_info(self.finetuned_from)
                for tag in model_info.tags:
                    if tag.startswith("license:"):
                        self.license = tag[8:]
            except requests.exceptions.HTTPError:
                pass

    def create_model_index(self, metric_mapping):
        model_index = {"name": self.model_name}

        # Dataset mapping tag -> name
        dataset_names = _listify(self.dataset)
        dataset_tags = _listify(self.dataset_tags)
        dataset_args = _listify(self.dataset_args)
        if len(dataset_args) < len(dataset_tags):
            dataset_args = dataset_args + [None] * (len(dataset_tags) - len(dataset_args))
        dataset_mapping = {tag: name for tag, name in zip(dataset_tags, dataset_names)}
        dataset_arg_mapping = {tag: arg for tag, arg in zip(dataset_tags, dataset_args)}

        task_mapping = {
            task: TASK_TAG_TO_NAME_MAPPING[task] for task in _listify(self.tasks) if task in TASK_TAG_TO_NAME_MAPPING
        }

        if len(task_mapping) == 0 and len(dataset_mapping) == 0:
            return model_index
        if len(task_mapping) == 0:
            task_mapping = {None: None}
        if len(dataset_mapping) == 0:
            dataset_mapping = {None: None}

        model_index["results"] = []

        # One entry per dataset and per task
        all_possibilities = [(task_tag, ds_tag) for task_tag in task_mapping for ds_tag in dataset_mapping]
        for task_tag, ds_tag in all_possibilities:
            result = {}
            if task_tag is not None:
                result["task"] = {"name": task_mapping[task_tag], "type": task_tag}

            if ds_tag is not None:
                result["dataset"] = {"name": dataset_mapping[ds_tag], "type": ds_tag}
                if dataset_arg_mapping[ds_tag] is not None:
                    result["dataset"]["args"] = dataset_arg_mapping[ds_tag]

            if len(metric_mapping) > 0:
                for metric_tag, metric_name in metric_mapping.items():
                    result["metric"] = {
                        "name": metric_name,
                        "type": metric_tag,
                        "value": self.eval_results[metric_name],
                    }

            model_index["results"].append(result)

        return [model_index]

    def create_metadata(self):
        metric_mapping = infer_metric_tags_from_eval_results(self.eval_results)

        metadata = {}
        metadata = _insert_values_as_list(metadata, "language", self.language)
        metadata = _insert_value(metadata, "license", self.license)
        metadata = _insert_values_as_list(metadata, "tags", self.tags)
        metadata = _insert_values_as_list(metadata, "datasets", self.dataset_tags)
        metadata = _insert_values_as_list(metadata, "metrics", list(metric_mapping.keys()))
        metadata["model_index"] = self.create_model_index(metric_mapping)

        return metadata

    def to_model_card(self):
        model_card = ""

        metadata = yaml.dump(self.create_metadata(), sort_keys=False)
        if len(metadata) > 0:
            model_card = f"---\n{metadata}---\n"

        # Now the model card for realsies.
        model_card += AUTOGENERATED_COMMENT

        model_card += f"\n# {self.model_name}\n\n"

        if self.finetuned_from is None:
            model_card += "This model was trained from scratch on "
        else:
            model_card += f"This model is a fine-tuned version of [{self.finetuned_from}](https://huggingface.co/{self.finetuned_from}) on "

        if self.dataset is None:
            model_card += "an unkown dataset."
        else:
            if isinstance(self.dataset, str):
                model_card += f"the {self.dataset} dataset."
            elif isinstance(self.dataset, (tuple, list)) and len(self.dataset) == 1:
                model_card += f"the {self.dataset[0]} dataset."
            else:
                model_card += (
                    ", ".join([f"the {ds}" for ds in self.dataset[:-1]]) + f" and the {self.dataset[-1]} datasets."
                )

        if self.eval_results is not None:
            model_card += "\nIt achieves the following results on the evaluation set:\n"
            model_card += "\n".join([f"- {name}: {_maybe_round(value)}" for name, value in self.eval_results.items()])
        model_card += "\n"

        model_card += "\n## Model description\n\nMore information needed\n"
        model_card += "\n## Intended uses & limitations\n\nMore information needed\n"
        model_card += "\n## Training and evaluation data\n\nMore information needed\n"

        model_card += "\n## Training procedure\n"
        model_card += "\n### Training hyperparameters\n"
        if self.hyperparameters is not None:
            model_card += "\nThe following hyperparameters were used during training:\n"
            model_card += "\n".join([f"- {name}: {value}" for name, value in self.hyperparameters.items()])
            model_card += "\n"
        else:
            model_card += "\nMore information needed\n"

        if self.eval_lines is not None:
            model_card += "\n### Training results\n\n"
            model_card += make_markdown_table(self.eval_lines)
            model_card += "\n"

        model_card += "\n### Framework versions\n\n"
        model_card += f"- Transformers {__version__}\n"
        if is_torch_available():
            import torch

            model_card += f"- Pytorch {torch.__version__}\n"
        if is_datasets_available():
            import datasets

            model_card += f"- Datasets {datasets.__version__}\n"
        if is_tokenizers_available():
            import tokenizers

            model_card += f"- Tokenizers {tokenizers.__version__}\n"

        return model_card

    @classmethod
    def from_trainer(
        cls,
        trainer,
        language=None,
        license=None,
        tags=None,
        model_name=None,
        finetuned_from=None,
        tasks=None,
        dataset_tags=None,
        dataset=None,
        dataset_args=None,
    ):
        # Infer default from dataset
        one_dataset = trainer.train_dataset if trainer.train_dataset is not None else trainer.eval_dataset
        if is_hf_dataset(one_dataset) and (dataset_tags is None or dataset_args is None):
            default_tag = one_dataset.builder_name
            # Those are not real datasets from the Hub so we exclude them.
            if default_tag not in ["csv", "json", "pandas", "parquet", "text"]:
                if dataset_tags is None:
                    dataset_tags = [default_tag]
                if dataset_args is None:
                    dataset_args = [one_dataset.config_name]

        if dataset is None and dataset_tags is not None:
            dataset = dataset_tags

        # Infer default finetuned_from
        if (
            finetuned_from is None
            and hasattr(trainer.model.config, "_name_or_path")
            and not os.path.isdir(trainer.model.config._name_or_path)
        ):
            finetuned_from = trainer.model.config._name_or_path

        # Infer default task tag:
        if tasks is None:
            model_class_name = trainer.model.__class__.__name__
            for task, mapping in TASK_MAPPING.items():
                if model_class_name in _get_mapping_values(mapping):
                    tasks = task

        if model_name is None:
            model_name = Path(trainer.args.output_dir).name

        _, eval_lines, eval_results = parse_log_history(trainer.state.log_history)
        hyperparameters = extract_hyperparameters_from_trainer(trainer)

        return cls(
            language=language,
            license=license,
            tags=tags,
            model_name=model_name,
            finetuned_from=finetuned_from,
            tasks=tasks,
            dataset_tags=dataset_tags,
            dataset=dataset,
            dataset_args=dataset_args,
            eval_results=eval_results,
            eval_lines=eval_lines,
            hyperparameters=hyperparameters,
        )


def parse_log_history(log_history):
    """
    Parse the `log_history` of a Trainer to get the intermediate and final evaluation results.
    """
    idx = 0
    while idx < len(log_history) and "train_runtime" not in log_history[idx]:
        idx += 1

    # If there are no training logs
    if idx == len(log_history):
        idx -= 1
        while idx >= 0 and "eval_loss" not in log_history[idx]:
            idx -= 1

        if idx > 0:
            return None, None, log_history[idx]
        else:
            return None, None, None

    # From now one we can assume we have training logs:
    train_log = log_history[idx]
    lines = []
    training_loss = "No log"
    for i in range(idx):
        if "loss" in log_history[i]:
            training_loss = log_history[i]["loss"]
        if "eval_loss" in log_history[i]:
            metrics = log_history[i].copy()
            _ = metrics.pop("total_flos", None)
            epoch = metrics.pop("epoch", None)
            step = metrics.pop("step", None)
            _ = metrics.pop("eval_runtime", None)
            _ = metrics.pop("eval_samples_per_second", None)
            _ = metrics.pop("eval_steps_per_second", None)
            values = {"Training Loss": training_loss, "Epoch": epoch, "Step": step}
            for k, v in metrics.items():
                if k == "eval_loss":
                    values["Validation Loss"] = v
                else:
                    splits = k.split("_")
                    name = " ".join([part.capitalize() for part in splits[1:]])
                    values[name] = v
            lines.append(values)

    idx = len(log_history) - 1
    while idx >= 0 and "eval_loss" not in log_history[idx]:
        idx -= 1

    if idx > 0:
        eval_results = {}
        for key, value in log_history[idx].items():
            if key.startswith("eval_"):
                key = key[5:]
            if key not in ["runtime", "samples_per_second", "steps_per_second", "epoch", "step"]:
                camel_cased_key = " ".join([part.capitalize() for part in key.split("_")])
                eval_results[camel_cased_key] = value
        return train_log, lines, eval_results
    else:
        return train_log, lines, None


def _maybe_round(v, decimals=4):
    if isinstance(v, float) and len(str(v).split(".")) > 1 and len(str(v).split(".")[1]) > decimals:
        return f"{v:.{decimals}f}"
    return str(v)


def _regular_table_line(values, col_widths):
    values_with_space = [f"| {v}" + " " * (w - len(v) + 1) for v, w in zip(values, col_widths)]
    return "".join(values_with_space) + "|\n"


def _second_table_line(col_widths):
    values = ["|:" + "-" * w + ":" for w in col_widths]
    return "".join(values) + "|\n"


def make_markdown_table(lines):
    """
    Create a nice Markdown table from the results in `lines`.
    """
    if lines is None or len(lines) == 0:
        return ""
    col_widths = {key: len(str(key)) for key in lines[0].keys()}
    for line in lines:
        for key, value in line.items():
            if col_widths[key] < len(_maybe_round(value)):
                col_widths[key] = len(_maybe_round(value))

    table = _regular_table_line(list(lines[0].keys()), list(col_widths.values()))
    table += _second_table_line(list(col_widths.values()))
    for line in lines:
        table += _regular_table_line([_maybe_round(v) for v in line.values()], list(col_widths.values()))
    return table


_TRAINING_ARGS_KEYS = [
    "learning_rate",
    "train_batch_size",
    "eval_batch_size",
    "seed",
]


def extract_hyperparameters_from_trainer(trainer):
    hyperparameters = {k: getattr(trainer.args, k) for k in _TRAINING_ARGS_KEYS}

    if trainer.args.parallel_mode not in [ParallelMode.NOT_PARALLEL, ParallelMode.NOT_DISTRIBUTED]:
        hyperparameters["distributed_type"] = (
            "multi-GPU" if trainer.args.parallel_mode == ParallelMode.DISTRIBUTED else trainer.args.parallel_mode.value
        )
    if trainer.args.world_size > 1:
        hyperparameters["num_devices"] = trainer.args.world_size
    if trainer.args.gradient_accumulation_steps > 1:
        hyperparameters["gradient_accumulation_steps"] = trainer.args.gradient_accumulation_steps

    total_train_batch_size = (
        trainer.args.train_batch_size * trainer.args.world_size * trainer.args.gradient_accumulation_steps
    )
    if total_train_batch_size != hyperparameters["train_batch_size"]:
        hyperparameters["total_train_batch_size"] = total_train_batch_size
    total_eval_batch_size = trainer.args.eval_batch_size * trainer.args.world_size
    if total_eval_batch_size != hyperparameters["eval_batch_size"]:
        hyperparameters["total_eval_batch_size"] = total_eval_batch_size

    if trainer.args.adafactor:
        hyperparameters["optimizer"] = "Adafactor"
    else:
        hyperparameters[
            "optimizer"
        ] = f"Adam with betas=({trainer.args.adam_beta1},{trainer.args.adam_beta2}) and epsilon={trainer.args.adam_epsilon}"

    hyperparameters["lr_scheduler_type"] = trainer.args.lr_scheduler_type.value
    if trainer.args.warmup_ratio != 0.0:
        hyperparameters["lr_scheduler_warmup_ratio"] = trainer.args.warmup_ratio
    if trainer.args.warmup_steps != 0.0:
        hyperparameters["lr_scheduler_warmup_steps"] = trainer.args.warmup_steps
    if trainer.args.max_steps != -1:
        hyperparameters["training_steps"] = trainer.args.max_steps
    else:
        hyperparameters["num_epochs"] = trainer.args.num_train_epochs

    if trainer.args.fp16:
        if trainer.use_amp:
            hyperparameters["mixed_precision_training"] = "Native AMP"
        elif trainer._use_apex:
            hyperparameters["mixed_precision_training"] = f"Apex, opt level {trainer.args.fp16_opt_level}"

    if trainer.args.label_smoothing_factor != 0.0:
        hyperparameters["label_smoothing_factor"] = trainer.args.label_smoothing_factor

    return hyperparameters
