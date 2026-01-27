import json
import os
from datetime import datetime

LOG_FILE = "data/conversations.json"

def log_conversation(caregiver_text, patient_text, metrics):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "caregiver": caregiver_text,
        "patient": patient_text,
        "metrics": metrics
    }

    # Ensure data directory exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    # Load existing data safely
    if not os.path.exists(LOG_FILE):
        data = []
    else:
        try:
            with open(LOG_FILE, "r") as f:
                content = f.read().strip()
                if not content:
                    data = []
                else:
                    data = json.loads(content)
        except json.JSONDecodeError:
            data = []

    data.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)
