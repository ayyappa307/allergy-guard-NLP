import os
import json
import uuid
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

# Local DB File Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "local_db.json")

# Database URL from environment variables (Supabase)
POSTGRES_URL = os.environ.get("POSTGRES_URL") or os.environ.get("DATABASE_URL")

def get_connection():
    if not POSTGRES_URL:
        return None
    url = POSTGRES_URL
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    try:
        return psycopg2.connect(url, cursor_factory=RealDictCursor)
    except Exception as e:
        print(f"PostgreSQL connection error: {e}")
        return None

# --- LOCAL FILE DB FALLBACK ---

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

# --- AUTO-DB SCHEMA CREATOR & MIGRATOR ---

def init_db():
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            # Create Tables
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id VARCHAR PRIMARY KEY,
                    email VARCHAR UNIQUE NOT NULL,
                    password_hash VARCHAR NOT NULL,
                    created_at TIMESTAMP NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS allergens (
                    id VARCHAR PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    thumbnail_path VARCHAR,
                    description TEXT
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS symptoms (
                    id VARCHAR PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    severity VARCHAR NOT NULL,
                    image_path VARCHAR,
                    description TEXT
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS foods (
                    id VARCHAR PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    image_path VARCHAR,
                    description TEXT,
                    ingredients JSONB,
                    allergens JSONB,
                    alternatives JSONB
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS medicines (
                    id VARCHAR PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    brand VARCHAR,
                    type VARCHAR,
                    dosage VARCHAR,
                    severity_suitability VARCHAR,
                    active_ingredients VARCHAR,
                    image_path VARCHAR,
                    description TEXT
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS query_logs (
                    id VARCHAR PRIMARY KEY,
                    user_id VARCHAR REFERENCES users(id),
                    query_text TEXT,
                    selected_symptoms JSONB,
                    photo_url VARCHAR,
                    photo_analysis JSONB,
                    results JSONB,
                    created_at TIMESTAMP NOT NULL
                );
            """)
            conn.commit()

            # Seed tables if they are empty
            cur.execute("SELECT COUNT(*) FROM allergens;")
            if cur.fetchone()["count"] == 0:
                print("Supabase database empty. Auto-seeding tables from local JSON db...")
                local_data = load_db()
                
                # Seed allergens
                for a in local_data.get("allergens", []):
                    cur.execute(
                        "INSERT INTO allergens (id, name, thumbnail_path, description) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;",
                        (a["id"], a["name"], a["thumbnail_path"], a["description"])
                    )
                
                # Seed symptoms
                for s in local_data.get("symptoms", []):
                    cur.execute(
                        "INSERT INTO symptoms (id, name, severity, image_path, description) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;",
                        (s["id"], s["name"], s["severity"], s["image_path"], s["description"])
                    )

                # Seed foods
                for f in local_data.get("foods", []):
                    cur.execute(
                        "INSERT INTO foods (id, name, image_path, description, ingredients, allergens, alternatives) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;",
                        (f["id"], f["name"], f["image_path"], f["description"], json.dumps(f["ingredients"]), json.dumps(f["allergens"]), json.dumps(f["alternatives"]))
                    )

                # Seed medicines
                for m in local_data.get("medicines", []):
                    cur.execute(
                        "INSERT INTO medicines (id, name, brand, type, dosage, severity_suitability, active_ingredients, image_path, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;",
                        (m["id"], m["name"], m.get("brand"), m.get("type"), m.get("dosage"), m.get("severity_suitability"), m.get("active_ingredients"), m.get("image_path"), m.get("description", ""))
                    )
                
                # Seed users
                for u in local_data.get("users", []):
                    cur.execute(
                        "INSERT INTO users (id, email, password_hash, created_at) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;",
                        (u["id"], u["email"], u["password_hash"], datetime.fromisoformat(u["created_at"]))
                    )

                conn.commit()
                print("Supabase database successfully initialized and seeded.")
    except Exception as e:
        print(f"Error seeding Supabase database: {e}")
        conn.rollback()
    finally:
        conn.close()

# Auto-run table initialization if database connection environment is set
if POSTGRES_URL:
    init_db()

# --- USER AUTH ENTITIES ---

def create_user(email, password_hash):
    conn = get_connection()
    if not conn:
        db = load_db()
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

    try:
        with conn.cursor() as cur:
            user_id = str(uuid.uuid4())
            created_at = datetime.utcnow()
            cur.execute(
                "INSERT INTO users (id, email, password_hash, created_at) VALUES (%s, %s, %s, %s) RETURNING *;",
                (user_id, email, password_hash, created_at)
            )
            user = cur.fetchone()
            conn.commit()
            if user:
                user["created_at"] = user["created_at"].isoformat()
            return user
    except Exception as e:
        print(f"Error creating user in PostgreSQL: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def get_user_by_email(email):
    conn = get_connection()
    if not conn:
        db = load_db()
        for u in db["users"]:
            if u["email"].lower() == email.lower():
                return u
        return None

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(%s);", (email,))
            user = cur.fetchone()
            if user:
                user["created_at"] = user["created_at"].isoformat()
            return user
    except Exception as e:
        print(f"Error fetching user by email from PostgreSQL: {e}")
        return None
    finally:
        conn.close()

def get_user_by_id(user_id):
    conn = get_connection()
    if not conn:
        db = load_db()
        for u in db["users"]:
            if u["id"] == user_id:
                return u
        return None

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
            user = cur.fetchone()
            if user:
                user["created_at"] = user["created_at"].isoformat()
            return user
    except Exception as e:
        print(f"Error fetching user by ID from PostgreSQL: {e}")
        return None
    finally:
        conn.close()

# --- ALLERGENS ---

def get_allergens():
    conn = get_connection()
    if not conn:
        db = load_db()
        return db["allergens"]

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM allergens;")
            return list(cur.fetchall())
    except Exception as e:
        print(f"Error fetching allergens from PostgreSQL: {e}")
        return []
    finally:
        conn.close()

def get_allergen_by_id(allergen_id):
    conn = get_connection()
    if not conn:
        db = load_db()
        for a in db["allergens"]:
            if a["id"] == allergen_id:
                return a
        return None

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM allergens WHERE id = %s;", (allergen_id,))
            return cur.fetchone()
    except Exception as e:
        print(f"Error fetching allergen by ID from PostgreSQL: {e}")
        return None
    finally:
        conn.close()

# --- FOODS ---

def get_foods():
    conn = get_connection()
    if not conn:
        db = load_db()
        return db["foods"]

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM foods;")
            return list(cur.fetchall())
    except Exception as e:
        print(f"Error fetching foods from PostgreSQL: {e}")
        return []
    finally:
        conn.close()

def get_food_by_id(food_id):
    conn = get_connection()
    if not conn:
        db = load_db()
        for f in db["foods"]:
            if f["id"] == food_id:
                return f
        return None

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM foods WHERE id = %s;", (food_id,))
            return cur.fetchone()
    except Exception as e:
        print(f"Error fetching food by ID from PostgreSQL: {e}")
        return None
    finally:
        conn.close()

# --- SYMPTOMS ---

def get_symptoms():
    conn = get_connection()
    if not conn:
        db = load_db()
        return db["symptoms"]

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM symptoms;")
            return list(cur.fetchall())
    except Exception as e:
        print(f"Error fetching symptoms from PostgreSQL: {e}")
        return []
    finally:
        conn.close()

def get_symptom_by_id(symptom_id):
    conn = get_connection()
    if not conn:
        db = load_db()
        for s in db["symptoms"]:
            if s["id"] == symptom_id:
                return s
        return None

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM symptoms WHERE id = %s;", (symptom_id,))
            return cur.fetchone()
    except Exception as e:
        print(f"Error fetching symptom by ID from PostgreSQL: {e}")
        return None
    finally:
        conn.close()

# --- MEDICINES ---

def get_medicines():
    conn = get_connection()
    if not conn:
        db = load_db()
        return db["medicines"]

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM medicines;")
            return list(cur.fetchall())
    except Exception as e:
        print(f"Error fetching medicines from PostgreSQL: {e}")
        return []
    finally:
        conn.close()

# --- QUERY LOGS ---

def save_query_log(user_id, query_text, selected_symptoms, photo_url, photo_analysis, results):
    conn = get_connection()
    if not conn:
        db = load_db()
        log_entry = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "query_text": query_text,
            "selected_symptoms": selected_symptoms,
            "photo_url": photo_url,
            "photo_analysis": photo_analysis,
            "results": results,
            "created_at": datetime.utcnow().isoformat()
        }
        db["query_logs"].append(log_entry)
        save_db(db)
        return log_entry

    try:
        with conn.cursor() as cur:
            log_id = str(uuid.uuid4())
            created_at = datetime.utcnow()
            cur.execute(
                """
                INSERT INTO query_logs (id, user_id, query_text, selected_symptoms, photo_url, photo_analysis, results, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
                """,
                (log_id, user_id, query_text, json.dumps(selected_symptoms), photo_url, json.dumps(photo_analysis), json.dumps(results), created_at)
            )
            log = cur.fetchone()
            conn.commit()
            if log:
                log["created_at"] = log["created_at"].isoformat()
            return log
    except Exception as e:
        print(f"Error saving query log in PostgreSQL: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def get_query_logs(user_id):
    conn = get_connection()
    if not conn:
        db = load_db()
        logs = [log for log in db["query_logs"] if log["user_id"] == user_id]
        logs.sort(key=lambda x: x["created_at"], reverse=True)
        return logs

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM query_logs WHERE user_id = %s ORDER BY created_at DESC;", (user_id,))
            logs = cur.fetchall()
            for log in logs:
                log["created_at"] = log["created_at"].isoformat()
            return list(logs)
    except Exception as e:
        print(f"Error fetching query logs from PostgreSQL: {e}")
        return []
    finally:
        conn.close()
