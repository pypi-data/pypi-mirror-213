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

class CustomBertConfig(PretrainedConfig):
    model_type = "custom-bert"

    def __init__(self, **kwargs):
        #https://github.com/huggingface/transformers/blob/98d88b23f54e5a23e741833f1e973fdf600cc2c5/src/transformers/configuration_utils.py#L323
        #Keys are always strings in JSON so convert ids to int here.       
        super().__init__(**kwargs)

#오토 설정에 등록
model_path = 'custom-bert'
AutoConfig.register(model_path, CustomBertConfig)
