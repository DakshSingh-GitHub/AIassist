
from skills.system_control import open_browser, shutdown, open_app
from core.memory import record_intent, remove_auto_confirm, clear_all_autoconfirm
import os

DANGEROUS_INTENT = {"SHUTDOWN", "RESET_ALL_TRUST", "DISABLE_AUTO_CONFIRM"}
SAFE_INTENTS = {"OPEN_BROWSER", "EXIT"}

def confirm_action(intent:str):
	response = input(f"Are you sure ? {intent}: (y/n): ")
	return response.lower() in ('yes', 'y')

def execute(intent, command = None):
	if intent == "OPEN_BROWSER":
		print("Assistant: Opening Edge")
		open_browser()
		record_intent(intent)

	elif intent == "SHUTDOWN":
		if confirm_action(intent):
			print("Assistant: Shutting down")
			shutdown()
			record_intent(intent)
		else:
			print("Assistant: Cancelled")

	elif intent == "DISABLE_AUTO_CONFIRM":
		from core.nlp import extract_intent_name
		from core.memory import get_all_autoconfirms

		trusted = get_all_autoconfirms()
		target = extract_intent_name(command, trusted)

		if target:
			remove_auto_confirm(target)
			print(f"Assistant: Disabled 'always allow' for {target}.")
		else:
			print("Assistant: Redo")

	elif intent == "OPEN_APP":
		from core.nlp import extract_slot
		app = extract_slot(command, intent)
		if not app:
			print("Assistant: What should I open? This app doesn't exist")
		else:
			print(f"Assistant: Opening {app}")
			open_app(app)
			record_intent(intent)

	elif intent == "SHOW_TRUSTED_INTENTS":
		from core.memory import get_all_autoconfirms
		trusted = get_all_autoconfirms()
		if not trusted:
			print("Assistant: No trusted intents available")
		else:
			print("Assistant: Trusted Intents:")
			for t in trusted:
				print(f"\t - {t}")


	elif intent == "RESET_ALL_TRUST":
		clear_all_autoconfirm()
		print("Assistant: All trusted intents have been reset.")

	elif intent == "EXIT":
		print("Assistant: GoodBye")
		return False

	else:
		print("Assistant: Unknown command")
	return True

