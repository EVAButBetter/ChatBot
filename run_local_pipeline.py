from intent_classification.intent_classification_model import IntentClassificationModel
from intent.non_ai_intent.intent_to_action import IntentToAction
import sys

GENERIC_DATASET_PATH = "./datasets/generic.yml"
DOMAIN_DATASET_PATH = "./datasets/domain.yml"
EMBEDDER_TRAIN_DATASET_PATH = "./datasets/glove.6B.100d.txt"
GENERIC_MODEL_PATH = "./intent_classification/models/generic_intent_classifier.h5"
GENERIC_TOKENIZER_PATH = "./intent_classification/utils/generic_tokenizer.pkl"
GENERIC_LABEL_ENCODER_PATH = "./intent_classification/utils/generic_label_encoder.pkl"
DOMAIN_MODEL_PATH = "./intent_classification/models/domain_intent_classifier.h5"
DOMAIN_TOKENIZER_PATH = "./intent_classification/utils/domain_tokenizer.pkl"
DOMAIN_LABEL_ENCODER_PATH = "./intent_classification/utils/domain_label_encoder.pkl"


def load_intent_classifiers():
    intent_classification_generic = IntentClassificationModel(embedder_train_data_path=EMBEDDER_TRAIN_DATASET_PATH,
                                                              domain_dataset_path=GENERIC_DATASET_PATH,
                                                              model_path=GENERIC_MODEL_PATH,
                                                              tokenizer_path=GENERIC_TOKENIZER_PATH,
                                                              label_encoder_path=GENERIC_LABEL_ENCODER_PATH)

    intent_classification_domain = IntentClassificationModel(embedder_train_data_path=EMBEDDER_TRAIN_DATASET_PATH,
                                                             domain_dataset_path=DOMAIN_DATASET_PATH,
                                                             model_path=DOMAIN_MODEL_PATH,
                                                             tokenizer_path=DOMAIN_TOKENIZER_PATH,
                                                             label_encoder_path=DOMAIN_LABEL_ENCODER_PATH)

    return intent_classification_generic, intent_classification_domain


def load_intent_to_action():
    actions_db_dir = "./text_generator/intent_to_action.json"
    intent_to_action = IntentToAction(actions_db_dir)
    return intent_to_action


def is_text_input():
    argv = sys.argv
    return len(argv) >= 2 and argv[1] == "text"


def get_transcription(input_type):
    if input_type == "text":
        eng_transcription = input('Type here:\n')
    else:
        #recording_path = recorder.listen()

        #lang, eng_transcription = speech_recognition_system.run(recording_path)
        raise AssertionError("Not expected this to be voice input...")
    return eng_transcription


def run_pipeline_step(step_num=1, input_type="text", output_type="text"):
    if step_num == 0:
        print("Session has ended.")
        exit()
    elif step_num == 1:
        eng_transcription = get_transcription(input_type=input_type)

        intent_obj = intent_classification_generic.predict(eng_transcription)

        intent_name = intent_obj["intent"]

        if intent_name == "upf":
            intent_obj = intent_classification_domain.predict(eng_transcription)
            intent_name = intent_obj["intent"]
            # TODO: CALL NON-AI BRANCH (FILL SLOTS, step 2)
            answer, next_action = "Non-ai branch still not implemented", 1
        else:
            answer, next_action = intent_to_action.run_action_by_intent(intent_name)

        print(answer)
        print("\n")
        # TODO: CHECK IF OUTPUT IS VOICE AND GENERATE IF SO

        return next_action

    elif step_num == 2:
        # TODO: FILL SLOTS
        assert NotImplementedError


if __name__ == "__main__":

    argv = sys.argv

    print("#### STARTING EVA...! ####\n")

    intent_classification_generic, intent_classification_domain = load_intent_classifiers()

    intent_to_action = load_intent_to_action()

    if is_text_input():
        ### TEXT INPUT / OUTPUT ###
        print("You have chosen text input, so please type your request (in English):\n")
        input_type = "text"

    else:
        ### LISTENING ###
        print("You have chosen audio input/output, so please make your request now to your microphone\n")
        input_type = "voice"

    next_step = 1
    while True:
        next_step = run_pipeline_step(step_num=next_step, input_type=input_type)
