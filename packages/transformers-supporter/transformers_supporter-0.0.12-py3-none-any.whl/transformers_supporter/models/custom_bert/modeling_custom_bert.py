from transformers import PretrainedConfig
from transformers import PreTrainedModel
from transformers import AutoModel
from transformers import AutoTokenizer
from transformers import AutoConfig
from transformers import AutoModelForSequenceClassification
import torch
from torch.nn import functional as F
import pytorch_supporter
import transformers
from .configuration_custom_bert import CustomBertConfig

'''
class CustomBertForSequenceClassification(PreTrainedModel):
    config_class = CustomBertConfig

    def __init__(self, config):
        super().__init__(config)
        self.bert_layer = AutoModel.from_pretrained(config.bert_model_path)
        self.linear_layer = torch.nn.Linear(in_features=768, out_features=config.num_labels)

    def forward(self, input_ids, attention_mask=None, token_type_ids=None, labels=None):
        outputs = self.bert_layer(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        #print(outputs.keys()) #dict_keys(['last_hidden_state', 'pooler_output'])
        pooler_output = outputs.pooler_output
        #print(pooler_output.shape) #torch.Size([1, 768])
        logits = self.linear_layer(pooler_output)
        #print(logits.shape) #torch.Size([16, 3])
        if labels == None:
            return transformers.file_utils.ModelOutput({'logits': logits})
        else:
            loss = F.nll_loss(F.log_softmax(logits), labels) #원핫 벡터를 넣을 필요없이 바로 실제값을 인자로 사용 #nll은 Negative Log Likelihood의 약자
            return transformers.file_utils.ModelOutput({'loss': loss, 'logits': logits})
'''
#'''
#torch.nn.Sequential 버전
class CustomBertForSequenceClassification(PreTrainedModel):
    config_class = CustomBertConfig

    def __init__(self, config):
        super().__init__(config)
        self.layer = torch.nn.Sequential(
            pytorch_supporter.layers.DictToParameters(AutoModel.from_pretrained(config.bert_model_path)),
            pytorch_supporter.layers.SelectFromArray(index=1), #x.pooler_output
            torch.nn.Linear(in_features=768, out_features=config.num_labels)
        )

    def forward(self, input_ids, attention_mask=None, token_type_ids=None, labels=None):
        logits = self.layer(dict(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids))
        #print(pooler_output.shape) #torch.Size([1, 768])
        #print(logits.shape) #torch.Size([16, 3])
        if labels == None:
            return transformers.file_utils.ModelOutput({'logits': logits})
        else:
            loss = F.nll_loss(F.log_softmax(logits), labels) #원핫 벡터를 넣을 필요없이 바로 실제값을 인자로 사용 #nll은 Negative Log Likelihood의 약자
            return transformers.file_utils.ModelOutput({'loss': loss, 'logits': logits})
#'''

#오토 모델에 등록
AutoModelForSequenceClassification.register(CustomBertConfig, CustomBertForSequenceClassification)
