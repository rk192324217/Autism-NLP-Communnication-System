import json
import os

USER_FILE = "data/users.json"


def load_users():
    if not os.path.exists(USER_FILE):
        return {}

    with open(USER_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)


def register_user(username, password, role):
    users = load_users()

    if username in users:
        return False

    users[username] = {
        "password": password,
        "role": role
    }
    save_users(users)
    return True


def authenticate_user(username, password):
    users = load_users()
    return username in users and users[username]["password"] == password
