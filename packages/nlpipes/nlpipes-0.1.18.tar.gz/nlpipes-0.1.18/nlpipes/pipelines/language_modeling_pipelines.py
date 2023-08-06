import os
import logging
import shutil

from typing import List
from typing import Optional
from typing import Union

from pathlib import Path

from dataclasses import dataclass

import tensorflow as tf
import transformers
from tensorflow.keras.optimizers.experimental import AdamW

from transformers import (
    PretrainedConfig,
    PreTrainedTokenizer,
    TFPreTrainedModel,
)

from nlpipes.trainers.trainers import Trainer

from nlpipes.losses.losses import SCELoss

from nlpipes.data.data_loaders import DataLoader
from nlpipes.data.data_processors import MLMProcessor

from nlpipes.data.data_selectors import DataSelector
from nlpipes.data.data_augmentors import VocabAugmentor
from nlpipes.data.data_cleaners import clean

from nlpipes.data.data_utils import (
     create_examples,
     split_examples,
)

from nlpipes.data.data_types import (
     Document,
     Corpus,
     Token,
     Example,
)

from nlpipes.callbacks.callbacks import (
     TrainingStep,
     History,
     LossHistory,
     AccuracyHistory,
     ModelCheckpoint,
     CSVLogger,
     ProgbarLogger,
     EarlyStopping,
     TimedStopping,
)

transformers.logging.set_verbosity_error()

logger = logging.getLogger('__name__')


@dataclass
class PipelineForMaskedLanguageModeling():
    """ The `pipeline` for the masked language modeling.
    
    Args
    ----------
    model(TFPreTrainedModel):
       The model used for the task.
    
    tokenizer(PreTrainedTokenizerFast):
       The rust tokenizer used to convert the input
       text into encoded vectors.
    
    config(PretrainedConfig): 
       The model configuration file.
    """
    
    model: TFPreTrainedModel
    tokenizer: PreTrainedTokenizer
    config: PretrainedConfig
    
    def train(
        self,
        texts: Corpus,
        train_frac: float = 0.8,
        test_frac: float = 0.2,
        epochs: int = 4,
        batch_size: int = 8,
        max_length: int = 256,
        learning_rate: float = 2e-5,
        beta_1: float = 0.9,
        beta_2: float = 0.999,
        mlm_prob: float = 0.15,
        target_corpus_size: Union[int, float] = 0.8,
        target_vocab_size: int = 31000,
        similarity_metrics: Optional[List[str]] = ['euclidean'],
        diversity_metrics: Optional[List[str]] = ['entropy'],
        min_delta: float = 0.01,
        patience: int = 5,
        time_limit: int = 86400,
        random_seed: int = 69,
        keep_checkpoints: bool = False,
        verbose: bool = True,
        save_corpus_dir: str = './model',
        checkpoints_dir: str = './model/checkpoints',
        logs_dir: str = './model',
    ) -> History:
        """ Train the model on a masked modeling task """
        
        data_selector = DataSelector(
            name='DataSelector',
            tokenizer=self.tokenizer,
            target_corpus_size=target_corpus_size,
            similarity_metrics=similarity_metrics,
            diversity_metrics=diversity_metrics,
        )
        
        vocab_augmentor = VocabAugmentor(
            name='VocabAugmentor',
            tokenizer=self.tokenizer,
            target_vocab_size=target_vocab_size,
            cased=False,
        )
        
        clean_texts = [clean(text) for text in texts]
        selected_texts = data_selector(clean_texts)
        new_tokens = vocab_augmentor.get_new_tokens(selected_texts)
        self.tokenizer.add_tokens(new_tokens)
        self.model.resize_token_embeddings(len(self.tokenizer))
        
        examples = create_examples(selected_texts)
        
        train_examples, test_examples = split_examples(
            examples=examples,
            train_frac=train_frac,
            test_frac=test_frac, 
            shuffle=True, 
        )

        data_processor = MLMProcessor(
            name='DataProcessor',
            tokenizer=self.tokenizer,
            config=self.config,
            max_length=max_length,
            mlm_prob=mlm_prob,
            mask_prob=0.80,
            rand_prob=0.10,
            idem_prob=0.10,
        )
        
        train_stream = DataLoader(
            name='TrainDataLoader',
            examples=train_examples,
            batch_size=batch_size,
            data_processor=data_processor,
        )
        
        test_stream = DataLoader(
            name='TestDataLoader',
            examples=test_examples,
            batch_size=batch_size,
            data_processor=data_processor,
        )
        
        training_step = TrainingStep(
            name='TrainingStep',
            model=self.model,
            loss_fn=SCELoss(),
            optimizer=AdamW(
                learning_rate=learning_rate,
                beta_1=beta_1,
                beta_2=beta_2,
            ),
        )
        
        loss_history = LossHistory(
            name='Loss', 
            metric = tf.metrics.Mean(),
            training_step=training_step,
            verbose=verbose,
        )
        
        model_checkpoint = ModelCheckpoint(
            name='ModelCheckpoint',
            history=loss_history,
            model=self.model, 
            direction='minimize',
            checkpoints_dir=checkpoints_dir,
            verbose=verbose,
        )
        
        early_stopping = EarlyStopping(
            name='EarlyStopping',
            history=loss_history,
            direction='minimize',
            min_delta=min_delta,
            patience=patience,
        )
        
        timed_stopping = TimedStopping(
            name='TimedStopping',
            time_limit=time_limit,
        )
        
        csv_logger = CSVLogger(
            name='CSVLogger',
            logs_dir=logs_dir,
        )
        
        progbar_logger = ProgbarLogger(
            name='ProgbarLogger',
            batch_size=batch_size,
            history=[
                loss_history,
            ],
            num_samples=sum([
                train_stream.num_examples(),
                test_stream.num_examples(),
            ])
        )
        
        callbacks = [
            training_step,
            loss_history,
            model_checkpoint,
            csv_logger,
            progbar_logger,
            timed_stopping,
        ]
        
        trainer = Trainer(callbacks)
        
        trainer.fit(
            train_stream=train_stream,
            test_stream=test_stream,
            epochs=epochs,
        )
        
        if keep_checkpoints == False:
            shutil.rmtree(checkpoints_dir)
            
        os.makedirs(save_corpus_dir, exist_ok=True) 
        corpus_path = os.path.join(save_corpus_dir, 'selected_corpus.txt')         
        Path(corpus_path).write_text('\n'.join(selected_texts))
        
        return loss_history
    
    def evaluate(self):
        """ Evaluate the model performance on new data
        according to the user-defined evaluation metric """
        raise NotImplementedError
    
    def save(self, save_dir: str):
        """ Save the model and the tokenizer on disk """
        
        os.makedirs(save_dir, exist_ok=True)        
        self.model.save_pretrained(save_dir)
        self.tokenizer.save_pretrained(save_dir)
        self.config.save_pretrained(save_dir)
        