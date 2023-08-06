import os
import logging
import importlib
import inspect

from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
)

import tensorflow as tf
import transformers

from tensorflow.python.client import device_lib

from transformers import (
    TFPreTrainedModel,
    TFAutoModelForMaskedLM,
    TFAutoModelForSequenceClassification,
    TFBertForSequenceClassification,
    BertTokenizerFast,
    AutoModel,
    AutoTokenizer,
    AutoConfig, 
)

from nlpipes.pipelines.base_pipeline import Pipeline
from nlpipes.pipelines.language_modeling_pipelines import PipelineForMaskedLanguageModeling
from nlpipes.pipelines.mono_label_classification_pipelines import PipelineForMonoLabelSequenceClassification
from nlpipes.pipelines.multi_label_classification_pipelines import PipelineForMultiLabelSequenceClassification
from nlpipes.pipelines.class_label_classification_pipelines import PipelineForClassLabelSequenceClassification
from nlpipes.models.classification_models import TFAdaptedBertForSequenceClassification
from nlpipes.models.classification_models import AdaptedBertForSequenceClassification
from nlpipes.configurations.bert_config import AdaptedBertConfig
from nlpipes.data.data_types import Task
from nlpipes.data.data_types import LabelsMapping

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel('ERROR')

logger = logging.getLogger('__name__')


SUPPORTED_TASKS = {
  "language-modeling": {
      "pipeline": PipelineForMaskedLanguageModeling,
      "models": {
          "default": TFAutoModelForMaskedLM,
          "adapters": None,
      },
      "tokenizers": {
          "default": AutoTokenizer,
          "adapters": AutoTokenizer,
      },
      "configs": {
          "default": AutoConfig,
          "adapters": AdaptedBertConfig,
      },
  },
  "mono-label-classification": {
      "pipeline": PipelineForMonoLabelSequenceClassification,
      "models": {
          "default": TFAutoModelForSequenceClassification,
          "adapters": TFAdaptedBertForSequenceClassification,
      },
      "tokenizers": {
          "default": AutoTokenizer,
          "adapters": AutoTokenizer,
      },
      "configs": {
          "default": AutoConfig,
          "adapters": AdaptedBertConfig,
      },
  },
  "multi-label-classification": {
      "pipeline": PipelineForMultiLabelSequenceClassification,
      "models": {
          "default": TFAutoModelForSequenceClassification,
          "adapters": TFAdaptedBertForSequenceClassification,
      },
      "tokenizers": {
          "default": AutoTokenizer,
          "adapters": AutoTokenizer,
      },
      "configs": {
          "default": AutoConfig,
          "adapters": AdaptedBertConfig,
      },
  },
  "class-label-classification": {
      "pipeline": PipelineForClassLabelSequenceClassification,
      "models": {
          "default": TFAutoModelForSequenceClassification,
          "adapters": TFAdaptedBertForSequenceClassification,
      },
      "tokenizers": {
          "default": AutoTokenizer,
          "adapters": AutoTokenizer,
      },
      "configs": {
          "default": AutoConfig,
          "adapters": AdaptedBertConfig,
      },
  },
}


def Model(
    name_or_path: TFPreTrainedModel = None,
    task: str = None,
    all_labels: Optional[List] = None,
    from_pt:bool = False,
    **model_kwargs
) -> Pipeline:

    """ The `Model` offers an abstraction to run several text 
    classification tasks. Which task the model should learn 
    is determined automatically based on the user-supplied
    target task.

    Args
    ----------
    task(str):
          A task name that determines which task the model 
          should learn e.g., `single_label` classification`.
            
    model(str):
          A path or name of the model that should be used.
          It can be:
            - The path of a model available in a local repo.
            - The name of a model available in the Huggingface
              model repo.
    
    all_labels (List[str]): 
          A list of all labels. Needed as some labels may be 
          not present in the dataset.
    """

    try:
        pipeline = get_pipeline_from_task(
            task=task, 
            name_or_path=name_or_path, 
            all_labels=all_labels,
            customization_tag='#',
            from_pt=from_pt,
        )

        return pipeline

    except EnvironmentError as error:
        message = "The pipeline could not be loaded."
        logger.error(message)
        raise error


def get_pipeline_from_task(
    task:str, 
    name_or_path:str,
    all_labels:List[str],
    customization_tag:str,
    from_pt:bool,
) -> Pipeline:
    """ Create a task specific pipeline. """
    
    if task:
        TASK = SUPPORTED_TASKS[task]
        PIPELINE = TASK["pipeline"]
    
        if customization_tag in name_or_path:
            customization = name_or_path.split(customization_tag, 1)[1]
            MODEL = TASK["models"][customization]
            TOKENIZER = TASK["tokenizers"][customization]
            CONFIG = TASK["configs"][customization]
            name_or_path = name_or_path.replace(
                customization_tag+customization, ""
            )
        else:
            MODEL = TASK["models"]["default"]
            TOKENIZER = TASK["tokenizers"]["default"]
            CONFIG = TASK["configs"]["default"]

        config = CONFIG.from_pretrained(name_or_path)
        
        if all_labels:
            all_labels = sorted(all_labels)
            config.id2label=LabelsMapping(all_labels).id2label()
            config.label2id=LabelsMapping(all_labels).label2id()
            config.num_labels=LabelsMapping(all_labels).num_labels()
            
        if not config.finetuning_task:
            config.finetuning_task=task

        tokenizer = TOKENIZER.from_pretrained(name_or_path)
        model = MODEL.from_pretrained(
            name_or_path, 
            config=config, 
            from_pt=from_pt,
        )
        
        pipeline = PIPELINE(
            model=model,
            tokenizer=tokenizer,
            config=config,
        )
    
    else:
        config = AutoConfig.from_pretrained(name_or_path)
        PIPELINE = SUPPORTED_TASKS[config.finetuning_task]['pipeline']
        
        MODEL = get_model_from_config(config)
        
        model = MODEL.from_pretrained(name_or_path)
        tokenizer = AutoTokenizer.from_pretrained(name_or_path)
        
        pipeline = PIPELINE(
            model=model,
            tokenizer=tokenizer,
            config=config,
        )


    return pipeline


def get_model_from_config(config):
    """ Get the model class from the model configuration file.
    Note : we use a temporary dirty workaround to bypass an issue in 
    the model architecture name stored in the saved config """
    
    model_name = config.architectures[0]
    models_module_name = 'nlpipes.models.classification_models'
    models_module = importlib.import_module(models_module_name)
    available_models = [
        model[0] for model in inspect.getmembers(models_module)
    ]
    
    if model_name in available_models:
        model_class = getattr(models_module, model_name)
    else:
        model_class = getattr(transformers, 'TF' + model_name)
    return model_class


def get_available_tasks() -> List[str]:
    """ Get a list of all available tasks."""
    return list(SUPPORTED_TASKS.keys())


def get_available_gpus():
    local_device_protos = device_lib.list_local_devices()
    return [
        device.name for device in local_device_protos 
        if device.device_type == 'GPU'
    ]
