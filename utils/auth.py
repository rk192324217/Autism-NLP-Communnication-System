import json
import os

USERS_FILE = "data/users.json"

def ensure_users_file():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump([], f)

def load_users():
    ensure_users_file()
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def register_user(username, password, role):
    users = load_users()
    for user in users:
        if user["username"] == username:
            return False
    users.append({
        "username": username,
        "password": password,
        "role": role
    })
    save_users(users)
    return True

def authenticate_user(username, password):
    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return user  # return full user dict instead of True
    return None
