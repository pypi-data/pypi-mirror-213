from transformers import PretrainedConfig
from transformers import PreTrainedModel
from transformers import AutoModel
from transformers import AutoTokenizer
from transformers import AutoConfig
from transformers import AutoModelForSequenceClassification
import torch
from torch.nn import functional as F
import transformers
from .configuration_ann import AnnConfig

class AnnForTabularRegression(PreTrainedModel):
    config_class = AnnConfig

    def __init__(self, config):
        super().__init__(config)
        self.layer = torch.nn.Sequential(
            torch.nn.Linear(in_features=config.in_features, out_features=32),
            #torch.nn.BatchNorm1d(num_features=32),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=32, out_features=1)   
        )

    def forward(self, x, labels=None):
        #print(x.shape) #
        logits = self.layer(x)
        #print(logits.shape) #
        if labels == None:
            return transformers.file_utils.ModelOutput({'logits': logits})
        else:
            #print(labels.shape) #torch.Size([8, 1]) #
            #loss = torch.nn.MSELoss()(logits, labels) 
            loss = F.mse_loss(logits, labels) 
            return transformers.file_utils.ModelOutput({'loss': loss, 'logits': logits})

'''
#오토 모델에 등록
AutoModelForTabularRegression.register(AnnConfig, AnnForTabularRegression)
'''

####################

from transformers import PretrainedConfig
from transformers import PreTrainedModel
from transformers import AutoModel
from transformers import AutoTokenizer
from transformers import AutoConfig
from transformers import AutoModelForSequenceClassification
import transformers
import torch
from torch.nn import functional as F
import transformers
from .configuration_ann import AnnConfig

class AnnForTabularBinaryClassification(PreTrainedModel):
    config_class = AnnConfig

    def __init__(self, config):
        super().__init__(config)
        self.layer = torch.nn.Sequential(
            torch.nn.Linear(in_features=config.in_features, out_features=32),
            #torch.nn.BatchNorm1d(num_features=32),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=32, out_features=1)
        )

    def forward(self, x, labels=None):
        #print(x.shape) #torch.Size([2, 4])
        logits = self.layer(x)
        #print(logits.shape) #torch.Size([16, 3])
        if labels == None:
            return transformers.file_utils.ModelOutput({'logits': logits})
        else:
            #print(labels.shape) #torch.Size([2, 3])
            #loss = F.binary_cross_entropy(F.sigmoid(logits), labels)
            loss = F.binary_cross_entropy_with_logits(logits, labels)
            return transformers.file_utils.ModelOutput({'loss': loss, 'logits': logits})

'''
#오토 모델에 등록
AutoModelForTabularClassification.register(AnnConfig, AnnForTabularBinaryClassification)
'''

####################

from transformers import PretrainedConfig
from transformers import PreTrainedModel
from transformers import AutoModel
from transformers import AutoTokenizer
from transformers import AutoConfig
from transformers import AutoModelForSequenceClassification
import torch
from torch.nn import functional as F
import transformers
from .configuration_ann import AnnConfig

class AnnForTabularClassification(PreTrainedModel):
    config_class = AnnConfig

    def __init__(self, config):
        super().__init__(config)
        self.layer = torch.nn.Sequential(
            torch.nn.Linear(in_features=config.in_features, out_features=32),
            #torch.nn.BatchNorm1d(num_features=32),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=32, out_features=config.num_labels)
        )

    def forward(self, x, labels=None):
        #print(x.shape) #torch.Size([2, 4])
        logits = self.layer(x)
        #print(logits.shape) #torch.Size([16, 3])
        if labels == None:
            return transformers.file_utils.ModelOutput({'logits': logits})
        else:
            #print(labels.shape) #torch.Size([2, 3])
            loss = F.nll_loss(F.log_softmax(logits), labels) #원핫 벡터를 넣을 필요없이 바로 실제값을 인자로 사용 #nll은 Negative Log Likelihood의 약자
            return transformers.file_utils.ModelOutput({'loss': loss, 'logits': logits})

'''
#오토 모델에 등록
AutoModelForTabularClassification.register(AnnConfig, AnnForTabularClassification)
'''

####################
