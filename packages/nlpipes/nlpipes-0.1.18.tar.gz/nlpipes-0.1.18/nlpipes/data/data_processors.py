from typing import Callable
from typing import List

from dataclasses import dataclass

import copy

import numpy as np
import tensorflow as tf

from transformers import (
    PretrainedConfig,
    PreTrainedTokenizer,
    AutoTokenizer,
)

from nlpipes.data.data_types import Example
from nlpipes.data.data_types import Features


""" The data processor classes.

The data processor encapsulates all the transformations
needed to encode input examples into features to be used
as input batch by the model. """


@dataclass
class MLMProcessor:
    """ 
    Data processor for Masked Language Modeling.
    By default, we assign a 15% probability for 
    each token of a sequence to be included in
    the mask. Among the tokens in the mask:
     - 80% are replaced with [MASK] token
     - 10% are replaced with some random token
     - 10% are kept unchanged.
    The special tokens i.e., [CLS], [SEP], [PAD] 
    are excluded from the mask, as we don’t want 
    to predict them during training.
    Inputs are dynamically padded to the maximum 
    length of a batch if they are not all of the 
    same length
    
    Args
    ----------

    tokenizer:
        The tokenizer used for encoding the data.

    config:
        The configuration of the model.
    """
    
    name: str = 'MaskedLanguageModelingProcessor'
    tokenizer: PreTrainedTokenizer = None
    config: PretrainedConfig = None
    max_length: int = 128
    mlm_prob: float = 0.15
    mask_prob: float = 0.80
    rand_prob: float = 0.10
    idem_prob: float = 0.10
    
    def __call__(self, 
                 examples: List[Example],
                ) -> Features:
        
        texts = [example.text for example in examples]
        
        # We first tokenize the input sequence
        inputs = self.tokenizer(
            texts,
            add_special_tokens=True,
            padding=True,
            truncation=True,
            max_length=self.max_length,
            is_split_into_words=False,
            return_attention_mask=True,
            return_token_type_ids=True,
            return_tensors='tf',
        )
        
        # The target label is simply the input_ids
        labels = tf.identity(inputs.input_ids)
        
        # Random selection of tokens to be masked. 
        mask, mask_details = self.create_mask(
            inputs=inputs.input_ids,
            excluded=self.tokenizer.all_special_ids,
            mlm_prob=self.mlm_prob,
            mask_prob=self.mask_prob,
            rand_prob=self.rand_prob,
            idem_prob=self.idem_prob,
        )
        
        # 80% of the time, replace with the [MASK] token
        inputs['input_ids'] = self.apply_mask(
            inputs=inputs.input_ids,
            mask=mask_details['masked'],
            mask_id=self.tokenizer.mask_token_id,
        )
        
        # 10% of the time, replace with random token
        vocab_size = len(self.tokenizer)
        random_token_ids = tf.random.uniform(
            shape=inputs.input_ids.shape, 
            maxval=vocab_size,
            dtype=inputs.input_ids.dtype,
        )
        
        inputs['input_ids'] = self.apply_mask(
            inputs=inputs.input_ids,
            mask=mask_details['random'],
            mask_id=random_token_ids,
        )
        
        # Unchanged The rest of the time (10% of the time).
        
        # Only the `masked` tokens are predicted during training.
        labels = self.apply_mask(
            inputs=labels,
            mask=~mask,
            mask_id=-100,
        )
        
        inputs['label'] = tf.one_hot(
            [label for label in labels],
            depth=vocab_size
        )
        
        input_features = Features(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            token_type_ids=inputs['token_type_ids'],
            label=inputs['label'],
        )
        
        return input_features
    
    def create_mask(
        self,
        inputs: tf.Tensor,
        mlm_prob: float,
        mask_prob: float,
        rand_prob: float,
        idem_prob: float,
        excluded: tf.Tensor,  
    ) -> tf.Tensor:
        """ Create the mask used for the masked 
        language modeling."""
        
        uniform = tf.random.uniform(inputs.shape, maxval=1)
        
        mask_treshold = mlm_prob * mask_prob
        rand_treshold = mlm_prob * (mask_prob + rand_prob)

        mask = tf.math.logical_and(
            uniform <= mlm_prob, 
            ~np.isin(inputs, excluded),
        )
        
        masked = tf.math.logical_and(
            uniform <= mask_treshold, 
            ~np.isin(inputs, excluded),
        )
        
        random = tf.math.logical_and(
            uniform > mask_treshold,
            uniform <= rand_treshold,
            ~np.isin(inputs, excluded),
        )
        
        mask_details = {}
        mask_details['masked'] = masked
        mask_details['random'] = random
        
        return mask, mask_details
    
    def apply_mask(
        self,
        inputs: tf.Tensor,
        mask: tf.Tensor,
        mask_id: int,
    ) -> tf.Tensor:
        """ Apply the mask to the given inputs """
        
        input_masked = tf.where(
            condition=mask,
            x=mask_id,
            y=inputs,
        )
        
        return input_masked


