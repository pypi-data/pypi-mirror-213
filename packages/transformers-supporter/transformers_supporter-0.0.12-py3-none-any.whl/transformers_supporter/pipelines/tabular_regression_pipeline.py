from transformers import Pipeline
from transformers.pipelines import PIPELINE_REGISTRY

class TabularRegressionPipeline(Pipeline):
    def _sanitize_parameters(self, **kwargs):
        preprocess_kwargs = {}
        if "transformer_path" in kwargs:
            preprocess_kwargs["transformer_path"] = kwargs["transformer_path"]
        postprocess_kwargs = {}
        return preprocess_kwargs, {}, postprocess_kwargs

    def preprocess(self, inputs, transformer_path=None):
        return self.feature_extractor(inputs, transformer_path=transformer_path, return_tensors=self.framework)        

    def _forward(self, model_inputs):
        return self.model(**model_inputs)

    def postprocess(self, model_outputs):
        logits = model_outputs['logits']
        results = []
        for logit in logits:
            results.append({"logit": logit[0].item()})        
        return results

PIPELINE_REGISTRY.register_pipeline('tabular-regression', 
                                    #pt_model=AutoModelForTabularRegression
                                    pipeline_class=TabularRegressionPipeline)
