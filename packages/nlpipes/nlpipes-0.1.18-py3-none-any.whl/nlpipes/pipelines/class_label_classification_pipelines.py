import os
import logging
import shutil

from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple

from dataclasses import dataclass

from pathlib import Path

import tensorflow as tf
import transformers

from tensorflow.keras.optimizers.experimental import AdamW
from tensorflow.keras.metrics import (
    Mean,
    Precision,
    Recall,
    CategoricalAccuracy,
)

from transformers import (
    PretrainedConfig,
    PreTrainedTokenizerFast,
    TFPreTrainedModel,
    TFAutoModelForMaskedLM,
    AutoConfig,
    AutoTokenizer,
)

from tokenizers.pre_tokenizers import Whitespace

from nlpipes.trainers.trainers import Trainer
from nlpipes.losses.losses import SCELoss
from nlpipes.metrics.confusion import F1_Score

from nlpipes.data.data_loaders import DataLoader
from nlpipes.data.data_selectors import DataSelector
from nlpipes.data.data_augmentors import VocabAugmentor
from nlpipes.data.data_processors import ClassLabelDataProcessor
from nlpipes.data.data_cleaners import clean

from nlpipes.data.data_utils import (
     create_classlabel_examples,
     generate_batches,
     get_labels_depth,
     split_examples,
     make_alignment,
     chunk,
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
     AccuracyHistory,
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
class PipelineForClassLabelSequenceClassification():
    """ The pipeline for aspect sentiment classification.
    
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
              X: List[str], 
              Y: List[str],
              train_frac: float = 0.8,
              test_frac: float = 0.2,
              epochs: int = 3,
              batch_size: int = 16,
              max_length: int = 128,
              lr: float = 2e-5,
              beta_1: float = 0.9,
              beta_2: float = 0.999,
              patience: int = 2,
              min_delta: float = 0.01,
              time_limit: int = 86400,
              random_seed: int = 69,
              verbose: bool = True,
              keep_checkpoints: bool = False,
              checkpoints_dir: str = './model/checkpoints',
              logs_dir: str = './model',
             ) -> Tuple[History]:
        """ Train a model for class-label sequence classification """
        
        examples = create_classlabel_examples(
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
        
        data_processor = ClassLabelDataProcessor(
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
            loss_fn=SCELoss(),
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
        
        accuracy_history = AccuracyHistory(
            name='Accuracy',
            metric=CategoricalAccuracy(),
            training_step=training_step,
            verbose=verbose,
        )
        
        f1_history = F1ScoreHistory(
            name='F1',
            training_step=training_step,
            metric=F1_Score(),
            mode='multiclass',
            verbose=verbose,
        )
        
        precision_history = PrecisionHistory(
            name='Precision',
            training_step=training_step,
            metric=Precision(),
            mode='multiclass',
            verbose=verbose,
        )
        
        recall_history = RecallHistory(
            name='Recall',
            training_step=training_step,
            metric=Recall(),
            mode='multiclass',
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
                accuracy_history,
                f1_history,
                precision_history,
                recall_history,
            ],                
            num_samples=sum([
                train_stream.num_examples(),
                test_stream.num_examples(),
            ]))
        
        callbacks = [
            training_step,
            loss_history,
            accuracy_history,
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
            accuracy_history, 
            f1_history, 
            precision_history, 
            recall_history,
        )
    
    def evaluate(self,
                 X: List[str],
                 Y: List[str],
                 metric: tf.metrics.Metric,
                 batch_size: int = 16,
                ) -> tf.metrics.Metric:
        """ Evaluate the model performance on new data
        according to the user-defined evaluation metric """
        
        for texts, labels in generate_batches(X, Y, batch_size):
            examples = self.ingest(texts, labels=labels)
            features = self.transform(examples)
            predictions = self.predict(features)
            
            y_true = [e.label for e in examples]
            y_pred = [p.label for p in predictions]
            
            metric.update_state(y_true, y_pred)
        
        return metric.result()
    
    def classify(
        self, 
        texts: List[str],
        aspects: List[List[str]],
    ) -> List[Classification]:
        """ Get classification on new unlabeled data """
         
        examples = self.ingest(texts, aspects)
        features = self.transform(examples)
        predictions = self.predict(features)
        classifications = self.postprocess(
            predictions, examples, texts
        )
        
        return classifications
        
    def ingest(
        self,
        texts: List[str],
        aspects: Optional[List[str]] = None,
        labels: Optional[List[str]] = None,
        chunk_text: Optional[bool] = True,
    ) -> List[Example]:
        """ Serialize each raw text into examples. 
        We keep the a lignment between the examples and 
        the original raw input texts. """
        
        examples = []
        
        if labels:
            for idx, text in enumerate(texts):
                aspects = [label[0] for label in labels[idx]]
                aspect_labels = [label[1] for label in labels[idx]]

                for num, aspect in enumerate(aspects):
                    aspect = aspect.lower()
                    label = aspect_labels[num]
                    label = self.config.label2id[label]
                    example = Example(
                        text=text,
                        aspect=aspect,
                        label=label,
                        alignment=idx,
                    )
                    examples.append(example)
                    
        else:
            for idx, text in enumerate(texts):
                for aspect in aspects[idx]:
                    example = Example(
                        text=text, 
                        aspect=aspect, 
                        alignment=idx,
                    )
                    examples.append(example)
                    
        return examples
    
    def transform(self, examples: Iterable[Example]) -> Features: 
        """ Transform human-readable sequences into encoded
        features that can be use as input by the model. """
        
        text_pairs = [(e.text, e.aspect) for e in examples]
        max_length = self.config.max_position_embeddings
        
        inputs = self.tokenizer(
           text_pairs,
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
    
    def predict(self, features: Features) -> List[Prediction]:
        """ Predict the label index matching the maximum
        prediction score and compute the loss value associated
        with each prediction. """

        outputs = self.model.call(
            input_ids=features.input_ids,
            attention_mask=features.attention_mask,
            token_type_ids=features.token_type_ids,
        )

        logits = outputs.logits
        confidences = tf.nn.softmax(logits, axis=1)
        labels = tf.argmax(logits, axis=-1)
        
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
        texts: Iterable[str], 
    ) -> List[Classification]:
        """ Post-process the predictions. We convert tensors 
        into more convenient python lists and also convert the 
        predicted labels ids into their original name. """
        
        aspects = [e.aspect for e in examples]
        alignments = [e.alignment for e in examples]
        
        labels = [p.label.numpy() for p in predictions]
        labels = [self.config.id2label[l] for l in labels]
        labels = [[a, l] for a, l in zip(aspects, labels)]
        labels = make_alignment(labels, alignments)
        
        confidences = [p.confidence.numpy() for p in predictions]
        confidences = [max(c.tolist()) for c in confidences]
        confidences = make_alignment(confidences, alignments)
        
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
        