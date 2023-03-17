import pyjokes, randfacts
from .action import Action


class Fun(Action):
    def run(self, action_obj):
        type = action_obj["type"]
        if type == 'fact':
            return randfacts.get_fact()
        elif type == "joke":
            return pyjokes.get_joke()
