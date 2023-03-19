from lib.extraction.extractor_wrapper import Extractor
from lib.parsing.parser import Parser
from lib.parsing.parser_yml import ParserYML
from spacy.tokens import Doc
import spacy
from spacy.util import minibatch, compounding
from spacy.training.example import Example
import warnings
import random
from pathlib import Path
from tqdm import tqdm
import os
import re

# pip install -U spacy
# python -m spacy download en_core_web_sm

spacy.util.fix_random_seed(42)
MODEL_PATH = 'models/ner_en_core_web_sm_mixed'  # os.path.join(os.path.dirname(os.getcwd()),
# os.path.join("models", 'ner'))
# print(MODEL_PATH)
ENTITY_RE = re.compile(r'\[(.+?)\]\((.+?)\)')


class ExtractorSpaCy(Extractor):
    def __init__(self, model_name=MODEL_PATH):
        super().__init__()

        try:
            self.model = spacy.load(model_name)
        except:
            warning = "Can't find model {}  loading en_core_web_sm".format(model_name)
            warnings.warn(warning)
            self.model = spacy.load('en_core_web_sm')

    def extract_sent(self, sent):
        if isinstance(sent, str):
            sents = self.model(sent)
            output_list = {"data": [{'value': e.text, 'entity': e.label_} for e in sents.ents]}
            return output_list
        elif isinstance(sent, list):
            output_list = [
                {"data": [{'entity': ent.label_, 'start': ent.start_char, 'end': ent.end_char, 'value': ent.text,
                           'extractor': 'SpaCy'} for ent in
                          self.model(sentence).ents]} for
                sentence in sent]
            return output_list

    def extract_tokens(self, tokens, ner=True, pos=True, morph=True, lemma=True, skip_empty=True):
        output_list = []
        for sent_tokens in tokens:
            doc = Doc(nlp.vocab, words=sent_tokens)
            doc = self.model(doc)

            for i, token in enumerate(doc):
                word = {"value": token.text}
                if ner:
                    word["entity"] = token.ent_type_

                if pos:
                    word["pos"] = token.pos_
                if lemma:
                    word["lemma"] = token.lemma_

                if word["entity"] and skip_empty:
                    output_list.append({"data": word})

        return output_list

    def convert_rasa_to_spacy(self, nlu_file, parser: Parser = ParserYML(), case=2):
        data = parser.parse(nlu_file)
        sentences = []
        for intent in data['nlu']:
            for example in intent['examples'].split('\n'):
                example_str = example.lstrip('- ')

                # choose register
                if case == 0:
                    text = ENTITY_RE.sub(r'\1', example_str).lower()  # Remove entity labels and brackets
                elif case == 1:
                    text = ENTITY_RE.sub(r'\1', example_str).title()
                elif case == 2:
                    random_case = random.randint(0, 2)
                    if random_case == 0:
                        text = ENTITY_RE.sub(r'\1', example_str).lower()
                    elif random_case == 1:
                        text = ENTITY_RE.sub(r'\1', example_str).title()
                    elif random_case == 2:
                        text = ENTITY_RE.sub(r'\1', example_str)
                else:
                    text = ENTITY_RE.sub(r'\1', example_str)

                entities = []
                for match in ENTITY_RE.finditer(example_str):
                    entity_text = match.group(1)
                    entity_label = match.group(2)
                    start_index = match.start(1)
                    end_index = match.end(1)
                    entities.append((start_index - 1,
                                     end_index - 1,
                                     # "value": entity_text,
                                     entity_label
                                     ))
                training_data = (text, {"entities": entities})
                if (entities != []):
                    sentences.append(training_data)
        return sentences

    def train_ner(self, output_dir, config_path,model_name, use_gpu = False, n_iter=80, case=0):
        print("Create model")
        if use_gpu:
            # spacy.util.use_gpu(0)
            spacy.prefer_gpu(0)
        if model_name is not None:
            self.model = spacy.load(model_name)
        else:
            warning = "Can't find model {}  loading blank en".format(model_name)
            warnings.warn(warning)
            self.model = spacy.blank('en')

        if 'ner' not in self.model.pipe_names:
            ner = self.model.create_pipe('ner')
            self.model.add_pipe('ner', last=True)
        else:
            ner = self.model.get_pipe('ner')
        data = self.convert_rasa_to_spacy(config_path, case=case)
        for _, annotations in data:
            for ent in annotations.get('entities'):
                ner.add_label(ent[2])

        other_pipes = [pipe for pipe in self.model.pipe_names if pipe != 'ner']
        with self.model.disable_pipes(*other_pipes):  # only train NER

            if model_name is not None:
                optimizer = self.model.create_optimizer()
            else:
                optimizer = self.model.begin_training()

            for itn in tqdm(range(n_iter)):
                random.shuffle(data)
                losses = {}
                # batch up the examples using spaCy's minibatch
                batches = minibatch(data, size=compounding(4.0, 64.0, 1.5))
                for batch in batches:
                    for text, annotations in batch:
                        # create Example
                        doc = self.model.make_doc(text)
                        example = Example.from_dict(doc, annotations)
                        # Update the model
                        self.model.update([example],sgd = optimizer, losses=losses, drop=0.3)
                print("Losses in iteration = {}".format(n_iter), losses)

        # Save model
        if output_dir is not None:
            output_dir = Path(output_dir)
            if not output_dir.exists():
                output_dir.mkdir()
            self.model.to_disk(output_dir)
            print("Saved model to", output_dir)


# ExtractorSpaCy().train_ner('../../models/ner_blank_en_mixed',
#                            '../../data/datasets/nlu.yml',
#                            model_name = None,
#                            use_gpu=True, n_iter=70, case=2)
