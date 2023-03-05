from lib.parsing.parser import Parser
from lib.parsing.parser_yml import ParserYML
from intent.intent_object import IntentObject


class IntentCustom(IntentObject):
    def __init__(self, intent, dialog_act, config_file, parser: Parser = ParserYML()):
        super().__init__(intent, dialog_act)

        raw_data = parser.parse(config_file)
        slots = raw_data.get("slots", {})

        for slot_name, slot_data in slots.items():
            for mapping in slot_data.get('mappings', []):
                if self.intent.get('value') == mapping.get('intent'):
                    slot_value = {
                        "type": slot_data.get('type'),
                        'value': slot_data.get('initial_value'),
                        "entity": mapping.get('entity'),
                    }
                    self.slots[slot_name] = slot_value

    def fill_slots(self, data):
        for slot, value in self.slots.items():
            for element in data.get('data'):
                if value.get('entity') == element.get('entity'):
                    self.slots[slot].update(element)

# test_obj = IntentCustom({'value':'professor_info'},'qw',"/Users/macbook_pro/Documents/GitHub/ChatBot/rasa_pipeline/domain.yml")
# print(test_obj.slots)
# test_obj.fill_slots(    {'data': [{'entity': 'PERSON', 'start': 40, 'end': 63,
#                'value': 'Bonada Sanjaume Jordi ?', 'extractor': 'SpaCy'}]})
# print(test_obj.slots)
