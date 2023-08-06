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
from .configuration_embedded_1dcnn import Embedded1dcnnConfig

class Embedded1dcnnForSequenceClassification(PreTrainedModel):
    config_class = Embedded1dcnnConfig

    def __init__(self, config):
        super().__init__(config)
        self.layer = torch.nn.Sequential(
            torch.nn.Embedding(num_embeddings=config.vocab_size, embedding_dim=32), #
            #https://chriskhanhtran.github.io/posts/cnn-sentence-classification/
            #Permute `x_embed` to match input shape requirement of `nn.Conv1d`.
            #Output shape: (b, embed_dim, max_len)
            pytorch_supporter.layers.Permute((0, 2, 1)),
            torch.nn.Conv1d(in_channels=32, out_channels=32, kernel_size=5, stride=1, padding=0),
            torch.nn.BatchNorm1d(num_features=32),
            torch.nn.ReLU(),
            torch.nn.MaxPool1d(kernel_size=2, stride=2, padding=0),
            torch.nn.Conv1d(in_channels=32, out_channels=32, kernel_size=5, stride=1, padding=0),
            torch.nn.BatchNorm1d(num_features=32),
            torch.nn.ReLU(),
            torch.nn.MaxPool1d(kernel_size=2, stride=2, padding=0),
            torch.nn.Flatten(), #배치를 제외한 모든 차원을 평탄화
            pytorch_supporter.layers.LazilyInitializedLinear(out_features=config.num_labels)
        )

    def forward(self, input_ids, labels=None):
        logits = self.layer(input_ids)
        print(logits.shape) #torch.Size([16, 3])
        if labels == None:
            return transformers.file_utils.ModelOutput({'logits': logits})
        else:
            loss = F.nll_loss(F.log_softmax(logits), labels) #원핫 벡터를 넣을 필요없이 바로 실제값을 인자로 사용 #nll은 Negative Log Likelihood의 약자
            return transformers.file_utils.ModelOutput({'loss': loss, 'logits': logits})

#오토 모델에 등록
AutoModelForSequenceClassification.register(Embedded1dcnnConfig, Embedded1dcnnForSequenceClassification)
