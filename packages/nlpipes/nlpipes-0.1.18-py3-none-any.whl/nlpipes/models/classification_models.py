import tensorflow as tf

from transformers import PretrainedConfig
from transformers import TFBertPreTrainedModel

from nlpipes.layers.bert_layers import TFAdaptedBertMainLayer
from nlpipes.data.data_types import TFSequenceClassifierOutput


class TFAdaptedBertForSequenceClassification(TFBertPreTrainedModel):
    """ A modified Bert Model for sequence classification with additionnals
    bottleneck-adapters modules. It subclass the `TFBertPreTrainedModel`
    which is the base class for all TensorFlow BERT based models. 
    Note that the `TFBertPreTrainedModel` is also a `tf.keras.Model`. 
    Reference: https://arxiv.org/pdf/1902.00751.pdf """
    
    def __init__(self, config: PretrainedConfig, **kwargs):
        super().__init__(config, **kwargs)
        self.bert = TFAdaptedBertMainLayer(config, name="adapted_bert")
        self.dropout= tf.keras.layers.Dropout(config.hidden_dropout_prob)
        self.classifier = tf.keras.layers.Dense(
            units=config.num_labels,
            kernel_initializer=tf.keras.initializers.TruncatedNormal(
                stddev=config.initializer_range),
            name='classifier')
        
    def call(self,
             input_ids,
             attention_mask=None,
             token_type_ids=None,
             position_ids=None,
             head_mask=None,
             inputs_embeds=None,
             output_attentions=None,
             output_hidden_states=None,
             labels=None,
             class_weights=None,
             return_dict=None,
             training = False,
             **kwargs,
            ):
        
        bert_output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
            training=training,
        )
        
        pooler_output = bert_output['pooler_output']
        dropout_output = self.dropout(pooler_output, training=training)
        logits = self.classifier(dropout_output)
        
        return TFSequenceClassifierOutput(
            logits=logits,
            hidden_states=bert_output.hidden_states,
            attentions=bert_output.attentions,
    )


class AdaptedBertForSequenceClassification(TFBertPreTrainedModel):
    """ The Bert Model for sequence classification with additionnal
    bottleneck-adapters modules. It subclass the `TFBertPreTrainedModel`
    which is the base class for all TensorFlow BERT based models. 
    Note that the `TFBertPreTrainedModel` is also a `tf.keras.Model`. 
    Reference: https://arxiv.org/pdf/1902.00751.pdf """
    
    def __init__(self, config: PretrainedConfig, **kwargs):
        super().__init__(config, **kwargs)
        self.bert = TFAdaptedBertMainLayer(config, name="adapted_bert")
        self.dropout= tf.keras.layers.Dropout(config.hidden_dropout_prob)
        self.classifier = tf.keras.layers.Dense(
            units=config.num_labels,
            kernel_initializer=tf.keras.initializers.TruncatedNormal(
                stddev=config.initializer_range),
            name='classifier')
        
    def call(self,
             input_ids,
             attention_mask=None,
             token_type_ids=None,
             position_ids=None,
             head_mask=None,
             inputs_embeds=None,
             output_attentions=None,
             output_hidden_states=None,
             labels=None,
             class_weights=None,
             return_dict=None,
             training = False,
             **kwargs,
            ):
        
        bert_output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
            training=training,
        )
        
        pooler_output = bert_output['pooler_output']
        dropout_output = self.dropout(pooler_output, training=training)
        logits = self.classifier(dropout_output)
        
        return TFSequenceClassifierOutput(
            logits=logits,
            hidden_states=bert_output.hidden_states,
            attentions=bert_output.attentions,
    )
    