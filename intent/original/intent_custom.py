from lib.parsing.parser import Parser
from lib.parsing.parser_yml import ParserYML
from intent.original.intent_object import IntentObject

DOMAIN_PATH = "../../data/domains/domain.yml"


class IntentCustom(IntentObject):
    def __init__(self, sentence_data, intent, dialog_act, parser: Parser = ParserYML()):
        super().__init__(sentence_data, intent, dialog_act)
        self.update_count = 0
        raw_data = parser.parse(DOMAIN_PATH)
        intent = raw_data['intents']
        for slot_name, slot_data in intent.get(self.intent['value']).get('slots').items():
            slot_value = {
                "type": slot_data.get('type'),
                'value': slot_data.get('initial_value'),
                'mappings': slot_data.get('mappings'),
            }
            if slot_data.get('action'):
                slot_value['action'] = slot_data.get('action')
            self.slots[slot_name] = slot_value


    def update_slots(self, data):
        for slot_name, value in self.slots.items():
            for map in value['mappings'] or []:
                if map.get('type') == 'from_entity':
                    for element in data.get('data'):
                        if map.get('entity') == element.get('entity') and self.slots[slot_name].get('value') is not None:
                            self.slots[slot_name]['value'] = element.get('value')


    def update_state(self, separator=" & "):
        inform_str = 'confirm( '
        if self.update_count > 0:
            inform_str = 'inform( '
        for slot_name, value in self.slots.items():

            # if no action request information
            if value.get('value') == '<REQUEST>' and value.get('action') is None:
                return f"request( {slot_name} = {'?'} )" + separator

            # Execute action if no value
            if value.get('value') is None or '<REQUEST>' and value.get('action') is not None:
                function_name, parameter_names = value['action'].split(",")
                parameter_values = [self.slots[p]['value'] for p in parameter_names.split(";")]

                # if all values are <REQUEST> - ask again about this item (order matters!)
                if any(a == '<REQUEST>' for a in parameter_values):
                    return f"request( {slot_name} = {'?'} )" + separator

                # Call the function with the input parameters
                self.slots['slot_name']['value'] = globals()[function_name](*parameter_values)

            inform_str += f"{slot_name} = {value.get('value')} ; "
        return inform_str + " )" + separator

# test_obj = IntentCustom({}, {'value': 'course_info'}, {'label': 'qw', 'prob': 0.965216875076294})
# print(test_obj.slots)
# print(test_obj.dialog_act)
# test_obj.update_slots({'data': [{'entity': 'PERSON', 'start': 40, 'end': 63,
#                                'value': 'Bonada Sanjaume Jordi ?', 'extractor': 'SpaCy'}]})
# print(test_obj.slots)
