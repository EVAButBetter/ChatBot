import yaml
import sys

def get_intent_slots(intent_name):
    with open("/Users/macbook_pro/Documents/GitHub/ChatBot/rasa_pipeline/domain.yml", "r") as f:
        domain = yaml.safe_load(f)
        slots = domain.get("slots", {})
        intent_slots = {}
        print(domain.get("intents", {}))
        # for intent, intent_data in domain.get("intents", {}).items():
        #     if intent == intent_name:
        #         intent_slots = intent_data.get("slots", {})
        #         break
        result = {}
        for slot_name, slot_data in slots.items():
            for mapping in slot_data.get('mappings', []):
                if intent_name == mapping.get('intent'):
                    slot_value = {
                        "type": slot_data.get('type'),
                        'value': slot_data.get('initial_value'),
                        "mappings": mapping,
                    }
                    result[slot_name] = slot_value
        return result



intent_name = "professor_info"
intent_slots = get_intent_slots(intent_name)
print(intent_slots)