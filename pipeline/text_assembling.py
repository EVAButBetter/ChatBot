from generation.generator import TemplateGenerator
from generation.sc_gpt.generator_scgpt import TemplateGeneratorSCGPT

from paraphrasing.paraphraser import Paraphraser
from paraphrasing.paraphraser_t5 import ParaphrasetT5

from random import choice

G_NUM_SEQ = 4
G_REP_PEN = 1.0
G_TOP_P = 0.92
G_DO_SAMPLE = True
G_TOP_K = 5
G_EARLY_STOPPING = True
G_MAX_LENGTH = 100
G_TEMPERATURE = 1

P_NUM_SEQ = 4
# P_REP_PEN = 1.0
P_TOP_P = 0.95
P_DO_SAMPLE = True
P_TOP_K = 50
P_EARLY_STOPPING = True
P_MAX_LENGTH = 100


class TextAssembler:
    def __init__(self):
        self.generator: TemplateGenerator = TemplateGeneratorSCGPT()
        self.paraphraser: Paraphraser = ParaphrasetT5()

    def assemble(self, text, ai_pipeline=False):
        assembled_text = text
        if ai_pipeline:
            assembled_text = self.generator.generate_from_template(assembled_text,
                                                                   do_sample=G_DO_SAMPLE,
                                                                   max_length=G_MAX_LENGTH,
                                                                   top_p=G_TOP_P,
                                                                   top_k=G_TOP_K,
                                                                   num_return_sequences=G_NUM_SEQ,
                                                                   early_stopping=G_EARLY_STOPPING,
                                                                   # no_repeat_ngram_size=2,
                                                                   repetition_penalty=G_REP_PEN,
                                                                   temperature=G_TEMPERATURE)
        assembled_text = self.paraphraser.paraphrase(choice(assembled_text),
                                                     do_sample=P_DO_SAMPLE,
                                                     max_length=P_MAX_LENGTH,
                                                     top_p=P_TOP_P,
                                                     top_k=P_TOP_K,
                                                     num_return_sequences=P_NUM_SEQ,
                                                     early_stopping=P_EARLY_STOPPING)

        return choice(assembled_text)
