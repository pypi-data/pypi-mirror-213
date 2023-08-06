from typing import Callable
from typing import Iterator
from typing import List

from dataclasses import dataclass

import math
import numpy as np

import tensorflow as tf
import transformers

from nlpipes.data.data_types import Example
from nlpipes.data.data_types import Features


""" The Data Loader to load the data in batch.

A obj:`DataLoader` represents an iterable over data 
samples. It represent a batch generator to get a stream
of data reading from a set of examples. Beyond batches
generation, it also apply all the data transformation
to examples into enncoded features that the model can 
understand.
"""

@dataclass
class DataLoader:
    """ An iterable style Data loader wher data loading 
    order is entirely controlled by the user-defined 
    iterable.
    
    Args
    ----------
    name: 
    examples:
    batch_size:
    data_processor:
    max_length:

    """
    
    name: str
    examples: List[Example] = None
    batch_size: int = None
    data_processor: Callable[[List[Example]], Features] = None
    random_seed: int = 69
    
    def __iter__(self) -> Iterator[Features]:
        """ Iterate over the data, shuffles examples 
        and yield a batches of encoded data at 
        each iteration.	""" 
        batch_examples = list()
        indices = np.random.RandomState(self.random_seed).permutation(
            len(self.examples)
        )
        
        for index in indices:
            example = self.examples[index]
            batch_examples.append(example)
            
            if len(batch_examples) == self.batch_size:
                batch_features = self.data_processor(batch_examples)
                batch_examples.clear()
                yield batch_features
    
    def num_batches(self) -> int:
        """ Number of batches per epoch. """
        return math.ceil(len(self.examples) / self.batch_size)
    
    def num_examples(self) -> int:
        """ Number of dataset examples. """
        return len(self.examples)
    