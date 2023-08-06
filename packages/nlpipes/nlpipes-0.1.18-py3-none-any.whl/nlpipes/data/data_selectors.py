# Code adapted from https://github.com/georgian-io/Transformers-Domain-Adaptation

from collections import Counter

from typing import List
from typing import Optional
from typing import Union
from typing import Sequence
from typing import NewType

from tqdm import tqdm

import numpy as np
import pandas as pd
from scipy import sparse

from sklearn.preprocessing import RobustScaler

from transformers import PreTrainedTokenizer

from nlpipes.data.data_types import (
     Corpus,
     Token,
)

from nlpipes.metrics import (
    DIVERSITY_FEATURES,
    SIMILARITY_FEATURES,
    diversity_metrics_factory,
    similarity_metrics_factory,
)

np.seterr(invalid='ignore')


class DataSelector():
    """ """
    def __init__(
        self,
        name: str,
        target_corpus_size: Union[int, float],
        tokenizer: PreTrainedTokenizer,
        similarity_metrics: Optional[List[str]] = None,
        diversity_metrics: Optional[List[str]] = None,
    ):
        self.target_corpus_size = target_corpus_size
        self.tokenizer = tokenizer
        self.similarity_metrics = similarity_metrics
        self.diversity_metrics = diversity_metrics

    def __call__(self, corpus: Corpus) -> Corpus:
        self.fit(corpus)
        sub_corpus = self.select(corpus)
        return sub_corpus
    
    def fit(self, corpus: Corpus):
        """ Get tokens distribution from the corpus """
        self.tokens_distribution = self.get_tokens_distribution(" ".join(corpus))
        return self
    
    def select(self, corpus: Corpus) -> Corpus:
        """ Select the most relevant texts from the corpus
        according to the provided selection metrics """
        
        scores = self.compute_metrics(corpus)
        composite_scores = scores["composite"].sort_values(ascending=False)
        n_selected = (self.target_corpus_size 
                      if isinstance(self.target_corpus_size, int)
                      else int(self.target_corpus_size * len(corpus))
                     )
        selection_index = composite_scores.index[:n_selected]
        
        sub_corpus = pd.Series(corpus)[selection_index]
        
        return sub_corpus.tolist()

    def compute_metrics(self, corpus: Corpus) -> pd.DataFrame:
        """ """
        scores = pd.concat([self.compute_similarities(corpus),
                            self.compute_diversities(corpus),
                           ],
                           axis=1,
                          )
        
        # Ensure metrics are normalized
        scores = pd.DataFrame(
            RobustScaler().fit_transform(scores), columns=scores.columns
        )
        
        scores["composite"] = scores.sum(axis=1)
        return scores
    
    def compute_similarities(self, corpus: Corpus) -> pd.DataFrame:
        """ """ 
        
        similarities = pd.DataFrame()
        
        if (self.similarity_metrics is None):  
            return similarities

        tokens_distribution = self.get_tokens_distribution_batch(corpus)

        progress_bar = tqdm(
            self.similarity_metrics,
            desc="computing similarity",
            unit="metric",
            dynamic_ncols=True,
        )
        
        for metric in progress_bar:
            similarity_func = similarity_metrics_factory(metric)
            similarities[metric] = similarity_func(
                tokens_distribution, 
                self.tokens_distribution.reshape(1, -1),
            )
        
        return similarities
    
    def compute_diversities(self, corpus: Corpus) -> pd.DataFrame:
        """ """ 
        diversities = pd.DataFrame()
        
        if self.diversity_metrics is None:
            return diversities
        
        tokenized_corpus = self.tokenizer(corpus, add_special_tokens=False)
        tokens = [
            self.tokenizer.convert_ids_to_tokens(token_ids) 
            for token_ids in tokenized_corpus.input_ids
        ]
        
        progress_bar = tqdm(
            self.diversity_metrics,
            desc="computing diversity",
            unit="metric",
            dynamic_ncols=True,
        )
        
        for metric in progress_bar:
            diversity_function = diversity_metrics_factory(
                metric,
                tokens_distribution=self.tokens_distribution,
                vocab2id=self.tokenizer.vocab,
            )
            diversities[metric] = pd.Series(
                diversity_function(token) 
                for token in tokens
            )

        return diversities
    
    def get_tokens_distribution(self, text: str) -> np.ndarray:
        """ Get the vocabulary distribution of a corpus. The 
        function computes the token frequency for each corpus
        token detected in the tokenizer vocabulary. """
        
        vocabulary = self.tokenizer.vocab
        
        tokens = self.tokenizer.tokenize(text)
        tokens_count = Counter(tokens)
        
        tokens_distribution = np.zeros(len(vocabulary))
        for token, count in tokens_count.items():
            if token in vocabulary:
                token_idx = vocabulary[token]
                tokens_distribution[token_idx] = count
            
        tokens_distribution /= tokens_distribution.sum()
        
        return tokens_distribution

    def get_tokens_distribution_batch(self, corpus: Corpus) -> np.ndarray:
        """ """
        
        counters = [
            Counter(encoding.ids)
            for encoding in self.tokenizer.backend_tokenizer.encode_batch(
                corpus, add_special_tokens=False
            )
        ]
        
        rows = np.array(
            [val for i, counter in enumerate(counters) for val in [i] * len(counter)]
        )
        cols = np.array(
            [key for counter in counters for key in counter.keys()
            ]
        )
        data = np.array(
            [value for counter in counters for value in counter.values()]
        )
        
        term_counts = sparse.csr_matrix(
            (data, (rows, cols)),
            shape=(len(counters), len(self.tokenizer)),
            dtype=np.uint16 if len(self.tokenizer) < 2**16 else np.uint32,
        )

        term_dist = term_counts / term_counts.sum(axis=1)
        
        return np.array(term_dist)
