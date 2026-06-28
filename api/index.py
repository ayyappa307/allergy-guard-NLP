import os
import sys
import traceback
from fastapi import FastAPI

app = FastAPI()

try:
    # Ensure root folder is in sys.path
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)

    # Ensure backend folder is in sys.path so inner imports work
    backend_dir = os.path.join(root_dir, "backend")
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)

    from backend.main import app as real_app
    app = real_app
except Exception as e:
    tb = traceback.format_exc()
    
    @app.get("/{path:path}")
    def catch_all(path: str):
        return {
            "error": "Import failed during serverless function startup",
            "message": str(e),
            "traceback": tb.split("\n")
        }

# Diagnostic Debug Endpoint
@app.get("/api/debug")
def get_debug_info():
    try:
        import db
        
        info = {
            "db_driver": db.DB_DRIVER,
            "postgres_url_exists": bool(db.POSTGRES_URL),
            "db_file_exists": os.path.exists(db.DB_FILE),
            "db_file_path": db.DB_FILE,
            "tables": {}
        }
        
        if db.DB_DRIVER != "local":
            conn = None
            try:
                conn = db.get_connection()
                cur = conn.cursor()
                for tbl in ["users", "allergens", "symptoms", "foods", "medicines", "query_logs"]:
                    try:
                        cur.execute(f"SELECT COUNT(*) FROM {tbl};")
                        cnt = db.fetch_one_dict(cur)["count"]
                        info["tables"][tbl] = f"{cnt} rows"
                    except Exception as e:
                        info["tables"][tbl] = f"Error: {e}"
                cur.close()
            except Exception as e:
                info["db_connection_error"] = str(e)
            finally:
                if conn:
                    conn.close()
        else:
            # Local mode info
            try:
                data = db.load_db()
                for key, val in data.items():
                    info["tables"][f"local_{key}"] = f"{len(val)} items"
            except Exception as e:
                info["local_db_error"] = str(e)
                
        return info
    except Exception as e:
        return {
            "error": "Debug endpoint crashed",
            "message": str(e),
            "traceback": traceback.format_exc().split("\n")
        }
