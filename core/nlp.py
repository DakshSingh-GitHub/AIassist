
import json
import os
import difflib

COMMAND_PATH = os.path.join("data", "commands.json")

CONTROL_INTENTS = {
    "DISABLE_AUTO_CONFIRM",
    "RESET_ALL_TRUST",
    "SHOW_TRUSTED_INTENTS"
}

KNOWN_APPS = {
    # 🌐 Browsers & Web
    "youtube": "https://www.youtube.com",
    "gmail": "https://mail.google.com",
    "google": "https://www.google.com",
    "github": "https://github.com",
    "stackoverflow": "https://stackoverflow.com",
    "reddit": "https://www.reddit.com",
    "twitter": "https://twitter.com",
    "linkedin": "https://www.linkedin.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",

    # 🧑‍💻 Developer Tools
    "leetcode": "https://leetcode.com",
    "codeforces": "https://codeforces.com",
    "codechef": "https://www.codechef.com",
    "hackerrank": "https://www.hackerrank.com",
    "geeksforgeeks": "https://www.geeksforgeeks.org",
    "gitlab": "https://gitlab.com",
    "bitbucket": "https://bitbucket.org",
    "npm": "https://www.npmjs.com",
    "pypi": "https://pypi.org",
    "replit": "https://replit.com",

    # 🧠 AI & Learning
    "chatgpt": "https://chat.openai.com",
    "gemini": "https://gemini.google.com",
    "kaggle": "https://www.kaggle.com",
    "coursera": "https://www.coursera.org",
    "udemy": "https://www.udemy.com",
    "edx": "https://www.edx.org",
    "brilliant": "https://brilliant.org",

    # 📁 Productivity
    "notion": "https://www.notion.so",
    "trello": "https://trello.com",
    "slack": "https://slack.com",
    "zoom": "https://zoom.us",
    "drive": "https://drive.google.com",
    "docs": "https://docs.google.com",
    "sheets": "https://sheets.google.com",
    "calendar": "https://calendar.google.com",

    # 🎵 Entertainment
    "spotify": "https://open.spotify.com",
    "netflix": "https://www.netflix.com",
    "prime": "https://www.primevideo.com",
    "hotstar": "https://www.hotstar.com",
    "twitch": "https://www.twitch.tv",

    # 🛒 Misc
    "amazon": "https://www.amazon.in",
    "flipkart": "https://www.flipkart.com",
    "maps": "https://maps.google.com",
    "weather": "https://weather.com"
}


def fuzzy_match(word: str, choices:list, cutoff=0.7):
    matches = difflib.get_close_matches(
        word, choices, n=1, cutoff=cutoff
    )
    return matches[0] if matches else None

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

def extract_slot(command: str, intent:str):
    command = normalize(command)
    if intent in {"SHUTDOWN", "RESET_ALL_TRUST", "DISABLE_AUTO_CONFIRM"}:
        return None
    for app in KNOWN_APPS:
        if app in command:
            return app
    words = command.split()
    for word in words:
        guess = fuzzy_match(word, list(KNOWN_APPS.keys()))
        if guess: return guess
    return None

