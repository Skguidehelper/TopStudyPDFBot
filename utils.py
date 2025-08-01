# utils.py

import json
from config import DB_FILE  # ✅ Use shared config for path consistency

# ✅ Load database from JSON file
def load_data():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"admins": [], "premium_users": []}

# ✅ Save updated data to JSON file
def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ✅ Check if a user is admin
def is_admin(user_id):
    user_id = int(user_id)
    data = load_data()
    return user_id in data.get("admins", [])

# ✅ Check if a user is premium
def is_premium_user(user_id):
    user_id = int(user_id)
    data = load_data()
    return user_id in data.get("premium_users", [])

# ✅ Add a user to premium list
def add_premium_user(user_id):
    user_id = int(user_id)
    data = load_data()
    if user_id not in data.get("premium_users", []):
        data["premium_users"].append(user_id)
        save_data(data)
        return True
    return False

# ✅ (Optional) Remove a user from premium list
def remove_premium_user(user_id):
    user_id = int(user_id)
    data = load_data()
    if user_id in data.get("premium_users", []):
        data["premium_users"].remove(user_id)
        save_data(data)
        return True
    return False
