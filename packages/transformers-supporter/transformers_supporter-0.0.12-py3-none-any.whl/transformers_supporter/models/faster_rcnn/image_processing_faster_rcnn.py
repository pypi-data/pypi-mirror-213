from transformers import ImageProcessingMixin
from PIL import Image
import torch
from transformers.image_utils import is_batched
from transformers import BatchFeature
from transformers import AutoImageProcessor
from torchvision import transforms
from torch.nn import functional as F

class FasterRcnnImageProcessor(ImageProcessingMixin):
    def __init__(self, image_mean=[0.5, 0.5, 0.5], image_std=[0.5, 0.5, 0.5], **kwargs):
        super().__init__(**kwargs)
        self.image_mean = image_mean
        self.image_std = image_std

    def __call__(self, images, annotations=None, return_tensors=None, **kwargs):
        return_tensors = None #return_tensors 미지원
        composed_transforms = transforms.Compose([
            transforms.ToTensor() #최소 최대 정규화 ([0, 1])
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
            if not isinstance(annotations, list):
                annotations = [annotations]
            labels = []
            for sub_annotations in annotations:
                label = self.get_label(sub_annotations)
                labels.append(label)
            '''
            if return_tensors == 'pt':
                images = torch.stack(images)
            return {'pixel_values': images, 'labels': labels}
            '''
            #'''
            return BatchFeature(data={'pixel_values': images, 'labels': labels}, tensor_type=return_tensors)
            #'''

    def get_label(self, sub_annotations):
        #print(sub_annotations) #[{'bbox': [34.5299987793, 556.8300170898, 401.4400024414, 276.2600097656], 'category_id': 0}]
        boxes = []
        labels = []
        for sub_annotation in sub_annotations:
            #print(annotation) #{"bbox":[34.5299987793, 556.8300170898, 401.4400024414, 276.2600097656], "category_id":0}
            x = sub_annotation['bbox'][0] #데이타셋 (coco) #x, y, w, h
            y = sub_annotation['bbox'][1]
            w = sub_annotation['bbox'][2]
            h = sub_annotation['bbox'][3]
            sub_annotation['bbox'][0] = x #x1 #모델 (pascal_voc) #min_x, min_y, max_x, max_y
            sub_annotation['bbox'][1] = y #x2
            sub_annotation['bbox'][2] = x + w #x2
            sub_annotation['bbox'][3] = y + h #y2
            boxes.append(sub_annotation['bbox'])
            labels.append(sub_annotation['category_id'] + 1) #torchvision.models.detection.fasterrcnn_resnet50_fpn 에서는 0 (백그라운드), 1 부터        
        return {'boxes': boxes, 'labels': labels} 

    def post_process_object_detection(self, outputs, threshold=0.5, target_sizes=None):
        results = []
        for boxes, labels, scores in zip(outputs['boxes'], outputs['labels'], outputs['scores']):
            boxes_ = boxes[scores > threshold]
            labels_ = labels[scores > threshold]
            scores_ = scores[scores > threshold]
            results.append({"scores": scores_, "labels": labels_, "boxes": boxes_})
        return results

#오토 이미지 프로세서에 등록
AutoImageProcessor.register(FasterRcnnImageProcessor, FasterRcnnImageProcessor)
