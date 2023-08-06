import os
import logging
import shutil

from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple

from dataclasses import dataclass

from pathlib import Path

import numpy as np
import tensorflow as tf
import transformers

from tensorflow.keras.optimizers.experimental import AdamW
from tensorflow.keras.metrics import (
    Mean,
    Precision,
    Recall,
)

from transformers import (
     AutoConfig,
     AutoTokenizer,
     PretrainedConfig,
     PreTrainedTokenizerFast,
     TFPreTrainedModel,
     TFAutoModelForMaskedLM,
)

from tokenizers.pre_tokenizers import Whitespace

from nlpipes.trainers.trainers import Trainer
from nlpipes.losses.losses import WCELoss
from nlpipes.metrics.confusion import F1_Score

from nlpipes.data.data_loaders import DataLoader
from nlpipes.data.data_selectors import DataSelector
from nlpipes.data.data_augmentors import VocabAugmentor
from nlpipes.data.data_processors import MultiLabelProcessor
from nlpipes.data.data_cleaners import clean

from nlpipes.data.data_utils import (
     create_multilabel_examples,
     split_examples,
     generate_batches,
     chunk,
     convert_onehot_to_ids,
     convert_ids_to_onehot,
)

from nlpipes.data.data_types import (
     Example,
     Features,
     Prediction,
     Classification,
)

from nlpipes.callbacks.callbacks import (
     TrainingStep,
     History,
     LossHistory,
     FBetaScoreHistory,
     F1ScoreHistory,
     PrecisionHistory,
     RecallHistory,
     ModelCheckpoint,
     CSVLogger,
     ProgbarLogger,
     EarlyStopping,
     TimedStopping,
)

transformers.logging.set_verbosity_error()

logger = logging.getLogger('__name__')


