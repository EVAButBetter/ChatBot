from lib.preprocessing.preprocessor import Preprocessor
from lib.preprocessing.tokenizer import Tokenizer
from lib.extraction.extractor_wrapper import Extractor
from lib.extraction.extractor_spacy import ExtractorSpaCy
from lib.embeddings.embedder import Embedder
from lib.embeddings.embedder_bert import EmbedderBERT
from intent_classification.intent_classifier import Classifier
from intent_classification.intent_dialog_act_clss_torch import ClassifierDA
from intent_classification.intent_classification_model import IntentClassificationModel

GENERIC_DATASET_PATH = "../data/datasets/generic.yml"
EMBEDDER_TRAIN_DATASET_PATH = "../data/datasets/glove.6B.100d.txt"
GENERIC_MODEL_PATH = "../intent_classification/models/generic_intent_classifier.h5"
GENERIC_TOKENIZER_PATH = "../intent_classification/utils/generic_tokenizer.pkl"
GENERIC_LABEL_ENCODER_PATH = "../intent_classification/utils/generic_label_encoder.pkl"



class Tools():
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.preprocessor = Preprocessor()
        self.extractor: Extractor = ExtractorSpaCy()
        self.embedder: Embedder = EmbedderBERT()
        self.dialog_act_classifier: Classifier = ClassifierDA()
        self.general_intent_classifier: Classifier = IntentClassificationModel(
            embedder_train_data_path=EMBEDDER_TRAIN_DATASET_PATH,
            domain_dataset_path=GENERIC_DATASET_PATH,
            model_path=GENERIC_MODEL_PATH,
            tokenizer_path=GENERIC_TOKENIZER_PATH,
            label_encoder_path=GENERIC_LABEL_ENCODER_PATH)
