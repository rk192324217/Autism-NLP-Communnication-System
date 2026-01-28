import json
import os
from datetime import datetime

LOG_FILE = "data/conversations.json"

def ensure_log_file():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

def load_logs():
    ensure_log_file()
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_logs(data):
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_conversation(caregiver_text, patient_text, metrics):
    logs = load_logs()
    logs.append({
        "timestamp": datetime.now().isoformat(),
        "caregiver": caregiver_text,
        "patient": patient_text,
        "metrics": metrics
    })
    save_logs(logs)
