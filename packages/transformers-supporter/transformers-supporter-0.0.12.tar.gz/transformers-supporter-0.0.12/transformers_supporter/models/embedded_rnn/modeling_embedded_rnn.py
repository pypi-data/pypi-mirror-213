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
from .configuration_embedded_rnn import EmbeddedRnnConfig

class EmbeddedRnnForSequenceClassification(PreTrainedModel):
    config_class = EmbeddedRnnConfig

    def __init__(self, config):
        super().__init__(config)        
        self.layer = torch.nn.Sequential(
            torch.nn.Embedding(num_embeddings=config.vocab_size, embedding_dim=32),
            pytorch_supporter.layers.HiddenStateResetLSTM(input_size=32, hidden_size=32, batch_first=True),
            pytorch_supporter.layers.LSTMLastHiddenState(),
            torch.nn.Linear(in_features=32, out_features=config.num_labels)
        )

    def forward(self, input_ids, labels=None):
        logits = self.layer(input_ids)
        #print(logits.shape) #torch.Size([16, 3])
        if labels == None:
            return transformers.file_utils.ModelOutput({'logits': logits})
        else:
            loss = F.nll_loss(F.log_softmax(logits), labels) #원핫 벡터를 넣을 필요없이 바로 실제값을 인자로 사용 #nll은 Negative Log Likelihood의 약자
            return transformers.file_utils.ModelOutput({'loss': loss, 'logits': logits})

#오토 모델에 등록
AutoModelForSequenceClassification.register(EmbeddedRnnConfig, EmbeddedRnnForSequenceClassification)

####################

from transformers import PretrainedConfig
from transformers import PreTrainedModel
from transformers import AutoModel
from transformers import AutoTokenizer
from transformers import AutoConfig
import torch
from torch.nn import functional as F
import pytorch_supporter
import transformers
from .configuration_embedded_rnn import EmbeddedRnnConfig

class EmbeddedRnnForFixedLengthTranslation(PreTrainedModel):
    config_class = EmbeddedRnnConfig

    def __init__(self, config):
        super().__init__(config)        
        self.layer = torch.nn.Sequential(
            torch.nn.Embedding(num_embeddings=config.vocab_size, embedding_dim=32),
            pytorch_supporter.layers.HiddenStateResetLSTM(input_size=32, hidden_size=32, batch_first=True),
            pytorch_supporter.layers.SelectFromArray(index=0), #lstm output, 모든 타임 스텝(토큰: 숫자, 문자, 단어)의 숨은 상태, torch.Size([8, 380, 32]) 
            torch.nn.Linear(in_features=32, out_features=config.vocab_size)
        )

    def forward(self, input_ids, labels=None):
        logits = self.layer(input_ids)
        #print(logits.shape) #torch.Size([2, 3, 7])
        if labels == None:
            return transformers.file_utils.ModelOutput({'logits': logits})
        else:
            #print(labels.shape) #torch.Size([2, 3])
            logits_ = logits.view(-1, logits.size(-1))
            labels_ = labels.view(-1)
            #print(logits_.shape) #torch.Size([6, 7])
            #print(labels_.shape) #torch.Size([6])
            loss = F.nll_loss(F.log_softmax(logits_), labels_) #원핫 벡터를 넣을 필요없이 바로 실제값을 인자로 사용 #nll은 Negative Log Likelihood의 약자
            return transformers.file_utils.ModelOutput({'loss': loss, 'logits': logits})

'''
#오토 모델에 등록
AutoModelForFixedLengthTranslation.register(EmbeddedRnnConfig, EmbeddedRnnForFixedLengthTranslation)
'''

####################

from transformers import PretrainedConfig
from transformers import PreTrainedModel
from transformers import AutoModel
from transformers import AutoTokenizer
from transformers import AutoConfig
from transformers import AutoModelForSequenceClassification
from .configuration_embedded_rnn import PretrainedEmbeddedRnnConfig
import torch
from torch.nn import functional as F
from torchtext.vocab import build_vocab_from_iterator, Vectors
import transformers

class PretrainedEmbeddedRnnForSequenceClassification(PreTrainedModel):
    config_class = PretrainedEmbeddedRnnConfig

    def __init__(self, config):
        super().__init__(config)  
        self.layer = torch.nn.Sequential(
            self.load_pretrained_embedding(num_embeddings=config.vocab_size, embedding_dim=300, id_to_token=config.id_to_token),
            pytorch_supporter.layers.HiddenStateResetLSTM(input_size=300, hidden_size=32, batch_first=True),
            pytorch_supporter.layers.LSTMLastHiddenState(),
            torch.nn.Linear(in_features=32, out_features=config.num_labels)
        )

    def load_pretrained_embedding(self, num_embeddings, embedding_dim, id_to_token):
        #사이즈가 작은 파일들만 가져왔습니다. 다른 모델을 써보고 싶다면, 아래 링크를 참고해서 코드를 변경해서 사용하세요.
        #https://pytorch.org/text/stable/_modules/torchtext/vocab/vectors.html#Vectors
        '''
        #glove
        pretrained_vectors = Vectors(name='glove.6B.300d.txt', url='http://nlp.stanford.edu/data/glove.6B.zip')
        pretrained_emb = pretrained_vectors.get_vecs_by_tokens(id_to_token, lower_case_backup=True)
        embedding = torch.nn.Embedding(num_embeddings=num_embeddings, embedding_dim=embedding_dim).from_pretrained(pretrained_emb, freeze=False)
        return embedding
        '''
        #'''
        #fasttext
        pretrained_vectors = Vectors(name='wiki.simple.vec', url='https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.simple.vec')
        pretrained_emb = pretrained_vectors.get_vecs_by_tokens(id_to_token, lower_case_backup=True)
        embedding = torch.nn.Embedding(num_embeddings=num_embeddings, embedding_dim=embedding_dim).from_pretrained(pretrained_emb, freeze = False)
        return embedding
        #'''

    def forward(self, input_ids, labels=None):
        logits = self.layer(input_ids)
        #print(logits.shape) #torch.Size([16, 3])
        if labels == None:
            return transformers.file_utils.ModelOutput({'logits': logits})
        else:
            loss = F.nll_loss(F.log_softmax(logits), labels) #원핫 벡터를 넣을 필요없이 바로 실제값을 인자로 사용 #nll은 Negative Log Likelihood의 약자
            return transformers.file_utils.ModelOutput({'loss': loss, 'logits': logits})

#오토 모델에 등록
AutoModelForSequenceClassification.register(PretrainedEmbeddedRnnConfig, PretrainedEmbeddedRnnForSequenceClassification)

####################
