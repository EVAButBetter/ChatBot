from generation.generator import TemplateGenerator
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
import warnings

warnings.filterwarnings("ignore")

# MODEL_DIR = '/Users/macbook_pro/Documents/GitHub/ChatBot/generation/model'
MODEL_DIR = 'igorktech/sc-gpt-upf'
class GPTModel():
    def __init__(self, model_name=MODEL_DIR):
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)


class TemplateGeneratorSCGPT(TemplateGenerator):
    def __init__(self, model=GPTModel()):
        self.model = model

    def generate_from_template(self, input, gpu=False, **kwargs):
        if gpu:
            device = "cuda:0"
        else:
            device = "cpu"
        self.model.model = self.model.model.to(device)
        self.model.model.eval()
        input_ids = self.model.tokenizer.encode(input, return_tensors='pt')
        with torch.no_grad():

            inputs = self.model.model.generate(input_ids, pad_token_id=self.model.tokenizer.eos_token_id, **kwargs)
        output_text = self.model.tokenizer.batch_decode(inputs, skip_special_tokens=True)
        return output_text

# print(TemplateGeneratorSCGPT().generate_from_template('inform ( name = Kojn Ljj ; location = 55.101 ; group  = AI&ML )',
#                    max_length=150,
#                    num_return_sequences=5,
#                    # no_repeat_ngram_size=2,
#                    repetition_penalty=1.0,
#                    top_p=0.92,
#                    temperature=1,
#                    do_sample=True,
#                    top_k=5,
#                    early_stopping=True
#                    ))
