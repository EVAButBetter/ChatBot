import os
import io
import sys
sys.path.append("..")

import pandas as pd
from Intent import Intent
from lib.parsing.parser_yml import ParserYML

# from text_generation_module import text_generation_function


class AiIntent(Intent):
    def __init__(self, name, database) -> None:
        super(AiIntent).__init__()
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
        (type, initial_value, action, mappings, required, value) = self.slots[slot_name].values()
        print(type, initial_value, action, mappings, required, value)
        return type, initial_value, action, mappings, required, value

    def fill_slot(self, slot_name, slot_value):
        if not self.confirm(slot_name, slot_value):
            print("confirm return false")
            return
        if not self.check_value(slot_name, slot_value):
            print("value not in database")
            return False
        self.slots[slot_name]["initial_value"] = None
        self.slots[slot_name]["value"] = slot_value
        # print("current slot value: ", self.slots[slot_name])
        return True

    def check_value(self, slot_name, slot_value):
        if slot_value in self.data[slot_name].values:
            return True
        else:
            return False
        
    def check_slot(self):
        for i, slot_name in enumerate(self.slots):
            slot = self.slots[slot_name]
            if slot["initial_value"] == "<REQUEST>" and slot["required"]:
                return False
            else:
                return True
            
    def get_all_slots(self):
        for i, slot_name in enumerate(self.slots):
            slot = self.slots[slot_name]
            if slot["initial_value"] is None:
                yield (slot_name, slot["value"])
                
    def request(self, slot_name):

        # res =  text_generation_function(self.name, slot_name)
        # return res
        
        # e.g.
        request_text = "request(name=?)"
        print("{}:{}".format(self.name,request_text))
        
        return slot_name


    def confirm(self, slot_name, slot_value):
        # res = text_generation_function(self.name, slot_name, slot_value)
        # return res
        
        # e.g.
        confirm_text = "confirm({}={})".format(slot_name, slot_value)
        print("{}:{}".format(self.name,confirm_text))
        return True
    
    def inform(self):
        # e.g.
        if not self.check_slot():
            return  False
        
        packs = self.get_all_slots()
        inform_text = ""
        
        for (name, value) in packs:
            inform_text += '"{}={}",'.format(name,value)
            
        inform_text = "inform(" + inform_text + ")"
        print(inform_text)
            
        # else:
            # res = text_generation_function(self.name, slot_name, slot_value)
            # return res
            
        
        
        

