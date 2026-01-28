import json
import os
import time

LOG_FILE = "data/conversations.json"


def log_conversation(caregiver, patient, metrics):
    entry = {
        "timestamp": time.time(),
        "caregiver": caregiver,
        "patient": patient,
        "metrics": metrics
    }

    if not os.path.exists(LOG_FILE):
        data = []
    else:
        try:
            with open(LOG_FILE, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []

    data.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)
