from transformers import PretrainedConfig
from transformers import PreTrainedModel
from transformers import AutoModel
from transformers import AutoTokenizer
from transformers import AutoConfig
from transformers import AutoModelForAudioClassification
import pytorch_supporter
import torch
from torch.nn import functional as F
import transformers
from .configuration_rnn import RnnConfig

class RnnForAudioClassification(PreTrainedModel):
    config_class = RnnConfig

    def __init__(self, config):
        super().__init__(config)        
        self.layer = torch.nn.Sequential(
            pytorch_supporter.layers.HiddenStateResetLSTM(input_size=1, hidden_size=32, batch_first=True),
            pytorch_supporter.layers.LSTMLastHiddenState(),
            torch.nn.Linear(in_features=32, out_features=config.num_labels)
        )

    def forward(self, input_values, labels=None):
        if len(input_values.shape) == 2:
            input_values = input_values.unsqueeze(-1)
        
        logits = self.layer(input_values)
        #print(logits.shape) #torch.Size([16, 3])
        if labels == None:
            return transformers.file_utils.ModelOutput({'logits': logits})
        else:
            loss = F.nll_loss(F.log_softmax(logits), labels) #원핫 벡터를 넣을 필요없이 바로 실제값을 인자로 사용 #nll은 Negative Log Likelihood의 약자
            return transformers.file_utils.ModelOutput({'loss': loss, 'logits': logits})

#모델을 오토 모델에 등록
model_path = 'rnn-config'
AutoConfig.register(model_path, RnnConfig)
AutoModelForAudioClassification.register(RnnConfig, RnnForAudioClassification)

####################

from transformers import PretrainedConfig
from transformers import PreTrainedModel
from transformers import AutoModel
from transformers import AutoTokenizer
from transformers import AutoConfig
from transformers import AutoModelForAudioClassification
import pytorch_supporter
import torch
from torch.nn import functional as F
import transformers
from .configuration_rnn import RnnConfig

class RnnForTimeSeriesRegression(PreTrainedModel):
    config_class = RnnConfig

    def __init__(self, config):
        super().__init__(config)        
        self.layer = torch.nn.Sequential(
            pytorch_supporter.layers.HiddenStateResetLSTM(input_size=1, hidden_size=32, batch_first=True),
            pytorch_supporter.layers.LSTMLastHiddenState(),
            torch.nn.Linear(in_features=32, out_features=32),
            #torch.nn.BatchNorm1d(num_features=32),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=32, out_features=1)   
        )

    def forward(self, input_values, labels=None):
        if len(input_values.shape) == 2:
            input_values = input_values.unsqueeze(-1)
        
        logits = self.layer(input_values)
        #print(logits.shape) #torch.Size([16, 3])
        if labels == None:
            return transformers.file_utils.ModelOutput({'logits': logits})
        else:
            #print(labels.shape) #torch.Size([8, 1]) #
            #loss = torch.nn.MSELoss()(logits, labels) 
            loss = F.mse_loss(logits, labels) 
            return transformers.file_utils.ModelOutput({'loss': loss, 'logits': logits})
        
'''
#모델을 오토 모델에 등록
model_path = 'rnn-config'
AutoConfig.register(model_path, RnnConfig)
AutoModelForTimeSeriesRegression.register(RnnConfig, RnnForTimeSeriesRegression)
'''
