import logging
from enum import IntEnum

from collections import OrderedDict

from dataclasses import dataclass
from dataclasses import fields
from dataclasses_json import dataclass_json

from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import NewType
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import numpy as np
import tensorflow as tf

from transformers import (
    PreTrainedModel,
    PreTrainedTokenizer,
    PretrainedConfig,
)

from nlpipes.pipelines.base_pipeline import Pipeline


Document = NewType("Document", str)
Corpus = NewType("Corpus", Sequence[Document])
Token = NewType("Token", str)
Sequence = NewType("Sequence", str)
AllLabel = NewType("Label", str)


@dataclass
class Task:
    """ """
    pipeline: Pipeline
    model: PreTrainedModel
    tokenizer: PreTrainedTokenizer
    config: PretrainedConfig 
    
    
@dataclass
class Example:
    """ A single example used to create a classifier.
        
    Args
    ----------
        text: raw input text.
        aspects: (optional): to be specified when the labels is 
                 toward a specific aspect in the input text.
        label: (optional) target label.
    """
    text: str
    label: Optional[str] = None
    aspect: Optional[str] = None
    alignment: Optional[int] = None  
    
@dataclass
class Tokens:
    """ A set of tokens to be encoded to be used
    as input by the transformer model.
    
    Args
    ----------
        words: words split into words using a 
            `whitespace` tokenizer.
        subwords: words split into subwords
             using a model specific tokenizer.
        subwords_plus: subwords with the additionnal 
             special tokens '[CLS]' and '[SEP]'.
    """
    words: List[str]
    subwords: List[str]
    subwords_plus: List[str]
    
    
@dataclass
class Features:
    """ A set of features expected as input by a transformer model.
    
    Args
    ----------
        input_ids: indices of input sequence tokens in the vocabulary.
        attention_mask: mask to avoid performing attention on padding 
                        token indices. Mask values selected in `[0, 1]`.
                        Usually `1` for tokens that are NOT MASKED and 
                        `0` for MASKED (padded) tokens.
        token_type_ids: segment token indices to indicate first and 
                        second portions of the inputs. Only some models 
                        use them.
        label: (Optional) the target label corresponding to the input.
    """
    input_ids: tf.Tensor
    attention_mask: tf.Tensor = None
    token_type_ids: tf.Tensor = None
    label: Optional[tf.Tensor] = None
    
    
@dataclass
class Prediction:
    """ The model predictions 

    Args
    ----------
        label:
        confidence:
    """
    label: tf.Tensor
    confidence: tf.Tensor
    
@dataclass_json  
@dataclass
class Classification:
    """ The final outcome after post-processing the 
    model outputs

    Args
    ----------
        text:
        prediction:
        confidence:
    """
    text: List[str]
    prediction: List[str]
    confidence: List[str]
    
    
@dataclass
class TFSequenceClassifierOutput():
    """ The model outputs for a single example.
    
    Args
    ----------
        logits: the logits scores outputed by the
                classification head.
        hidden_states: hidden-states of the model at the output of each
                layer plus the initial embedding outputs.
        attentions: attentions weights after the attention softmax, used
                to compute the weighted average in the self-attention 
                heads.
    """
    logits: tf.Tensor
    hidden_states: Optional[Tuple[tf.Tensor]]
    attentions: Optional[Tuple[tf.Tensor]]


@dataclass
class TFSequenceClassifierBatchOutput(TFSequenceClassifierOutput):
    loss: tf.Tensor
    
    
@dataclass
class LabelsMapping:
    """ The labels used for classification tasks. """
    def __init__(self, labels):
        for idx, label in enumerate(labels):
            setattr(self, label, idx)
    def id2label(self):
        return {idx:label 
                for label, idx in self.__dict__.items()}
    def label2id(self):
        return {label:idx 
                for label, idx  in self.__dict__.items()}
    def num_labels(self):
        return len(self.__dict__)
    
    
# Source: https://github.com/huggingface/transformers
# TODO: clean unrelevant code
@dataclass
class ModelOutput(OrderedDict):
    """
    Base class for all model outputs as dataclass. Has a `__getitem__` 
    that allows indexing by integer or slice (like a tuple) or strings
    (like a dictionary) that will ignore the `None` attributes. Otherwise
    behaves like a regular python dictionary.
    <Tip warning={true}>
    You can't unpack a `ModelOutput` directly. Use the 
    [`~utils.ModelOutput.to_tuple`]	method to convert it to a tuple before.
    </Tip>
    """

    def __post_init__(self):
        class_fields = fields(self)

        # Safety and consistency checks
        if not len(class_fields):
            raise ValueError(f"{self.__class__.__name__} has no fields.")
        if not all(field.default is None for field in class_fields[1:]):
            raise ValueError(f"{self.__class__.__name__} should not have more than one required field.")

        first_field = getattr(self, class_fields[0].name)
        other_fields_are_none = all(getattr(self, field.name) is None for field in class_fields[1:])

        if other_fields_are_none and not isinstance(first_field, tf.Tensor):
            if isinstance(first_field, dict):
                iterator = first_field.items()
                first_field_iterator = True
            else:
                try:
                    iterator = iter(first_field)
                    first_field_iterator = True
                except TypeError:
                    first_field_iterator = False

            if first_field_iterator:
                for element in iterator:
                    if (
                        not isinstance(element, (list, tuple))
                        or not len(element) == 2
                        or not isinstance(element[0], str)
                    ):
                        break
                    setattr(self, element[0], element[1])
                    if element[1] is not None:
                        self[element[0]] = element[1]
            elif first_field is not None:
                self[class_fields[0].name] = first_field
        else:
            for field in class_fields:
                v = getattr(self, field.name)
                if v is not None:
                    self[field.name] = v

    def __delitem__(self, *args, **kwargs):
        raise Exception(f"You cannot use ``__delitem__`` on a {self.__class__.__name__} instance.")

    def setdefault(self, *args, **kwargs):
        raise Exception(f"You cannot use ``setdefault`` on a {self.__class__.__name__} instance.")

    def pop(self, *args, **kwargs):
        raise Exception(f"You cannot use ``pop`` on a {self.__class__.__name__} instance.")

    def update(self, *args, **kwargs):
        raise Exception(f"You cannot use ``update`` on a {self.__class__.__name__} instance.")

    def __getitem__(self, k):
        if isinstance(k, str):
            inner_dict = {k: v for (k, v) in self.items()}
            return inner_dict[k]
        else:
            return self.to_tuple()[k]

    def __setattr__(self, name, value):
        if name in self.keys() and value is not None:
            super().__setitem__(name, value)
        super().__setattr__(name, value)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        super().__setattr__(key, value)

    def to_tuple(self) -> Tuple[Any]:
        """ Convert self to a tuple containing all the attributes/keys that
        are not `None`. """
        return tuple(self[k] for k in self.keys())


@dataclass
class TFBaseModelOutput(ModelOutput):
    """ Base class for model's outputs, with potential hidden states and
    attentions. """

    last_hidden_state: tf.Tensor = None
    hidden_states: Optional[Tuple[tf.Tensor]] = None
    attentions: Optional[Tuple[tf.Tensor]] = None


@dataclass
class TFBaseModelOutputWithPooling(ModelOutput):
    """ Base class for model's outputs that also contains a pooling of 
    the last hidden states. """

    last_hidden_state: tf.Tensor = None
    pooler_output: tf.Tensor = None
    hidden_states: Optional[Tuple[tf.Tensor]] = None
    attentions: Optional[Tuple[tf.Tensor]] = None
