class IntentObject:
    def __init__(self, sentence_data, intent, dialog_act):
        self.sentence_data = sentence_data
        self.intent: dict = intent
        self.dialog_act: dict = dialog_act
        self.slots: dict = {}