from transformers import PretrainedConfig
from transformers import PreTrainedModel
from transformers import AutoModel
from transformers import AutoConfig
from transformers import AutoModelForObjectDetection
import torch
import transformers
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.faster_rcnn import FasterRCNN_ResNet50_FPN_Weights
from torchvision.models.detection import FasterRCNN
from torchvision.models.detection.rpn import AnchorGenerator
from torchvision.models.detection._utils import Matcher
from torchvision.ops.boxes import box_iou
from .configuration_faster_rcnn import FasterRcnnConfig

class FasterRcnnForObjectDetection(PreTrainedModel):
    config_class = FasterRcnnConfig

    def __init__(self, config):
        super().__init__(config)
        # load a model; pre-trained on COCO
        weights = FasterRCNN_ResNet50_FPN_Weights.COCO_V1 
        self.model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights=weights)
        # get number of input features for the classifier
        in_features = self.model.roi_heads.box_predictor.cls_score.in_features
        #num_classes = 2  # 1 class (early_printed_illustration) + background
        # replace the pre-trained head with a new one
        self.model.roi_heads.box_predictor = FastRCNNPredictor(in_features, config.num_labels)

    def forward(self, pixel_values, labels=None):
        if labels == None:
            outputs = self.model(pixel_values)
            boxes = []
            labels = []
            scores = []
            for output in outputs:
                boxes.append(output['boxes'])
                labels.append(output['labels'])
                scores.append(output['scores'])
            return transformers.file_utils.ModelOutput({'boxes': boxes, 'labels': labels, 'scores': scores})
        else:
            if self.training: #train
                loss_dict = self.model(pixel_values, labels)
                #print(loss_dict) #[{'boxes': tensor([], device='cuda:0', size=(0, 4)), 'labels': tensor([], device='cuda:0', dtype=torch.int64), 'scores': tensor([], device='cuda:0')}, {'boxes': tensor([], device='cuda:0', size=(0, 4)), 'labels': tensor([], device='cuda:0', dtype=torch.int64), 'scores': tensor([], device='cuda:0')}]
                #print(loss_dict.keys()) #dict_keys(['loss_classifier', 'loss_box_reg', 'loss_objectness', 'loss_rpn_box_reg'])
                #print(loss_dict.values()) #dict_values([tensor(0.7016, grad_fn=<NllLossBackward0>), tensor(0.6681, grad_fn=<DivBackward0>), tensor(4.9426, grad_fn=<BinaryCrossEntropyWithLogitsBackward0>), tensor(0.1818, dtype=torch.float64, grad_fn=<DivBackward0>)])
                loss = sum([loss for loss in loss_dict.values()])
                self.model.eval()
                outputs = self.model(pixel_values)
                boxes = []
                labels = []
                scores = []
                for output in outputs:
                    boxes.append(output['boxes'])
                    labels.append(output['labels'])
                    scores.append(output['scores'])
                self.model.train()
                return transformers.file_utils.ModelOutput({'loss': loss, 'boxes': boxes, 'labels': labels, 'scores': scores})
            else: #validation
                self.model.train()
                loss_dict = self.model(pixel_values, labels)
                loss = sum([loss for loss in loss_dict.values()])
                self.model.eval()
                outputs = self.model(pixel_values)
                boxes = []
                labels = []
                scores = []
                for output in outputs:
                    boxes.append(output['boxes'])
                    labels.append(output['labels'])
                    scores.append(output['scores'])
                return transformers.file_utils.ModelOutput({'loss': loss, 'boxes': boxes, 'labels': labels, 'scores': scores})

#오토 모델에 등록
AutoModelForObjectDetection.register(FasterRcnnConfig, FasterRcnnForObjectDetection)

