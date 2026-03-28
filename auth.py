import json
import hashlib
import os

USERS_FILE = "users.json"

def _load():
    if not os.path.exists(USERS_FILE):
        return {"users": []}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def _save(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def _hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(name, username, email, phone, password):
    data = _load()

    for u in data["users"]:
        if u["username"] == username or u["email"] == email:
            return False, "Username or Email already exists"

    data["users"].append({
        "name": name,
        "username": username,
        "email": email,
        "phone": phone,
        "password": _hash(password)
    })

    _save(data)
    return True, "Registration successful"

def authenticate_user(username, password):
    data = _load()
    hashed = _hash(password)

    for u in data["users"]:
        if u["username"] == username and u["password"] == hashed:
            return True, u["name"]

    return False, None
