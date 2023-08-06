from dataclasses import dataclass
from itertools import chain
from typing import Iterable
from typing import List
from typing import Optional

import numpy as np

from nlpipes.data.data_types import Example


@dataclass
class TrainTestSplitter:
    """ Splits input data into training/test set """
        
    train_frac: float = None
    test_frac: float = None
    shufffle: bool = True

    def __call__(self, examples: List[Example]
                ) -> Iterable:
        """  """
        
        n_examples = len(examples)
        n_train = int(np.ceil(n_examples*self.train_frac))
        n_test = int(np.ceil(n_examples*self.test_frac))
        n_samples = n_train + n_test
        
        if self.shufffle:
            order = np.random.permutation(n_examples)
            train_indices = order[n_train:]
            test_indices = order[:n_test]
        else:
            train_indices = np.arange(n_train)
            test_indices = np.arange(n_train, n_samples)
        
        train_examples = self._indexing(examples, train_indices)
        test_examples = self._indexing(examples, test_indices) 
            
        return train_examples, test_examples

    def _indexing(self, examples, indices):
        """  """
        
        if hasattr(examples, 'shape'):
            return examples[indices]
        
        return [examples[idx] for idx in indices]
    