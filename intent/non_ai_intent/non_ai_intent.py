import os
import io
import sys
sys.path.append("..")

import pandas as pd
from Intent import Intent
from lib.parsing.parser_yml import ParserYML

# from text_generation_module import text_generation_function


class NonAiIntent(Intent):
    def __init__(self, name, database) -> None:
        super(NonAiIntent).__init__()
        """
        general intent class, link to domain.yml
        args:
        name: intent's name
        database: name of linked database
        self:
        name: intent's name
        parser: yml parser
        FILE_DIR: root file directory
        DATABASE_DIR: database .csv file dircetory
        data: data imported from .csv file
        CONFIG_DIF: config .yml file directory
        config: config imported from .yml file
        slots: slots import from .yml file 
        
        """
        self.name = name
        self.parser = ParserYML()
        self.FILE_DIR = "../data/"
        
        self.DATABASE = self.FILE_DIR + "database/" + database + ".csv"
        self.data = pd.read_csv(self.DATABASE, sep=";")
        self.CONFIG_DIR = self.FILE_DIR + "domains/domain.yml"
        self.config = self.parser.parse(self.CONFIG_DIR)
        self.slots = self.config["intents"][self.name]["slots"]

    def get_slot(self, slot_name):
        (type, initial_value, action, mappings) = self.slots[slot_name].values()
        
        return type, initial_value, action, mappings

    def fill_slot(self, slot_name, slot_value):
        if self.confirm(slot_name, slot_value) is False:
            return
        if self.check_value(slot_name, slot_value) is False:
            return False
        self.slots[slot_name]["initial_value"] = None
        print("current slot value: ", self.slots[slot_name])
        return True

    def check_value(self, slot_name, slot_value):
        if slot_value in self.data[slot_name].values:
            return True
        else:
            return False
        
    def check_slot(self):
        for i, slot_name in enumerate(self.slots):
            slot = self.slots[slot_name]
            if slot["initial_value"] == "<REQUEST>" and slot["isFilled"] is False:
                return slot_name
        return True

    def request(self):
        slot_name = self.check_slot()
        # if slot_name is not True:
            # res =  text_generation_function(self.name, slot_name)
            # return res
        return slot_name


    def confirm(self, slot_name, slot_value):
        print("confirm")
        return True
        # res = text_generation_function(self.name, slot_name, slot_value)
        # return res

    def inform(self):
        print("inform")
        return True
        # if self.check_slot() is False:
            # return False
        # else:
            # res = text_generation_function(self.name, slot_name, slot_value)
            # return res

