
import json
import os

COMMAND_PATH = os.path.join("data", "commands.json")

CONTROL_INTENTS = {
    "DISABLE_AUTO_CONFIRM",
    "RESET_ALL_TRUST",
    "SHOW_TRUSTED_INTENTS"
}

def load_commands():
    with open(COMMAND_PATH, "r") as f:
        return json.load(f)

COMMANDS = load_commands()

def normalize(text: str): return text.lower().strip()

def get_intent(command: str):
    command = normalize(command)

    best_match = None
    best_length = 0

    for intent, phrases in COMMANDS.items():
        for phrase in phrases:
            if phrase in command:
                if len(phrase) > best_length:
                    best_match = intent
                    best_length = len(phrase)

    return best_match if best_match else "UNKNOWN"



def suggest_intents(command:str):
    suggestions = []
    command = normalize(command)

    for intent, phrases in COMMANDS.items():
        for phrase in phrases:
            if any(word in phrase for word in command.split()):
                suggestions.append(intent)
                break

    return list(set(suggestions))

def extract_intent_name(command: str, known_intents: list):
    command = normalize(command)
    for intent in known_intents:
        if intent.lower().replace("_", " ") in command:
            return intent
    return None



