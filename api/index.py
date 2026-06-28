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
