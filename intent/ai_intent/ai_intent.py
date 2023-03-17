import os
import io
import sys

sys.path.append("..")


# from data.actions_slots.actions_slots import *
from intent.intent import Intent
from lib.parsing.parser_yml import ParserYML
from data.actions_slots.actions_slots import ActionsSlots

# from text_generation_module import text_generation_function
FILE_DIR = "../data/"
# DATABASE = FILE_DIR + "database/" + database + ".csv"
CONFIG_DIR = FILE_DIR + "domains/domain.yml"
SEPARATOR = '&'  # for sc-gpt

ACTION_SLOTS = ActionsSlots()
class AiIntent(Intent):
    def __init__(self, name) -> None:
        super(AiIntent).__init__()

        self.name = name
        self.slots = dict()
        parser = ParserYML()
        self.action_slots = ACTION_SLOTS
        config = parser.parse(CONFIG_DIR)

        for slot_name, slot_data in config["intents"][self.name]["slots"].items():
            slot_value = {
                'main': slot_data.get('main'),
                "type": slot_data.get('type'),
                'value': slot_data.get('initial_value'),
                'mappings': slot_data.get('mappings'),
            }
            if slot_data.get('action_slot'):
                slot_value['action_slot'] = slot_data.get('action_slot')
            self.slots[slot_name] = slot_value

    def update_slots(self, data):
        for slot_name, value in self.slots.items():
            for map in value['mappings'] or []:
                if map.get('type') == 'from_entity':
                    for element in data:
                        if map.get('entity') == element.get('entity') and self.slots[slot_name]['value'] is not None:
                            self.fill_slot(slot_name, element['value'])

        for slot_name, value in self.slots.items():

            if value.get('value') is None or value.get('value') == '<REQUEST>' and value.get('action_slot') is not None:

                function_name, parameter_names = value['action_slot'].split(",")
                parameter_values = [self.slots[p.strip()]['value'] for p in parameter_names.split(";")]

                self.fill_slot(slot_name, getattr(self.action_slots, function_name)(*parameter_values))

    def get_slot(self, slot_name):

        return self.slots[slot_name]

    def fill_slot(self, slot_name, slot_value):

        self.slots[slot_name]["value"] = slot_value

    def check_slot(self):
        for i, slot_name in enumerate(self.slots):
            slot = self.slots[slot_name]
            if slot["value"] == "<REQUEST>":
                return False
            else:
                return True

    def get_all_slots(self):
        for i, slot_name in enumerate(self.slots):
            slot = self.slots[slot_name]
            if slot["value"] is not None:
                yield (slot_name, slot["value"])

    def check_info(self):
        # check correctness of info in db through actions_slots
        for slot_name, value in self.slots.items():

            if (value.get('value') is not None) and (value.get('value') is not '<REQUEST>') and (value.get('action_slot') is not None):
                function_name, parameter_names = value['action_slot'].split(",")
                parameter_values = [self.slots[p.strip()]['value'] for p in parameter_names.split(";")]

                # if provided info isn't correct
                if self.get_slot(slot_name)['value'] != getattr(self.action_slots, function_name)(*parameter_values):
                    return False

        return True

    def confirm(self, slot_name, slot_value):

        return self.name + " { "+"confirm ( {} = {} )".format(slot_name, slot_value)+" } " + SEPARATOR

    def inform(self):

        packs = self.get_all_slots()
        inform_text = ""

        for (name, value) in packs:
            inform_text += '" {} = {} "; '.format(name, value)

        return self.name + " { "+"inform(" + inform_text + ") } " + SEPARATOR

    def request(self, slot_name):

        return self.name + " { "+"request ( {} = ? )".format(slot_name)+" } " + SEPARATOR

    def deny(self, slot_name):

        return self.name + " { "+"deny ( {} = ? )".format(slot_name)+" } " + SEPARATOR
