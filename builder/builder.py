from builder.tools import Tools
import warnings

warnings.filterwarnings("ignore")
class Builder:
    def __init__(self,tools: Tools):
        self.tools = tools
    def build(self, text):
        tokenized_text = self.tools.tokenizer.tokenize_sent(text)
        tokenized_sent = self.tools.tokenizer.tokenize(tokenized_text)
        preprocessed_text = [ self.tools.preprocessor.reconstruct(self.tools.preprocessor.preprocess(tokens)) for tokens in tokenized_sent]
        # print(preprocessed_text)
        preprocessed_text_dict = [{'sentence': sent} for sent in preprocessed_text]
        extracted_sentence_data = self.tools.extractor.extract_sent(preprocessed_text)
        # print(extracted_sentence_data)
        sentence_embeddings = self.tools.embedder.encode(preprocessed_text)
        # print(sentence_embeddings)
        # TODO: make list of dicts from sentences and embeddings
        dialog_acts = [self.tools.dialog_act_classifier.predict(emb.get('embedding')) for emb in sentence_embeddings]
        intents_generic = [self.tools.general_intent_classifier.predict(text) for text in preprocessed_text]

        result = []
        for i in range(len(preprocessed_text_dict)):
            result.append({**preprocessed_text_dict[i], **extracted_sentence_data[i], **sentence_embeddings[i], **dialog_acts[i], **intents_generic[i]})
        return(result)


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


# list1 = [{"A": 1, "B": 2}, {"C": 3, "D": 4}]
# list2 = [{"E": 5, "F": 6}, {"G": 7, "H": 8}]
#
# result = []
# for i in range(len(list1)):
#     result.append({**list1[i], **list2[i]})
#
# print(result)