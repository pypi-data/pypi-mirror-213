from typing import Any
from typing import Callable
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple

from itertools import chain
from collections import namedtuple
from collections import Counter

import math
import numpy as np
import tensorflow as tf

from transformers import PretrainedConfig

from sklearn.preprocessing import MultiLabelBinarizer

from nlpipes.data.data_types import Example


def chunk() -> Callable[[str], List[str]]:
    """  Chunk text into shorter sequences. """  
    
    def chunk_into_sentences(texts: str) -> List[str]:
        """ Chunk text with regular-expressions """
        on_regex = '(?<=[^A-Z].[.?]) +(?=[A-Z])'
        sequences = [re.split(on_regex, text) for text in texts]
        sequences = [sequence for sublist in sequences for sequence in sublist]
        return sequences
    
    def chunk_into_whatever(texts: str) -> List[str]:
        raise NotImplementedError
    
    chunk_fn = chunk_into_sentences

    return chunk_fn


def create_examples(texts: List[str]) -> List[Example]:
    """ Serialize each input raw data into unlabelled examples. """
    examples = [Example(text) for text in texts]
    return examples


def create_monolabel_examples(
    texts: List[str],
    labels: Optional[List[str]],
    config: PretrainedConfig,
   ) -> List[Example]:
    """ Serialize each input raw data into single label examples. """
    labels = [config.label2id[label] for label in labels] 
    examples = [
        Example(text, label=label)
        for text, label in zip(texts, labels)
    ]        
    return examples


def create_multilabel_examples(
    texts: List[str],
    labels: Optional[List[List[str]]],
    config: PretrainedConfig,
   ) -> List[Example]:
    """ Serialize each input raw data into multiple label examples. """
    labels = [
        [config.label2id[label] for label in sub_labels]
        for sub_labels in labels
    ]
    examples = [
        Example(text, label=label)
        for text, label in zip(texts, labels)
    ]
    return examples

        
def create_classlabel_examples(
    texts: List[str],
    labels: Optional[List[List[List[str]]]],
    config: PretrainedConfig,
   ) -> List[Example]:
    """ Serialize each input raw data into class label examples. """
    
    def generate_classlabel_example(
        text: str,
        labels: List[Any],
        config: PretrainedConfig,
    ):
        label2id = {
            'negative': 0,
            'neutral': 1,
            'positive': 2,
        }

        aspects = [label[0] for label in labels]
        polarities = [label[1] for label in labels]

        for i, aspect in enumerate(aspects):
            aspect = aspect.lower()
            sentiment = polarities[i]
            label = label2id[sentiment]
            yield Example(
                text=text, 
                aspect=aspect, 
                label=label,
            )
    
    data = namedtuple('data', 'x y')
    data_raw = data(texts, labels)
    
    examples = [
        example
        for x, y in zip(*data_raw)
        for example in generate_classlabel_example(x, y, config)
    ]
    return examples
    

def split_examples(
    examples: List[Example],
    train_frac: float = None,
    test_frac: float = None, 
    shuffle: bool = True,
    random_seed: int = 42,
   ) -> Tuple[Example]:
    """ split the input example into a training and a
    testing set. """
    n_examples = len(examples)
    n_train = int(np.ceil(n_examples*train_frac))
    n_test = int(np.ceil(n_examples*test_frac))
    n_total = n_train + n_test
    
    if shuffle:
        random_state = np.random.RandomState(random_seed)
        order = random_state.permutation(n_examples)
        train_idx = order[:n_train]
        test_idx = order[n_train:n_total]
    else:
        train_idx = np.arange(n_train)
        test_idx = np.arange(n_train, n_total)
    
    train_examples = [examples[idx] for idx in train_idx]
    test_examples = [examples[idx] for idx in test_idx]
    return train_examples, test_examples


def generate_batches(
    X: List[str], 
    Y: List[Any], 
    batch_size: int,
) -> Iterable[List[Any]]:
    """ Yield a batch of examples from the input raw data """
    X_batch = list()
    Y_batch = list()
    
    for x, y in zip(X,Y):
        X_batch.append(x)
        Y_batch.append(y)
        if len(X_batch) < batch_size:
            continue
        yield X_batch, Y_batch    
        X_batch = list()
        Y_batch = list()

            
def get_labels_depth(labels: List[Any]) -> int:
    """ Get the depth level of a potentially nested list of labels """
    level = 1
    if isinstance(labels, list):
        return level + max(get_labels_depth(label) for label in labels)
    else:
        return 0
    
    
def make_alignment(
    labels: List[Tuple], 
    alignements: List[int],
) -> List[Any]:
    """ reformat the predicted labels to keep alignment
    with the input text."""
    n_labels = len(set(alignements))
    aligned_labels = [[] for idx in range(n_labels)]
    
    for idx, position in enumerate(alignements):
        aligned_labels[position].append(labels[idx])
    
    return aligned_labels
    

def convert_onehot_to_ids(
    one_hot: tf.Tensor
) -> tf.Tensor:
    """ """
    mask = tf.dtypes.cast(one_hot, tf.bool)
    s = tf.shape(mask)
    r = tf.reshape(
            tf.range(s[-1]),
            tf.concat([
                tf.ones(
                    tf.rank(one_hot) - 1, 
                    tf.int32),
                [-1]
            ],
            axis=0)
    )
    r = tf.tile(r, tf.concat([s[:-1], [1]], axis=0))
    ragged_tensor = tf.ragged.boolean_mask(r, mask)
    return ragged_tensor


def convert_ids_to_onehot(ids, depth, dtype):
    """ """
    one_hot_tensor = tf.convert_to_tensor(
        MultiLabelBinarizer(
            classes=range(depth)
        ).fit_transform(ids),
        dtype=dtype
    )
    return one_hot_tensor


def get_class_names(Y: list, classes=None):
    """ """
    if classes is None:
        classes = set()
    for y in Y:
        if isinstance(y, list):
            get_classes(y, classes)
        else:
            classes.add(y)
    class_names = list(sorted(classes))    
    return class_names


def get_class_weights(Y: list, mu: float=0.5):
    """ """
    Y_flatten = [y for sub_Y in Y for y in sub_Y]
    counter = Counter(sorted(Y_flatten))
    class_names = [k for k in counter.keys()]
    class_freqs = [v for v in counter.values()]
    total = sum(class_freqs)
    
    class_weights = []
    for key in counter.keys():
        weight = math.log(mu*total/float(counter[key]))
        weight = weight if weight > 1.0 else 1.0
        class_weights.append(weight)
    
    return class_names, class_weights