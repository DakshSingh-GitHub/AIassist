import os
import subprocess
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PREF_PATH = os.path.join(BASE_DIR, 'data', 'preferences.json')

def get_default_browser():
	with open(PREF_PATH, 'r') as f:
		prefs = json.load(f)
	return prefs.get('default_browser', 'edge')

def open_browser():
	browser = get_default_browser()
	if browser == 'edge':
		subprocess.Popen("C:/Program Files (x86)/Microsoft/Edge/Application/msedge")
	else:
		subprocess.Popen(browser)

def shutdown():
	os.system("shutdown /s /t 5")

def open_app(app_name):
	from core.nlp import KNOWN_APPS
	import subprocess

	url = KNOWN_APPS.get(app_name)
	if url:
		subprocess.Popen(["C:/Program Files (x86)/Microsoft/Edge/Application/msedge", url])