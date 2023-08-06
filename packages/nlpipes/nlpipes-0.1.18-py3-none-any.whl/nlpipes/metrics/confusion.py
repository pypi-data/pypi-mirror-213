from typing import Union
from typing import Optional

from typeguard import typechecked

import numpy as np
import tensorflow as tf


class ConfusionMatrix(tf.metrics.Metric):
    """ Compute the confusion matrix for single-label
    classifier. 
    
    Args:
    ---------
    num_classes: (int): the number of predictions labels
    name: (Optional) name of the metric instance.
    dtype: (Optional) data type of the metric result.
    """
    
    @typechecked
    def __init__(
        self, 
        num_classes: int,
        name: str = "multiclass_confusion_matrix",
        dtype = tf.dtypes.int32,
    ):
        super().__init__(name=name, dtype=dtype)
        self.num_classes = num_classes
        self.confusion_matrix = self.add_weight(
            'confusion_matrix',
            shape=[num_classes, num_classes],
            initializer='zeros',
            dtype=self.dtype,
        )

    def update_state(self, y_true, y_pred):
        """ Accumulates statistics for the metric. """
        batch = tf.math.confusion_matrix(
            y_true, y_pred,
            num_classes=self.num_classes,
            dtype=self.dtype,
        )
        self.confusion_matrix.assign_add(batch)

    def result(self):
        """ Return the metric result"""
        return self.confusion_matrix


class MultiLabelConfusionMatrix(tf.metrics.Metric):
    """ Computes the confusion matrix for multi-labels 
    classifier. Every class has a dedicated 
    matrix of shape `(2, 2)` that contains:
    - true negatives in cell `(0,0)`
    - false positives in cell `(0,1)`
    - false negatives in cell `(1,0)`
    - true positives in cell `(1,1)`
    
    Args:
    ---------
    num_classes: (int): the number of predictions labels
    name: (Optional) name of the metric instance.
    dtype: (Optional) data type of the metric result.
    """

    @typechecked
    def __init__(
        self,
        num_classes: int,
        name: str = "multilabel_confusion_matrix",
        dtype = tf.dtypes.int32,
        **kwargs,
    ):
        super().__init__(name=name, dtype=dtype)
        self.num_classes = num_classes
        self.true_positives = self.add_weight(
            "true_positives",
            shape=[self.num_classes],
            initializer="zeros",
            dtype=self.dtype,
        )
        self.false_positives = self.add_weight(
            "false_positives",
            shape=[self.num_classes],
            initializer="zeros",
            dtype=self.dtype,
        )
        self.false_negatives = self.add_weight(
            "false_negatives",
            shape=[self.num_classes],
            initializer="zeros",
            dtype=self.dtype,
        )
        self.true_negatives = self.add_weight(
            "true_negatives",
            shape=[self.num_classes],
            initializer="zeros",
            dtype=self.dtype,
        )

    def update_state(self, y_true, y_pred):
        """ Accumulates statistics for the metric. """
        y_true = tf.cast(y_true, self.dtype)
        y_pred = tf.cast(y_pred, self.dtype)
        
        pred_sum = tf.math.count_nonzero(y_pred, 0)
        true_sum = tf.math.count_nonzero(y_true, 0)
        
        y_true_negative = tf.math.not_equal(y_true, 1)
        y_pred_negative = tf.math.not_equal(y_pred, 1)
        
        true_positive = tf.math.count_nonzero(y_true * y_pred, 0)
        false_positive = pred_sum - true_positive
        false_negative = true_sum - true_positive
        true_negative = tf.math.count_nonzero(
            tf.math.logical_and(y_true_negative, y_pred_negative), 
            axis=0,
        )

        self.true_positives.assign_add(tf.cast(true_positive, self.dtype))
        self.false_positives.assign_add(tf.cast(false_positive, self.dtype))
        self.false_negatives.assign_add(tf.cast(false_negative, self.dtype))
        self.true_negatives.assign_add(tf.cast(true_negative, self.dtype))

    def result(self):
        """ Returns the metric value. """
        flat_confusion_matrix = tf.convert_to_tensor(
            [
                self.true_negatives,
                self.false_positives,
                self.false_negatives,
                self.true_positives,
            ]
        )
        
        confusion_matrix = tf.reshape(
            tf.transpose(flat_confusion_matrix), [-1, 2, 2]
        )

        return confusion_matrix
    
    def reset_state(self):
        """ Resets all of the metric state variables. """
        reset_value = np.zeros(self.num_classes, dtype=np.int32)
        tf.keras.backend.batch_set_value(
            [(v, reset_value) for v in self.variables]
        )
    
    
def hamming_loss_with_logits(
    y_true: tf.Tensor,
    y_pred: tf.Tensor,
    threshold: Union[tf.Tensor, None],
) -> tf.Tensor:
    """  Computes the Hamming loss """
    
    y_pred = tf.sigmoid(tf.cast(y_pred, tf.float32))
    
    if threshold is None:
        threshold = tf.reduce_max(y_pred, axis=-1, keepdims=True)
        y_pred = tf.logical_and(
            y_pred >= threshold, 
            tf.abs(y_pred) > 1e-12,
        )
    else:
        y_pred = y_pred > threshold

    y_true = tf.cast(y_true, tf.int32)
    y_pred = tf.cast(y_pred, tf.int32)
    
    mismatches = tf.cast(
        tf.math.count_nonzero(y_true - y_pred, axis=-1),
        tf.float32,
    )
     
    return 1 - (mismatches / y_true.get_shape()[-1])
    
    
class HammingLoss(tf.metrics.MeanMetricWrapper):
    """ Compute the average Hamming loss between y_true and y_pred.
    The Hamming loss is the fraction of wrongly predicted labels to
    the total number of labels.
    
    Args:
    ----------
        y_true: actual target value.
        y_pred: predicted target value.
        threshold: Elements of `y_pred` greater than threshold
            are converted to be 1, and the rest 0. If threshold
            is None, the argmax is converted to 1, and the rest 0.
    Returns:
        hamming loss: float.
    """

    @typechecked
    def __init__(
        self,
        name: str = "hamming_loss",
        threshold: Union[tf.Tensor, float] = None,
        dtype = tf.float32,
        **kwargs,
    ):
        super().__init__(
            fn=hamming_loss_with_logits, 
            name=name, 
            dtype=dtype,
            threshold=threshold,
        )

        
class F1_Score(tf.metrics.Metric):
    """ """
    def __init__(
        self, 
        name: str ='f1_score',
        thresholds:float = None,
        top_k:int = None,
        dtype = tf.float32,
        **kwargs
    ):
        super().__init__(name=name, **kwargs)
        self.f1 = self.add_weight(name='f1', initializer='zeros')
        self.precision_fn = tf.metrics.Precision(
            thresholds=thresholds,
            top_k=top_k,
        )
        self.recall_fn = tf.metrics.Recall(
            thresholds=thresholds,
            top_k=top_k,
        )

    def update_state(self, y_true, y_pred, sample_weight=None):
        p = self.precision_fn(y_true, y_pred)
        r = self.recall_fn(y_true, y_pred)
        self.f1.assign(2 * ((p * r) / (p + r + 1e-6)))

    def result(self):
        return self.f1

    def reset_states(self):
        self.precision_fn.reset_states()
        self.recall_fn.reset_states()
        self.f1.assign(0)