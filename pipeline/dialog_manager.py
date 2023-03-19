from intent_classification.intent_classifier import Classifier
from intent_classification.intent_classification_model import IntentClassificationModel, index2id
from intent.non_ai_intent.intent_to_action import IntentToAction
from intent.intent import Intent
from intent.ai_intent.ai_intent import AiIntent

DOMAIN_DATASET_PATH = "data/datasets/nlu.yml"
EMBEDDER_TRAIN_DATASET_PATH = "data/datasets/glove.6B.100d.txt"
DOMAIN_MODEL_PATH = "intent_classification/models/domain_intent_classifier.h5"
DOMAIN_TOKENIZER_PATH = "intent_classification/utils/domain_tokenizer.pkl"
DOMAIN_LABEL_ENCODER_PATH = "intent_classification/utils/domain_label_encoder.pkl"

intent_classification_domain = IntentClassificationModel(embedder_train_data_path=EMBEDDER_TRAIN_DATASET_PATH,
                                                         domain_dataset_path=DOMAIN_DATASET_PATH,
                                                         model_path=DOMAIN_MODEL_PATH,
                                                         tokenizer_path=DOMAIN_TOKENIZER_PATH,
                                                         label_encoder_path=DOMAIN_LABEL_ENCODER_PATH)


def load_intent_to_action():
    actions_db_dir = "intent/non_ai_intent/intent_to_action.json"
    intent_to_action = IntentToAction(actions_db_dir)
    return intent_to_action


intent_to_action = load_intent_to_action()


class DialogManager:
    def __init__(self):
        self.domain_intent_classifier: Classifier = intent_classification_domain
        self.current_ai_intent_obj = None

    def update(self, sentence_data, step_num=1):  # -> text, next step_num, ai generation?
        # for sentence_data in sentence_data:
        if step_num == 0:
            return "Thank you for your questions! It was pleasure for me to help you!", 1, False
        elif step_num == 1:

            intent_name = sentence_data['intent'][
                'value']  # self.domain_intent_classifier.predict(sentence_data['intent']['value'])['intent']['value']

            if intent_name == "upf":
                intent_obj = self.domain_intent_classifier.predict(sentence_data['sentence'])
                domain_intent_name = index2id(intent_obj["intent"]['value'])
                # print('domain intent ', domain_intent_name)
                self.current_ai_intent_obj = AiIntent(domain_intent_name)
                # print("sentence_data_data[data] ", sentence_data['data'])
                self.current_ai_intent_obj.update_slots(sentence_data['data'])

                # if not all slots are filled
                if not self.current_ai_intent_obj.check_slot():
                    for i, slot_name in enumerate(self.current_ai_intent_obj.slots):
                        slot = self.current_ai_intent_obj.slots[slot_name]

                        # check if we should get this slot from user
                        if slot["value"] == "<REQUEST>" and slot.get('main') is True:
                            # prevent looping for request info
                            if slot['n_request'] >= 1:
                                slot['n_request'] -= 1
                                return self.current_ai_intent_obj.request(slot_name), 2, True
                            else:
                                return self.current_ai_intent_obj.deny(slot_name), 1, True


                # if slots are filled
                else:
                    # if info is false
                    if not self.current_ai_intent_obj.check_info():
                        for i, slot_name in enumerate(self.current_ai_intent_obj.slots):
                            slot = self.current_ai_intent_obj.slots[slot_name]
                            if slot.get('main') is True:
                                return self.current_ai_intent_obj.deny(slot_name), 1, True

                    else:
                        return self.current_ai_intent_obj.inform(), 1, True


            # if intent not about upf
            else:
                non_ai_response, next_action = intent_to_action.run_action_by_intent(intent_name)

                return non_ai_response, next_action, False

            return 'Exuse me, something went wrong', 1, False

        elif step_num == 2:

            self.current_ai_intent_obj.update_slots(sentence_data['data'])

            # if not all slots are filled
            if not self.current_ai_intent_obj.check_slot():
                for i, slot_name in enumerate(self.current_ai_intent_obj.slots):
                    slot = self.current_ai_intent_obj.slots[slot_name]

                    # check if we should get this slot from user
                    if slot["value"] == "<REQUEST>" and slot.get('main') is True:
                        # prevent looping for request info
                        if slot['n_request'] >= 1:
                            slot['n_request'] -= 1
                            return self.current_ai_intent_obj.request(slot_name), 2, True
                        else:
                            return self.current_ai_intent_obj.deny(slot_name), 1, True

            # if slots are filled
            else:
                # if info is false
                if not self.current_ai_intent_obj.check_info():
                    for i, slot_name in enumerate(self.current_ai_intent_obj.slots):
                        slot = self.current_ai_intent_obj.slots[slot_name]
                        if slot.get('main') is True:
                            return self.current_ai_intent_obj.deny(slot_name), 1, True

                else:
                    return self.current_ai_intent_obj.inform(), 1, True
