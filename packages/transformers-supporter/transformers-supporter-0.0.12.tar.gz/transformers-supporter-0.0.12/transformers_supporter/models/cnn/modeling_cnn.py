from transformers import PretrainedConfig
from transformers import PreTrainedModel
from transformers import AutoModel
from transformers import AutoTokenizer
from transformers import AutoConfig
from transformers import AutoModelForImageClassification
import torch
from torch.nn import functional as F
import pytorch_supporter
import transformers
from .configuration_cnn import CnnConfig
    
class CnnForImageClassification(PreTrainedModel):
    config_class = CnnConfig

    def __init__(self, config):
        super().__init__(config)
        self.layer = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels=config.in_channels, out_channels=32, kernel_size=5, stride=1, padding=0),
            torch.nn.BatchNorm2d(num_features=32),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=2, stride=2, padding=0),
            torch.nn.Conv2d(in_channels=32, out_channels=32, kernel_size=5, stride=1, padding=0),
            torch.nn.BatchNorm2d(num_features=32),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=2, stride=2, padding=0),
            torch.nn.Flatten(), #배치를 제외한 모든 차원을 평탄화
            #pytorch_supporter.layers.LazilyInitializedLinear(out_features=config.num_labels)
            torch.nn.Linear(in_features=512, out_features=config.num_labels)
        )

    def forward(self, pixel_values, labels=None):
        #print(pixel_values.shape) #
        logits = self.layer(pixel_values)
        #print(logits.shape) #torch.Size([16, 3])
        if labels == None:
            return transformers.file_utils.ModelOutput({'logits': logits})
        else:
            #print(labels.shape) #
            loss = F.nll_loss(F.log_softmax(logits), labels) #원핫 벡터를 넣을 필요없이 바로 실제값을 인자로 사용 #nll은 Negative Log Likelihood의 약자
            return transformers.file_utils.ModelOutput({'loss': loss, 'logits': logits})

#오토 모델에 등록
AutoModelForImageClassification.register(CnnConfig, CnnForImageClassification)

####################

from transformers import PreTrainedModel
import torch
from torch.nn import functional as F
import pytorch_supporter
import transformers
from .configuration_cnn import CnnConfig

class CnnForKeyPointDetection(PreTrainedModel):
    config_class = CnnConfig

    def __init__(self, config):
        super().__init__(config)
        self.layer = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels=3, out_channels=32, kernel_size=5, stride=1, padding=0),
            torch.nn.BatchNorm2d(num_features=32),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=2, stride=2, padding=0),
            torch.nn.Conv2d(in_channels=32, out_channels=32, kernel_size=5, stride=1, padding=0),
            torch.nn.BatchNorm2d(num_features=32),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=2, stride=2, padding=0),
            torch.nn.Flatten(), #배치를 제외한 모든 차원을 평탄화
            torch.nn.Linear(in_features=14112, out_features=config.num_labels * 2)
            #pytorch_supporter.layers.LazilyInitializedLinear(out_features=30)
        )

    def forward(self, pixel_values, labels=None):
        #print(pixel_values.shape) #
        logits = self.layer(pixel_values)
        #print(logits.shape) #torch.Size([16, 3])
        if labels == None:
            return transformers.file_utils.ModelOutput({'logits': logits})
        else:
            #print(labels.shape) #
            #loss = torch.nn.MSELoss()(logits, labels) 
            loss = F.mse_loss(logits, labels) 
            return transformers.file_utils.ModelOutput({'loss': loss, 'logits': logits})

'''
#오토 모델에 등록
AutoModelForKeyPointDetection.register(CnnConfig, CnnForKeyPointDetection)
'''

####################
