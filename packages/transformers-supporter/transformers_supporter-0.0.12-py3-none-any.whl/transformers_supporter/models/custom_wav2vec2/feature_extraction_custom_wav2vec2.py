from transformers import FeatureExtractionMixin
import torch
from transformers.image_utils import is_batched
from transformers import BatchFeature
from transformers import AutoFeatureExtractor
from torchvision import transforms

#Custom Feature extractor class for Wav2Vec2 (https://github.com/huggingface/transformers/blob/main/src/transformers/models/wav2vec2/feature_extraction_wav2vec2.py)
class CustomWav2Vec2FeatureExtractor(FeatureExtractionMixin):
    def __init__(self, sampling_rate=16000, **kwargs):
        super().__init__(**kwargs)
        self.sampling_rate = sampling_rate

    def __call__(self, raw_speeches, sampling_rate=None, return_tensors=None, **kwargs):
        if sampling_rate is not None:
            if sampling_rate != self.sampling_rate:
                raise ValueError(
                    f"The model corresponding to this feature extractor: {self} was trained using a sampling rate of"
                    f" {self.sampling_rate}. Please make sure that the provided `raw_speech` input was sampled with"
                    f" {self.sampling_rate} and not {sampling_rate}."
                )
        else:
            pint(
                "It is strongly recommended to pass the ``sampling_rate`` argument to this function. "
                "Failing to do so can result in silent errors that might be hard to debug."
            )
        is_batched = bool(
            isinstance(raw_speeches, (list, tuple))
            and (isinstance(raw_speeches[0], np.ndarray) or isinstance(raw_speeches[0], (tuple, list)))
        )
        if not is_batched:
            raw_speeches = [raw_speeches]
        raw_speeches = self.normalize(raw_speeches)
        #print(raw_speeches[0].shape) #
        '''
        if return_tensors == 'pt':
            raw_speeches = torch.stack(raw_speeches)
        return {"input_values": raw_speeches}
        '''
        #'''
        return BatchFeature(data={"input_values": raw_speeches}, tensor_type=return_tensors)
        #'''

    def normalize(self, input_values):
        #print(input_values) #[array([-0.00234106, -0.00490547, -0.00566588, ..., -0.00049007, -0.00182217, -0.00376346], dtype=float32)]
        #https://github.com/huggingface/transformers/blob/94b3f544a1f5e04b78d87a2ae32a7ac252e22e31/src/transformers/models/wav2vec2/feature_extraction_wav2vec2.py#L98
        normed_input_values = [(x - x.mean()) / np.sqrt(x.var() + 1e-7) for x in input_values]
        #print(normed_input_values) #[array([-0.02099453, -0.0440244 , -0.0508533 , ..., -0.00437161, -0.01633461, -0.03376846], dtype=float32)]
        return normed_input_values

#오토 특성 추출기에 등록
AutoFeatureExtractor.register(CustomWav2Vec2FeatureExtractor, CustomWav2Vec2FeatureExtractor)
