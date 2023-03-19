from builder.tools import Tools
import warnings

warnings.filterwarnings("ignore")


class Builder:
    def __init__(self, tools: Tools):
        self.tools = tools

    def build(self, text):
        tokenized_text = self.tools.tokenizer.tokenize_sent(text)
        tokenized_sent = self.tools.tokenizer.tokenize(tokenized_text)
        preprocessed_text = [self.tools.preprocessor.reconstruct(self.tools.preprocessor.preprocess(tokens)) for tokens
                             in tokenized_sent]

        # We assemble back all sentences because we assume that they are related
        one_paragraph = [' '.join(preprocessed_text)]
        preprocessed_text_dict = [{'sentence': sent} for sent in one_paragraph]
        extracted_sentence_data = self.tools.extractor.extract_sent(one_paragraph)

        # sentence_embeddings = self.tools.embedder.encode(one_paragraph)

        # dialog_acts = [self.tools.dialog_act_classifier.predict(emb.get('embedding')) for emb in sentence_embeddings]
        intents_generic = [self.tools.general_intent_classifier.predict(text) for text in one_paragraph]

        result = []
        for i in range(len(preprocessed_text_dict)):
            result.append(
                {**preprocessed_text_dict[i], **extracted_sentence_data[i],# **sentence_embeddings[i], **dialog_acts[i],
                 **intents_generic[i]})
        return (result)

# print(Builder(Tools()).build("Hello World. how are yo?"))

# import time
#
# tools = Tools()
# from lib.extraction.extractor_spacy import ExtractorSpaCy
# tools.extractor = ExtractorSpaCy()
# builder = Builder(tools)
# tmp = time.time()
# print(builder.build("Hello World World World. Flight at 12:00, how are you professor Bonada Sanjaume Jordi?"))
# print(time.time()-tmp)
# from lib.extraction.extractor_nltk import ExtractorNLTK
# tools.extractor = ExtractorNLTK()
# tmp = time.time()
# print(Builder(tools).build("Hello World. how are yo?"))
# print(time.time()-tmp)

