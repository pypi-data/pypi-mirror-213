from transformers import Pipeline
from transformers.pipelines import PIPELINE_REGISTRY
from torch.nn import functional as F

class TabularClassificationPipeline(Pipeline):
    def _sanitize_parameters(self, **kwargs):
        preprocess_kwargs = {}
        if "transformer_path" in kwargs:
            preprocess_kwargs["transformer_path"] = kwargs["transformer_path"]
        postprocess_kwargs = {}
        if "top_k" in kwargs:
            preprocess_kwargs["top_k"] = kwargs["top_k"]
        return preprocess_kwargs, {}, postprocess_kwargs

    def preprocess(self, inputs, transformer_path=None):
        return self.feature_extractor(inputs, transformer_path=transformer_path, return_tensors=self.framework)        

    def _forward(self, model_inputs):
        return self.model(**model_inputs)

    def postprocess(self, model_outputs, top_k=None):
        logits = model_outputs['logits']
        probabilities = F.softmax(logits, dim=-1)
        results = []
        for probability in probabilities:
            label = self.model.config.id2label[probability.argmax().item()]
            probability = probabilities[0][probability.argmax()]
            results.append({'label': label, 'score': probability.item()})   
        results.sort(key=lambda x: x['score'], reverse=True)
        if top_k != None:
            results = results[:top_k]            
        return results

PIPELINE_REGISTRY.register_pipeline('tabular-classification', 
                                    #pt_model=AutoModelForTabularClassification
                                    pipeline_class=TabularClassificationPipeline)
