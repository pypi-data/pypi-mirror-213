from dataclasses import dataclass
from typing import List
from collections import Counter

import tensorflow as tf
import tensorflow_addons as tfa

import numpy as np
import math


@dataclass
class SCELoss():
    """ Computes the softmax cross-entropy """

    def __call__(self, labels: tf.Tensor, logits: tf.Tensor):
        softmax = tf.nn.softmax_cross_entropy_with_logits
        return softmax(labels, logits, axis=-1)
    
    
@dataclass
class SFCELoss():
    """ Computes the focal sigmoid cross-entropy """
    alpha: float=0.25
    gamma: float=2.0

    def __call__(self, labels: tf.Tensor, logits: tf.Tensor):
        sigmoid_focal = tfa.losses.sigmoid_focal_crossentropy
        return sigmoid_focal(
            labels, logits, 
            alpha=tf.constant(self.alpha), 
            gamma=tf.constant(self.gamma), 
            from_logits=True,
        )

    
@dataclass
class WCELoss():
    """ Computes the weighted sigmoid cross-entropy """
    class_weights: List[float]
    
    def __call__(self, labels: tf.Tensor, logits: tf.Tensor):
        weighted_sigmoid = tf.nn.weighted_cross_entropy_with_logits
        
        if self.class_weights:
            batch_size, n_classes = logits.get_shape()
            class_weights = tf.constant(self.class_weights)
            class_weights = tf.expand_dims(class_weights, axis=0)
            class_weights = tf.tile(class_weights, [batch_size, 1])
        else:
            class_weights = tf.constant(1.0)
                                        
        return weighted_sigmoid(labels, logits, class_weights)
    