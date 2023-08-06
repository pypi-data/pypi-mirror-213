from transformers import Pipeline
from transformers.pipelines import PIPELINE_REGISTRY
from torch.nn import functional as F

class FixedLengthTranslationPipeline(Pipeline):
    def _sanitize_parameters(self, **kwargs):
        preprocess_kwargs = {}
        if 'vocab_path' in kwargs:
            preprocess_kwargs['vocab_path'] = kwargs['vocab_path']
        postprocess_kwargs = {}
        return preprocess_kwargs, {}, postprocess_kwargs

    def preprocess(self, inputs, vocab_path=None):
        return self.tokenizer(inputs, vocab_path=vocab_path, return_tensors=self.framework)        

    def _forward(self, model_inputs):
        return self.model(**model_inputs)

    def postprocess(self, model_outputs):
        logits = model_outputs['logits']
        #print(logits.shape) #torch.Size([1, 3, 9])

        probabilities = F.softmax(logits, dim=-1)
        probabilities = probabilities.argmax(axis=-1)
        results = []
        for probability in probabilities:
            #print(probability) #tensor([2, 4, 6])
            tokens = self.tokenizer.convert_ids_to_tokens(probability)
            translation_text = ' '.join(tokens)
            #print(translation_text) #i raise dog
            results.append({'translation_text': translation_text})         
        return results

PIPELINE_REGISTRY.register_pipeline('fixed-length-translation', 
                                    #pt_model=AutoModelForFixedLengthTranslation,
                                    pipeline_class=FixedLengthTranslationPipeline)
