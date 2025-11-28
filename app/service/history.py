import json
import os

HISTORY_FILE = "family_code_history.json"

def load_history():
    """Loads the family code history from the JSON file."""
    if not os.path.exists(HISTORY_FILE):
        return {"regular": [], "enterprise": []}

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure the structure is correct
            if not isinstance(data, dict):
                return {"regular": [], "enterprise": []}
            if "regular" not in data:
                data["regular"] = []
            if "enterprise" not in data:
                data["enterprise"] = []
            return data
    except (json.JSONDecodeError, IOError):
        return {"regular": [], "enterprise": []}

def save_history(history):
    """Saves the family code history to the JSON file."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)
    except IOError:
        print("Failed to save history file.")

def add_to_history(code: str, is_enterprise: bool = False):
    """Adds a new family code to the history."""
    if not code:
        return

    history = load_history()
    category = "enterprise" if is_enterprise else "regular"

    # Avoid duplicates and move to top
    if code in history[category]:
        history[category].remove(code)

    history[category].insert(0, code)

    # Limit history size (e.g., last 10)
    history[category] = history[category][:10]

    save_history(history)

def get_history(is_enterprise: bool = False):
    """Returns the list of family codes for the given category."""
    history = load_history()
    return history["enterprise" if is_enterprise else "regular"]
