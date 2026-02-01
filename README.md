# AIassist

AIassist is a smart, console-based personal assistant written in Python. It helps automate system tasks, learns from your usage patterns, and supports customizable voice/text commands.

## Features

*   **Natural Language Processing**: Matches user commands to intents using a flexible keyword matching system.
*   **Smart Suggestions**: If a command isn't recognized, it suggests the most likely intent based on your past usage history.
*   **Safety & Trust System**:
    *   Distinguishes between "Safe" (e.g., Open Browser) and "Dangerous" (e.g., Shutdown) intents.
    *   Supports "Auto-confirmation" for frequently used safe commands (reply "always" to trust a command).
    *   Manage trusted commands via voice/text (Disable, Reset, Show trusted).
*   **System Control**:
    *   Open Web Browser (Edge).
    *   Shutdown PC.
*   **Persistence**: Uses SQLite to store usage statistics and user preferences.

## Installation

1.  Clone the repository.
2.  Ensure you have Python 3.x installed.
3.  No external dependencies are currently required (uses standard library `sqlite3`, `json`, `os`, `subprocess`).

## Usage

Run the main script to start the assistant:

```bash
python main.py
```

### Example Commands

*   **Open Browser**: "open edge", "launch browser"
*   **System**: "shutdown pc", "turn off pc"
*   **Manage Trust**:
    *   "show trusted intents"
    *   "disable always allow for open browser"
    *   "reset all trust"
*   **Exit**: "bye", "exit"

### Auto-Confirmation
When the assistant guesses your intent, it may ask for confirmation.
*   Reply `yes` to execute once.
*   Reply `always` to automatically execute this command in the future (only for safe intents).

## Configuration

### Commands
You can add or modify commands in `data/commands.json`.
Format:
```json
{
  "INTENT_NAME": ["phrase 1", "phrase 2"]
}
```

### Preferences
Browser preferences are stored in `data/preferences.json`.

## Project Structure

*   `main.py`: Entry point of the application.
*   `core/`: Core logic modules.
    *   `nlp.py`: Command parsing and intent recognition.
    *   `executor.py`: Command execution and safety checks.
    *   `memory.py`: Database management (SQLite).
    *   `listener.py`: Input handling.
*   `skills/`: Implementation of specific capabilities.
    *   `system_control.py`: System-level operations.
*   `data/`: Configuration and database files.
