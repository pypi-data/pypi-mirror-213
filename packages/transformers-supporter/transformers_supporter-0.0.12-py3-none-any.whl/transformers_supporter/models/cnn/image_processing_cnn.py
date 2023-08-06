from transformers import ImageProcessingMixin
from PIL import Image
import torch
from transformers.image_utils import is_batched
from transformers import BatchFeature
from transformers import AutoImageProcessor
from torchvision import transforms
from torch.nn import functional as F

class GrayscaleImageProcessor(ImageProcessingMixin):
    def __init__(self, image_mean=[0.5], image_std=[0.5], size={"height": 28, "width": 28}, **kwargs):
        super().__init__(**kwargs)
        self.image_mean = image_mean
        self.image_std = image_std
        self.size = size 

    def __call__(self, images, return_tensors=None, **kwargs):
        composed_transforms = transforms.Compose([
            transforms.Resize((self.size['height'], self.size['width'])),
            transforms.ToTensor(), #최소 최대 정규화 ([0, 1])
            transforms.Normalize(mean=self.image_mean, std=self.image_std) #표준 정규화 ([-1, 1])
        ])
        if not is_batched(images):
            images = [images]
        images = [image.convert('L') for image in images]
        images = [composed_transforms(image) for image in images]
        #print(images[0].shape) #torch.Size([1, 28, 28])
        '''
        if return_tensors == 'pt':
            images = torch.stack(images)
        return {"pixel_values": images}
        '''
        #'''
        images = torch.stack(images)
        return BatchFeature(data={"pixel_values": images}, tensor_type=return_tensors)
        #'''

    def postprocess(self, outputs, top_k=None):
        logits = outputs['logits']
        probabilities = F.softmax(logits, dim=-1)
        results = {'labels': [], 'scores': []}
        for probability in probabilities:
            label = probability.argmax()
            probability = probability[label]
            results['labels'].append(label)
            results['scores'].append(probability)        
        return results

#오토 이미지 프로세서에 등록
AutoImageProcessor.register(GrayscaleImageProcessor, GrayscaleImageProcessor)

####################################

from transformers import ImageProcessingMixin
from PIL import Image
import torch
from transformers.image_utils import is_batched
from transformers import BatchFeature
from transformers import AutoImageProcessor
from torchvision import transforms

class KeyPointImageProcessor(ImageProcessingMixin):
    def __init__(self, image_mean=[0.5, 0.5, 0.5], image_std=[0.5, 0.5, 0.5], **kwargs):
        super().__init__(**kwargs)
        self.image_mean = image_mean
        self.image_std = image_std

    def __call__(self, images, annotations=None, return_tensors=None, **kwargs):
        return_tensors = None #return_tensors 미지원
        composed_transforms = transforms.Compose([
            transforms.ToTensor(), #최소 최대 정규화 ([0, 1])
            transforms.Normalize(mean=self.image_mean, std=self.image_std) #표준 정규화 ([-1, 1])
        ])
        if not is_batched(images):
            images = [images]
        images = [image.convert('RGB') for image in images]
        images = [composed_transforms(image) for image in images]
        #print(images[0].shape) #torch.Size([3, 28, 28])
        if annotations == None:
            '''
            if return_tensors == 'pt':
                images = torch.stack(images)
            return {'pixel_values': images}
            '''
            #'''
            return BatchFeature(data={'pixel_values': images}, tensor_type=return_tensors)
            #'''
        else:
            #if not isinstance(annotations, list):
            #    annotations = [annotations]
            if isinstance(annotations, list) and len(annotations) > 0 and not isinstance(annotations[0], list):
                annotations = [annotations]
            labels = [self.get_x_y_keypoints(keypoints) for keypoints in annotations]
            '''
            if return_tensors == 'pt':
                images = torch.stack(images)
            return {'pixel_values': images, 'labels': labels}
            '''
            #'''
            return BatchFeature(data={'pixel_values': images, 'labels': labels}, tensor_type=return_tensors)
            #'''

    def get_x_y_keypoints(self, keypoints, as_tuple=False):
        new_keypoints = []
        xs = keypoints[::3]
        ys = keypoints[1::3]
        for x, y in zip(xs, ys):
            if not as_tuple:
                new_keypoints.append(x)
                new_keypoints.append(y)
            else:
                new_keypoints.append((x, y))
        return new_keypoints

#오토 이미지 프로세서에 등록
AutoImageProcessor.register(KeyPointImageProcessor, KeyPointImageProcessor)

####################################
