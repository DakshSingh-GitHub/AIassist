from core.listener import listener
from core.nlp import get_intent, suggest_intents
from core.executor import execute, SAFE_INTENTS
from core.memory import init_db, get_most_used_intent, allow_auto_confirmation, is_auto_confirmed, get_intent_count

CONFIDENCE_THRESHOLD = 7
VOICE_MODE = True

def confirm_best_guess(intent: str):
	if is_auto_confirmed(intent):
		return True

	response = input(
		f"Assistant: You usually mean '{intent}'. Should I execute it? (yes/no/always): "
	).lower()
	if response == "always":
		allow_auto_confirmation(intent)
		return True

	return response.lower() in ('yes', 'y')

def main():
	print("Assistant: Online and waiting for command: ")
	running = True
	init_db()

	while running:
		command = listener("voice" if VOICE_MODE else "text")

		if not command:
			continue

		intent = get_intent(command)
		if intent == "UNKNOWN":
			suggestions = suggest_intents(command)

			if not suggestions:
				print("Assistant: Sorry, I didn't understand that.")
				continue

			best = get_most_used_intent(suggestions)

			# Case 1: We have a confident best guess
			if best:
				# Auto-execute only if safe AND trusted
				if best in SAFE_INTENTS:
					if confirm_best_guess(best):
						running = execute(best)
					else:
						print("Assistant: Okay, not executing anything.")
				else:
					# Dangerous intent → always ask explicitly
					print(f"Assistant: Did you mean {suggestions}?")
			else:
				# Case 2: No usage data yet
				print(f"Assistant: Did you mean {suggestions}?")

			continue
		running = execute(intent, command)


if __name__ == "__main__":
	main()
