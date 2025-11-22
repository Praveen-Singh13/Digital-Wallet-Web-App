import sqlite3
from flask import g
from pathlib import Path
from app.config.config import DATABASE_FILE, DATABASE_DIR

SCHEMA_PATH = Path(__file__).resolve().parent.parent.parent / "database" / "schema.sql"

def get_db_connection():
    if "db" not in g:
        DATABASE_DIR.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(DATABASE_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db

def init_db_if_needed():
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    if not Path(DATABASE_FILE).exists():
        conn = sqlite3.connect(DATABASE_FILE)
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.close()