@dataclass
class SingleLabelProcessor:
    """
    Data Processor for single-label sequence classification.
    Inputs are dynamically padded to the maximum 
    length of a batch if they are not all of the 
    same length.
    
    Args
    ----------

    tokenizer (transformers.PreTrainedTokenizer):
        The tokenizer used for encoding the data.

    config (transformers.PreTrainedCOnfig):
        The configuration of the model.
    """
    
    name: str = 'SingleLabelClassificationProcessor'
    tokenizer: PreTrainedTokenizer = None
    config: PretrainedConfig = None
    max_length: int = None
    
    def __call__(self, 
                 examples: List[Example],
                ) -> Features:
        
        texts = [example.text for example in examples]
        
        inputs = self.tokenizer(
            texts,
            add_special_tokens=True,
            padding=True,
            truncation=True,
            max_length=self.max_length,
            is_split_into_words=False,
            return_attention_mask=True,
            return_token_type_ids=True,
            return_tensors='tf',
        )
        
        inputs['label'] = tf.one_hot(
            [example.label for example in examples],
            depth=self.config.num_labels
        )
        
        input_features = Features(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            token_type_ids=inputs['token_type_ids'],
            label=inputs['label'],
        )
        
        return input_features


@dataclass(frozen=True)
class MultiLabelProcessor:
    """
    Data Processor for multi-label sequence classification.
    Inputs are dynamically padded to the maximum length of a
    batch if they are not all of the same length.
    
    Args
    ----------

    tokenizer (transformers.PreTrainedTokenizer):
        The tokenizer used for encoding the data.

    config (transformers.PreTrainedCOnfig):
        The configuration of the model.
    """
    
    name: str = 'MultiLabelClassificationProcessor'
    tokenizer: PreTrainedTokenizer = None
    config: PretrainedConfig = None
    max_length: int = None
    
    def __call__(self, 
                 examples: List[Example],
                ) -> Features:
        
        texts = [example.text for example in examples]
        
        inputs = self.tokenizer(
            texts,
            add_special_tokens=True,
            padding=True,
            truncation=True,
            max_length=self.max_length,
            is_split_into_words=False,
            return_attention_mask=True,
            return_token_type_ids=True,
            return_tensors='tf',
        )
        
        labels = [example.label for example in examples]
        # onehot encoding of empty list yield error
        labels = [[-1] if not l else l for l in labels]
        
        onehot_labels = tf.one_hot(
            tf.ragged.constant(labels),
            depth=self.config.num_labels,
        )
        
        inputs['label'] = tf.reduce_max(onehot_labels, axis=1)
        
        input_features = Features(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            token_type_ids=inputs['token_type_ids'],
            label=inputs['label'],
        )
        
        return input_features

@dataclass
class ClassLabelDataProcessor:
    """
    Data Processor for class-label sequence classification.
    Inputs are dynamically padded to the maximum 
    length of a batch if they are not all of the 
    same length.
    
    Args
    ----------

    tokenizer (transformers.PreTrainedTokenizer):
        The tokenizer used for encoding the data.

    config (transformers.PreTrainedCOnfig):
        The configuration of the model.
    """
    
    name: str = 'ClassLabelDataProcessor'
    tokenizer: PreTrainedTokenizer = None
    config: PretrainedConfig = None
    max_length: int = None
    
    def __call__(self, examples: List[Example]) -> Features:
        
        texts = [(example.text, example.aspect)
                 for example in examples]
        
        inputs = self.tokenizer(
            texts,
            add_special_tokens=True,
            padding=True,
            truncation=True,
            max_length=self.max_length,
            is_split_into_words=False,
            return_attention_mask=True,
            return_token_type_ids=True,
            return_tensors='tf',
        )
        
        inputs['label'] = tf.one_hot(
            [example.label for example in examples],
            depth=self.config.num_labels
        )
        
        input_features = Features(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            token_type_ids=inputs['token_type_ids'],
            label=inputs['label'],
        )
        
        return input_features
    