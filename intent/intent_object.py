class IntentObject:
    def __init__(self, intent, dialog_act):
        self.intent = intent
        self.dialog_act = dialog_act
        self.slots: dict = {}
