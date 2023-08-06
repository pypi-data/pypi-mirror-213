from transformers import PretrainedConfig
from transformers import TFBertPreTrainedModel 

from nlpipes.layers.bert_layers import TFAdaptedBertMainLayer


class TFAdaptedBertModel(TFBertPreTrainedModel):
    """ The Bert Model with additionnal bottleneck adapters layers 
    outputting raw hidden-states without any specific head on top. """
    def __init__(self, config: PretrainedConfig, *inputs, **kwargs):
        super().__init__(config, *inputs, **kwargs)

        self.bert = TFAdaptedBertMainLayer(config, name="adapted_bert")
    
    def call(self, inputs, **kwargs):
        outputs = self.bert(inputs, **kwargs)

        return outputs
