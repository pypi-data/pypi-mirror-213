from transformers import FeatureExtractionMixin
from transformers import AutoFeatureExtractor
from transformers import BatchFeature
import pickle
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator, Vectors
from transformers.utils import cached_file
from pathlib import Path

#token_type: word, split, subword, char
#language: en, de, ko
class TorchtextTokenizer(FeatureExtractionMixin):
    tokenizer = None
    vocab = None

    def __init__(
        self,
        token_type='word',
        language='en',
        min_freq=1,
        special_tokens=['<unk>', '<pad>'],
        default_token='<unk>',
        model_max_length=512,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.token_type = token_type
        self.language = language
        self.min_freq = min_freq
        self.special_tokens = special_tokens
        self.default_token = default_token
        self.vocab_size = None
        self.model_max_length = model_max_length

        if token_type == 'subword':
            TorchtextTokenizer.tokenizer = get_tokenizer('subword')
        elif token_type == 'char':
            TorchtextTokenizer.tokenizer = list 
        elif token_type == 'split':
            TorchtextTokenizer.tokenizer = str.split 
        else: #word
            if language == 'ko':
                import konlpy
                okt = konlpy.tag.Okt() 
                TorchtextTokenizer.tokenizer = okt.morphs
            else:  
                TorchtextTokenizer.tokenizer = get_tokenizer('spacy', language=self.language)

    #padding: False, True, 'max_length'
    def __call__(self, texts, padding=False, vocab_path=None, return_tensors=None, **kwargs):
        if TorchtextTokenizer.vocab == None and vocab_path != None:
            if Path(vocab_path).exists():
                vocab_file = f'{vocab_path}/vocab.pkl'
            else:
                #vocab_file = cached_file(path_or_repo_id='automatethem/imdb-text-classification', filename='vocab.pkl')
                vocab_file = cached_file(path_or_repo_id=vocab_path, filename='vocab.pkl')
                #print(vocab_file) #/root/.cache/huggingface/hub/models--automatethem--imdb-text-classification/snapshots/c588c4558da42a7c63fdb05bef68ecc35dc19710/vocab.pkl
            with open(vocab_file, 'rb') as f:
                TorchtextTokenizer.vocab = pickle.load(f)
        
        if not isinstance(texts, list):
            texts = [texts]
        
        batch_max_length = 0
        if padding == False:
            pass
        else:
            if padding == 'max_length':
                pass
            else: 
                for text in texts:
                    tokens = self.tokenize(text)
                    ids = TorchtextTokenizer.vocab(tokens)
                    if batch_max_length < len(ids):
                        batch_max_length = len(ids)

        input_ids = []
        for text in texts:
            print(text)
            tokens = self.tokenize(text)
            ids = TorchtextTokenizer.vocab(tokens)
            if padding == False or padding == None:
                pass
            else:
                if padding == 'max_length':
                    max_length = self.model_max_length
                    ids = ids + ([self.get_token_to_id()['<pad>']] * (max_length - len(ids)))
                else:    
                    max_length = batch_max_length
                    ids = ids + ([self.get_token_to_id()['<pad>']] * (max_length - len(ids)))
            input_ids.append(ids)

        '''
        if return_tensors == 'pt':
            ids = torch.from_numpy(ids)
        return {'input_ids': input_ids}
        '''
        #''' 
        return BatchFeature(data={'input_ids': input_ids}, tensor_type=return_tensors)
        #'''
    
    def tokenize(self, text):
        tokens = TorchtextTokenizer.tokenizer(text)
        return tokens

    def get_vocab(self):
        return TorchtextTokenizer.vocab

    def get_token_to_id(self):
        return TorchtextTokenizer.vocab.get_stoi()
    
    def get_id_to_token(self):
        return TorchtextTokenizer.vocab.get_itos()
     
    def convert_tokens_to_ids(self, tokens):
        return [TorchtextTokenizer.vocab(tokens)]

    def convert_ids_to_tokens(self, ids):
        id_to_token = self.get_id_to_token()
        return [id_to_token[id] for id in ids]

    def train_from_iterator(self, text_iterator):
        def tokens_iterator():
            for text in text_iterator:
                tokens = TorchtextTokenizer.tokenizer(text)
                yield tokens
        vocab = build_vocab_from_iterator(tokens_iterator(), min_freq=self.min_freq, specials=self.special_tokens)
        #print(vocab)
        vocab.set_default_index(vocab[self.default_token]) # This index will be returned when OOV token is queried.
        self.vocab_size = len(vocab)
        #print(self.vocab_size) #204
        TorchtextTokenizer.vocab = vocab

    #https://github.com/huggingface/transformers/blob/c8f35a9ce37bd03f37fcf8336172bdcbe7ffc86a/src/transformers/feature_extraction_utils.py#L333
    def save_pretrained(self, save_directory, push_to_hub=False, **kwargs):
        #print(save_directory) #/content/drive/MyDrive/models/pytorch/models/bank-loan-model-for-tabular-classification
        vocab_file = f'{save_directory}/vocab.pkl'
        with open(vocab_file, 'wb') as f:
            pickle.dump(TorchtextTokenizer.vocab, f)
        return super().save_pretrained(save_directory, push_to_hub, **kwargs)
    
#오토 특성 추출기에 등록
AutoFeatureExtractor.register(TorchtextTokenizer, TorchtextTokenizer)
