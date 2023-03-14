from lib.preprocessing.preprocessor import Preprocessor
from lib.preprocessing.tokenizer import Tokenizer
from lib.extraction.extractor_wrapper import Extractor
from lib.extraction.extractor_spacy import ExtractorSpaCy
from lib.embeddings.embedder import Embedder
from lib.embeddings.embedder_bert import EmbedderBERT
from intent_classification.intent_classifier import Classifier
from intent_classification.intent_dialog_act_clss_torch import ClassifierDA
from intent_classification.intent_classification_model import IntentClassificationModel

generic_dataset_path = "./datasets/data_full.json"
embedder_train_dataset_path = "./datasets/glove.6B.100d.txt"

class Tools():
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.preprocessor = Preprocessor()
        self.extractor: Extractor = ExtractorSpaCy()
        self.embedder: Embedder = EmbedderBERT()
        self.dialog_act_classifier: Classifier = ClassifierDA()
        self.general_intent_classifier: Classifier = IntentClassificationModel()

