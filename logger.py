from datetime import datetime
import os

LOG_DIR = "logs"
LOG_FILE = "command_log.txt"

def log_action(user_input, intent, command, status, message=""):
    # 🔒 Defensive filesystem handling
    if os.path.exists(LOG_DIR):
        if not os.path.isdir(LOG_DIR):
            # 'logs' exists but is a FILE → remove it
            os.remove(LOG_DIR)

    os.makedirs(LOG_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = (
        f"[{timestamp}] | "
        f"INPUT: {user_input} | "
        f"INTENT: {intent} | "
        f"COMMAND: {command} | "
        f"STATUS: {status} | "
        f"MESSAGE: {message}\n"
    )

    log_path = os.path.join(LOG_DIR, LOG_FILE)

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(log_entry)