@dataclass
class PipelineForMultiLabelSequenceClassification():
    """ The pipeline for aspect category classification.
    
    Args
    ----------
    model(TFPreTrainedModel):
       The model used for the task`.
    
    tokenizer(PreTrainedTokenizerFast):
       The rust tokenizer used to convert the input
       text into encoded vectors.
    
    config(PretrainedConfig): 
       The model configuration file.
    """
    
    model: TFPreTrainedModel
    tokenizer: PreTrainedTokenizerFast
    config: PretrainedConfig
    
    def train(self,
              X: List[str] = None, 
              Y: List[str] =  None,
              train_frac: float = 0.8,
              test_frac: float = 0.2,
              class_weights: List[float] = None, 
              epochs: int = 3,
              batch_size: int = 16,
              thresholds: float = 0.5,
              max_length: int = 128,
              lr: float = 2e-5,
              beta_1: float = 0.9,
              beta_2: float = 0.999,
              patience: int = 99999,
              min_delta: float = 0.01,
              time_limit: int = 86400,
              random_seed: int = 69,
              keep_checkpoints: bool = False,
              verbose: bool = True,
              checkpoints_dir: str = './model/checkpoints',
              logs_dir: str = './model',
             ) -> Tuple[History]:
        """ Train a model for multi-label classification.
        Most of the training process is implemented through 
        callbacks functions. Even the actual training step 
        (calculating the gradient and updating the weights 
        using an optimizer) is implemented as callbacks and
        is not part of the Trainer itself. This provide a 
        modular architecture that allows new ideas to be 
        implemented without having to change and increase
        the complexity of the trainer. """
        
        examples = create_multilabel_examples(
            texts=X, 
            labels=Y,
            config=self.config,
        )
        
        train_examples, test_examples = split_examples(
            examples,
            train_frac=train_frac,
            test_frac=test_frac,
            shuffle=True,
            random_seed=random_seed,
        )
        
        data_processor = MultiLabelProcessor(
            name='DataProcessor',
            tokenizer=self.tokenizer,
            config=self.config,
            max_length=max_length,
        )
        
        train_stream = DataLoader(
            name='TrainDataLoader',
            examples=train_examples,
            batch_size=batch_size,
            data_processor=data_processor,
            random_seed=random_seed,
        )
        
        test_stream = DataLoader(
            name='TestDataLoader',
            examples=test_examples,
            batch_size=batch_size,
            data_processor=data_processor,
            random_seed=random_seed,
        )
        
        training_step = TrainingStep(
            name='TrainingStep',
            model=self.model,
            loss_fn=WCELoss(class_weights),
            optimizer=AdamW(
                learning_rate=lr,
                beta_1=beta_1,
                beta_2=beta_2,
            ),
        )
        
        loss_history = LossHistory(
            name='Loss', 
            metric=Mean(),
            training_step=training_step,
            verbose=verbose,
        )
        
        f1_history = F1ScoreHistory(
            name='F1',
            training_step=training_step,
            metric=F1_Score(
                thresholds=thresholds, 
                top_k=1,
            ),
            mode='multilabel',
            verbose=verbose,
        )
        
        precision_history = PrecisionHistory(
            name='Precision',
            training_step=training_step,
            metric=Precision(
                thresholds, 
                top_k=1,
            ),
            mode='multilabel',
            verbose=verbose,
        )
        
        recall_history = RecallHistory(
            name='Recall',
            training_step=training_step,
            metric=Recall(
                thresholds, 
                top_k=1,
            ),
            mode='multilabel',
            verbose=verbose,
        )
        
        model_checkpoint = ModelCheckpoint(
            name='ModelCheckpoint',
            history=loss_history,
            model=self.model, 
            direction='minimize',
            checkpoints_dir=checkpoints_dir,
        )
        
        early_stopping = EarlyStopping(
            name='EarlyStopping',
            history=loss_history,
            min_delta=min_delta,
            direction='minimize',
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
                f1_history,
                precision_history,
                recall_history,
            ],
            num_samples=sum([
                train_stream.num_examples(),
                test_stream.num_examples(),
            ])
        )
        
        callbacks = [
            training_step,
            loss_history,
            f1_history,
            precision_history,
            recall_history,
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
            
        return (
            loss_history,
            f1_history, 
            precision_history,
            recall_history,
        )
    
    def evaluate(self,
                 X: List[str],
                 Y: List[str],
                 metric: tf.metrics.Metric,
                 batch_size: int = 32,
                 thresholds: float = 0.5,
                ) -> tf.metrics.Metric:
        """ Evaluate the model performance on new data
        according to the user-defined evaluation metric """
        
        for texts, labels in generate_batches(X, Y, batch_size):
            examples = self.ingest(texts, labels)
            features = self.transform(examples)
            predictions = self.predict(features, thresholds)
            
            y_true = [e.label for e in examples]
            y_pred = [p.label for p in predictions]
              
            y_true = convert_ids_to_onehot(
                ids=y_true,
                depth=self.config.num_labels,
                dtype=tf.float32
            )
            
            metric.update_state(y_true, y_pred)
            
        return metric.result()
    
    def classify(
        self,
        texts: List[str],
        thresholds: float = 0.5,
        chunk_text: bool = False,
    ) -> List[Classification]:
        """ Get predictions on new input texts """
        
        examples = self.ingest(texts)
        features = self.transform(examples)
        predictions = self.predict(features, thresholds)
        classifications = self.postprocess(predictions, examples, thresholds)
        
        return classifications
    
    def ingest(
        self,
        texts: List[str],
        labels: Optional[str] = None,
        chunk_text: Optional[bool] = False,
    ) -> List[Example]:
        """ Convert each raw text into examples. 
        Raw texts can eventually be chunk into spans """
        
        if labels:
            labels_id = [
                [
                    self.config.label2id[label] 
                    for label in sub_labels
                ]
                for sub_labels in labels
            ]
            examples = [
                Example(text, label) 
                for text, label
                in zip(texts, labels_id)
            ]
        else:
            texts = chunk(texts) if chunk_text else texts
            examples = [Example(text) for text in texts]
            
        return examples
    
    def transform(self, examples: Iterable[Example]) -> Features: 
        """ Encode human-readable examples into encoded
        features that will be used as input by the model. """
        
        texts = [e.text for e in examples]
        max_length = self.config.max_position_embeddings
        
        inputs = self.tokenizer(
           texts,
           add_special_tokens=True,
           padding=True,
           truncation=True,
           max_length=max_length,
           is_split_into_words = False,
           return_attention_mask=True,
           return_token_type_ids=True,
           return_tensors='tf',
        )
        
        features = Features(
           input_ids=inputs['input_ids'],
           attention_mask=inputs['attention_mask'],
           token_type_ids=inputs['token_type_ids'],
        )
        
        return features
    
    def predict(
        self,
        features: Features, 
        thresholds: float=0.5,
    ) -> List[Prediction]:
        """ Predict the label indices where prediction score
        is over the user defined threshold and compute the loss
        value associated with each prediction. """
        
        outputs = self.model.call(
            input_ids=features.input_ids,
            attention_mask=features.attention_mask,
            token_type_ids=features.token_type_ids,
        )
        
        logits = outputs.logits
        confidences = tf.nn.sigmoid(logits)
        thresholds = tf.constant(thresholds)
        labels = tf.cast(
            tf.math.greater(confidences, thresholds), 
            tf.float32,
        )
        
        predictions = [
            Prediction(label, confidence)
            for label, confidence
            in zip(labels, confidences)
        ]
        
        return predictions
    
    def postprocess(
        self,
        predictions: Iterable[Prediction],
        examples: Iterable[Example],
        thresholds: float,
    ) -> List[Classification]:
        """ Post-process the predictions. We convert tensors 
        into more convenient python lists and alss convert the 
        predicted labels ids into their original name. """
        
        texts = [e.text for e in examples]
        id2label = self.config.id2label
        
        labels = [
            convert_onehot_to_ids(p.label) 
            for p in predictions
        ]
        
        labels = [
            [id2label[l.numpy()] for l in label]
            for label in labels
        ]
        
        confidences = [
            p.confidence.numpy()
            for p in predictions
        ]
        
        confidences = [
            c[c > thresholds] 
            for c in confidences
        ]
        
        confidences = [c.tolist() for c in confidences]
        
        classifications = [
            Classification(text, label, confidence)
            for text, label, confidence
            in zip(texts, labels, confidences)
        ]

        return classifications
    
    def save(self, save_dir: str):
        """ Save the trained model on disk """
        
        os.makedirs(save_dir, exist_ok=True)
        self.model.save_pretrained(save_dir)
        self.tokenizer.save_pretrained(save_dir)
        self.config.save_pretrained(save_dir)
