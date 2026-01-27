import json
import os
import hashlib

USER_FILE = "data/users.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register_user(username, password, role):
    users = load_users()
    if username in users:
        return False

    users[username] = {
        "password": hash_password(password),
        "role": role
    }
    save_users(users)
    return True

def authenticate_user(username, password):
    users = load_users()
    if username not in users:
        return False

    return users[username]["password"] == hash_password(password)
