import logging

from typing import Iterable
from typing import List

from dataclasses import dataclass

import tensorflow as tf

from nlpipes.callbacks.callbacks import Callback
from nlpipes.callbacks.callbacks import CallbackList
from nlpipes.data.data_types import Features


logger = logging.getLogger('__name__')

@dataclass
class Trainer():
    
    """ The trainer is written from scratch. It consists in 
    a custom training loop that trigger a set of `Callback`
    functions at given stages of the training procedure, 
    such as when:
     - the training/testing starts.
     - the training/testing ends.
     - a train/test epoch starts
     - a train/test epoch ends.
     - a train/test batch starts.
     - a train/test batch ends.
    """
    
    callbacks: List[Callback]
    
    def fit(
        self,
        train_stream: Iterable[Features],
        test_stream: Iterable[Features],
        epochs: int,
    ):
        
        callbacks = CallbackList(self.callbacks)
        
        callbacks.on_train_begin()

        for epoch in range(epochs):
            
            callbacks.on_epoch_begin(epoch)
            for step, batch in enumerate(train_stream):
                callbacks.on_train_batch_begin(step, batch)
                callbacks.on_train_batch_end(step, batch)

            if test_stream:
                callbacks.on_test_begin()
                for step, batch in enumerate(test_stream):
                    callbacks.on_test_batch_begin(step, batch)
                    callbacks.on_test_batch_end(step, batch)

                callbacks.on_test_end()

            callbacks.on_epoch_end(epoch)
            
        callbacks.on_train_end()
        