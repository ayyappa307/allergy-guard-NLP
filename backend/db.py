import os
import json
import uuid
from datetime import datetime
from urllib.parse import urlparse

# Local DB File Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "local_db.json")

# Database URL from environment variables (Supabase)
POSTGRES_URL = os.environ.get("POSTGRES_URL") or os.environ.get("DATABASE_URL")
USE_POSTGRES = bool(POSTGRES_URL)

# Check which database drivers are available
DB_DRIVER = "local"
if USE_POSTGRES:
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        DB_DRIVER = "psycopg2"
    except Exception:
        try:
            import pg8000.dbapi
            DB_DRIVER = "pg8000"
        except Exception:
            DB_DRIVER = "local"

def get_connection():
    if DB_DRIVER == "local":
        return None
    url = POSTGRES_URL
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
        
    if DB_DRIVER == "psycopg2":
        if "sslmode" not in url:
            if "?" in url:
                url += "&sslmode=require"
            else:
                url += "?sslmode=require"
        return psycopg2.connect(url, cursor_factory=RealDictCursor)
        
    elif DB_DRIVER == "pg8000":
        # Parse credentials from URL for pg8000
        parsed = urlparse(url)
        username = parsed.username
        password = parsed.password
        database = parsed.path.lstrip('/')
        hostname = parsed.hostname
        port = parsed.port or 5432
        
        # Configure SSL context for Supabase
        import ssl
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        return pg8000.dbapi.connect(
            user=username,
            password=password,
            host=hostname,
            database=database,
            port=port,
            ssl_context=ssl_context
        )
    return None

# --- DUAL-DRIVER CURSOR COMPATIBILITY HELPERS ---

def fetch_all_dict(cursor):
    if DB_DRIVER == "psycopg2":
        return list(cursor.fetchall())
    else:
        desc = cursor.description
        if not desc:
            return []
        columns = [col[0].decode('utf-8') if isinstance(col[0], bytes) else col[0] for col in desc]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def fetch_one_dict(cursor):
    if DB_DRIVER == "psycopg2":
        return cursor.fetchone()
    else:
        desc = cursor.description
        if not desc:
            return None
        columns = [col[0].decode('utf-8') if isinstance(col[0], bytes) else col[0] for col in desc]
        row = cursor.fetchone()
        return dict(zip(columns, row)) if row else None

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
    try:
        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not write to local database file (likely read-only filesystem on Vercel): {e}")

# --- AUTO-DB SCHEMA CREATOR & MIGRATOR ---

