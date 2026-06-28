import os
import json
import uuid
from datetime import datetime

# Local DB File Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "local_db.json")

def load_db():
    if not os.path.exists(DB_FILE):
        return {
            "users": [],
            "allergens": [],
            "foods": [],
            "symptoms": [],
            "medicines": [],
            "query_logs": []
        }
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {
            "users": [],
            "allergens": [],
            "foods": [],
            "symptoms": [],
            "medicines": [],
            "query_logs": []
        }

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# --- USER AUTH ENTITIES ---

def create_user(email, password_hash):
    db = load_db()
    # Check if user already exists
    for u in db["users"]:
        if u["email"].lower() == email.lower():
            return None
    user = {
        "id": str(uuid.uuid4()),
        "email": email,
        "password_hash": password_hash,
        "created_at": datetime.utcnow().isoformat()
    }
    db["users"].append(user)
    save_db(db)
    return user

def get_user_by_email(email):
    db = load_db()
    for u in db["users"]:
        if u["email"].lower() == email.lower():
            return u
    return None

def get_user_by_id(user_id):
    db = load_db()
    for u in db["users"]:
        if u["id"] == user_id:
            return u
    return None

# --- ALLERGENS ---

def get_allergens():
    db = load_db()
    return db["allergens"]

def get_allergen_by_id(allergen_id):
    db = load_db()
    for a in db["allergens"]:
        if a["id"] == allergen_id:
            return a
    return None

# --- FOODS ---

def get_foods():
    db = load_db()
    return db["foods"]

def get_food_by_id(food_id):
    db = load_db()
    for f in db["foods"]:
        if f["id"] == food_id:
            return f
    return None

# --- SYMPTOMS ---

def get_symptoms():
    db = load_db()
    return db["symptoms"]

def get_symptom_by_id(symptom_id):
    db = load_db()
    for s in db["symptoms"]:
        if s["id"] == symptom_id:
            return s
    return None

# --- MEDICINES ---

def get_medicines():
    db = load_db()
    return db["medicines"]

# --- QUERY LOGS ---

def save_query_log(user_id, query_text, selected_symptoms, photo_url, photo_analysis, results):
    db = load_db()
    log_entry = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "query_text": query_text,
        "selected_symptoms": selected_symptoms, # List of symptom IDs/Names
        "photo_url": photo_url,
        "photo_analysis": photo_analysis,       # dict (label, confidence)
        "results": results,                     # dict (allergens, advice)
        "created_at": datetime.utcnow().isoformat()
    }
    db["query_logs"].append(log_entry)
    save_db(db)
    return log_entry

def get_query_logs(user_id):
    db = load_db()
    logs = [log for log in db["query_logs"] if log["user_id"] == user_id]
    # Sort by created_at descending
    logs.sort(key=lambda x: x["created_at"], reverse=True)
    return logs
