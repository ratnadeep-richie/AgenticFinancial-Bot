import json
import os
from datetime import datetime


# ================= PROFILE =================

def save_profile(username, profile_data):
    os.makedirs("user_data", exist_ok=True)

    with open(f"user_data/{username}_profile.json", "w") as f:
        json.dump(profile_data, f, indent=4)


def load_profile(username):
    path = f"user_data/{username}_profile.json"

    if not os.path.exists(path):
        return None

    with open(path) as f:
        return json.load(f)


# ================= MONTHLY HISTORY =================

def save_month(username, expenses):
    os.makedirs("user_data", exist_ok=True)

    path = f"user_data/{username}_history.json"

    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
    else:
        data = []

    data.append({
        "month": datetime.now().strftime("%Y-%m"),
        "expenses": expenses
    })

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def load_history(username):
    path = f"user_data/{username}_history.json"

    if not os.path.exists(path):
        return []

    with open(path) as f:
        return json.load(f)


# ================= ALERT HISTORY =================

def save_alert(username, alert_msg, severity):
    os.makedirs("user_data", exist_ok=True)

    path = f"user_data/{username}_alerts.json"

    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
    else:
        data = []

    alert_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "severity": severity,
        "message": alert_msg
    }

    data.append(alert_entry)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def load_alerts(username):
    path = f"user_data/{username}_alerts.json"

    if not os.path.exists(path):
        return []

    with open(path) as f:
        return json.load(f)