def init_db():
    conn = None
    cur = None
    try:
        conn = get_connection()
    except Exception as e:
        print(f"Error connecting to Supabase during initialization: {e}")
        return

    if not conn:
        print("Database connection returned None. Skipping initialization.")
        return
        
    try:
        cur = conn.cursor()
        
        # Drop the medicines, users, and query_logs tables cascade to recreate them safely with the name field
        cur.execute("DROP TABLE IF EXISTS query_logs CASCADE;")
        cur.execute("DROP TABLE IF EXISTS users CASCADE;")
        cur.execute("DROP TABLE IF EXISTS medicines CASCADE;")
        conn.commit()
        
        # Create Tables
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR PRIMARY KEY,
                name VARCHAR,
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
                stage VARCHAR NOT NULL,
                category VARCHAR NOT NULL,
                image_path VARCHAR,
                description TEXT,
                warning TEXT,
                mapped_allergens JSONB
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS query_logs (
                id VARCHAR PRIMARY KEY,
                user_id VARCHAR REFERENCES users(id) ON DELETE CASCADE,
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
        cur.execute("SELECT COUNT(*) as count FROM allergens;")
        count_result = fetch_one_dict(cur)
        count = count_result["count"] if count_result else 0
        if count == 0:
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

            # Seed medicines (using correct keys matching local_db.json)
            for m in local_data.get("medicines", []):
                cur.execute(
                    "INSERT INTO medicines (id, stage, category, image_path, description, warning, mapped_allergens) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;",
                    (m["id"], m["stage"], m["category"], m["image_path"], m["description"], m["warning"], json.dumps(m["mapped_allergens"]))
                )
            
            # Seed users
            for u in local_data.get("users", []):
                cur.execute(
                    "INSERT INTO users (id, name, email, password_hash, created_at) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;",
                    (u["id"], u.get("name", "Default User"), u["email"], u["password_hash"], datetime.fromisoformat(u["created_at"]))
                )

            conn.commit()
            print("Supabase database successfully initialized and seeded.")
    except Exception as e:
        print(f"Error seeding Supabase database: {e}")
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
    finally:
        if cur:
            try:
                cur.close()
            except Exception:
                pass
        if conn:
            try:
                conn.close()
            except Exception:
                pass

# Auto-run table initialization if database connection environment is set
if DB_DRIVER != "local":
    init_db()

# --- USER AUTH ENTITIES ---

def create_user(name, email, password_hash):
    if DB_DRIVER == "local":
        db = load_db()
        for u in db["users"]:
            if u["email"].lower() == email.lower():
                return None
        user = {
            "id": str(uuid.uuid4()),
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "created_at": datetime.utcnow().isoformat()
        }
        db["users"].append(user)
        save_db(db)
        return user

    conn = get_connection()
    cur = None
    try:
        cur = conn.cursor()
        user_id = str(uuid.uuid4())
        created_at = datetime.utcnow()
        cur.execute(
            "INSERT INTO users (id, name, email, password_hash, created_at) VALUES (%s, %s, %s, %s, %s) RETURNING *;",
            (user_id, name, email, password_hash, created_at)
        )
        user = fetch_one_dict(cur)
        conn.commit()
        if user:
            if isinstance(user["created_at"], str):
                pass
            else:
                user["created_at"] = user["created_at"].isoformat()
        return user
    except Exception as e:
        print(f"Error creating user in PostgreSQL: {e}")
        conn.rollback()
        raise e
    finally:
        if cur:
            cur.close()
        conn.close()

def get_user_by_email(email):
    if DB_DRIVER == "local":
        db = load_db()
        for u in db["users"]:
            if u["email"].lower() == email.lower():
                return u
        return None

    conn = get_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(%s);", (email,))
        user = fetch_one_dict(cur)
        if user:
            if isinstance(user["created_at"], str):
                pass
            else:
                user["created_at"] = user["created_at"].isoformat()
        return user
    except Exception as e:
        print(f"Error fetching user by email from PostgreSQL: {e}")
        raise e
    finally:
        if cur:
            cur.close()
        conn.close()

def get_user_by_id(user_id):
    if DB_DRIVER == "local":
        db = load_db()
        for u in db["users"]:
            if u["id"] == user_id:
                return u
        return None

    conn = get_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
        user = fetch_one_dict(cur)
        if user:
            if isinstance(user["created_at"], str):
                pass
            else:
                user["created_at"] = user["created_at"].isoformat()
        return user
    except Exception as e:
        print(f"Error fetching user by ID from PostgreSQL: {e}")
        raise e
    finally:
        if cur:
            cur.close()
        conn.close()

# --- ALLERGENS ---

def get_allergens():
    if DB_DRIVER == "local":
        db = load_db()
        return db["allergens"]

    conn = get_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM allergens;")
        return fetch_all_dict(cur)
    except Exception as e:
        print(f"Error fetching allergens from PostgreSQL: {e}")
        raise e
    finally:
        if cur:
            cur.close()
        conn.close()

def get_allergen_by_id(allergen_id):
    if DB_DRIVER == "local":
        db = load_db()
        for a in db["allergens"]:
            if a["id"] == allergen_id:
                return a
        return None

    conn = get_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM allergens WHERE id = %s;", (allergen_id,))
        return fetch_one_dict(cur)
    except Exception as e:
        print(f"Error fetching allergen by ID from PostgreSQL: {e}")
        raise e
    finally:
        if cur:
            cur.close()
        conn.close()

# --- FOODS ---

def get_foods():
    if DB_DRIVER == "local":
        db = load_db()
        return db["foods"]

    conn = get_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM foods;")
        return fetch_all_dict(cur)
    except Exception as e:
        print(f"Error fetching foods from PostgreSQL: {e}")
        raise e
    finally:
        if cur:
            cur.close()
        conn.close()

def get_food_by_id(food_id):
    if DB_DRIVER == "local":
        db = load_db()
        for f in db["foods"]:
            if f["id"] == food_id:
                return f
        return None

    conn = get_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM foods WHERE id = %s;", (food_id,))
        return fetch_one_dict(cur)
    except Exception as e:
        print(f"Error fetching food by ID from PostgreSQL: {e}")
        raise e
    finally:
        if cur:
            cur.close()
        conn.close()

# --- SYMPTOMS ---

def get_symptoms():
    if DB_DRIVER == "local":
        db = load_db()
        return db["symptoms"]

    conn = get_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM symptoms;")
        return fetch_all_dict(cur)
    except Exception as e:
        print(f"Error fetching symptoms from PostgreSQL: {e}")
        raise e
    finally:
        if cur:
            cur.close()
        conn.close()

def get_symptom_by_id(symptom_id):
    if DB_DRIVER == "local":
        db = load_db()
        for s in db["symptoms"]:
            if s["id"] == symptom_id:
                return s
        return None

    conn = get_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM symptoms WHERE id = %s;", (symptom_id,))
        return fetch_one_dict(cur)
    except Exception as e:
        print(f"Error fetching symptom by ID from PostgreSQL: {e}")
        raise e
    finally:
        if cur:
            cur.close()
        conn.close()

# --- MEDICINES ---

def get_medicines():
    if DB_DRIVER == "local":
        db = load_db()
        return db["medicines"]

    conn = get_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM medicines;")
        return fetch_all_dict(cur)
    except Exception as e:
        print(f"Error fetching medicines from PostgreSQL: {e}")
        raise e
    finally:
        if cur:
            cur.close()
        conn.close()

# --- QUERY LOGS ---

def save_query_log(user_id, query_text, selected_symptoms, photo_url, photo_analysis, results):
    if DB_DRIVER == "local":
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

    conn = get_connection()
    cur = None
    try:
        cur = conn.cursor()
        # Ensure user record exists in PostgreSQL to satisfy the foreign key constraint
        email = "patient@allergyguard.org" if user_id == "mock-user-123" else f"{user_id}@allergyguard.org"
        name = "Mock Guest" if user_id == "mock-user-123" else "Registered Patient"
        cur.execute(
            "INSERT INTO users (id, name, email, password_hash, created_at) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;",
            (user_id, name, email, "mock-password-hash", datetime.utcnow())
        )
        
        log_id = str(uuid.uuid4())
        created_at = datetime.utcnow()
        cur.execute(
            """
            INSERT INTO query_logs (id, user_id, query_text, selected_symptoms, photo_url, photo_analysis, results, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
            """,
            (log_id, user_id, query_text, json.dumps(selected_symptoms), photo_url, json.dumps(photo_analysis), json.dumps(results), created_at)
        )
        log = fetch_one_dict(cur)
        conn.commit()
        if log:
            if isinstance(log["created_at"], str):
                pass
            else:
                log["created_at"] = log["created_at"].isoformat()
        return log
    except Exception as e:
        print(f"Error saving query log in PostgreSQL: {e}")
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        raise e
    finally:
        if cur:
            cur.close()
        if conn:
            try:
                conn.close()
            except Exception:
                pass

def get_query_logs(user_id):
    if DB_DRIVER == "local":
        db = load_db()
        logs = [log for log in db["query_logs"] if log["user_id"] == user_id]
        logs.sort(key=lambda x: x["created_at"], reverse=True)
        return logs

    conn = get_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM query_logs WHERE user_id = %s ORDER BY created_at DESC;", (user_id,))
        logs = fetch_all_dict(cur)
        for log in logs:
            if isinstance(log["created_at"], str):
                pass
            else:
                log["created_at"] = log["created_at"].isoformat()
        return list(logs)
    except Exception as e:
        print(f"Error fetching query logs from PostgreSQL: {e}")
        raise e
    finally:
        if cur:
            cur.close()
        conn.close()
