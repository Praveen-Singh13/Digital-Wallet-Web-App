import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_FILE = DATABASE_DIR / "wallet.db"

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secure-wallet-key-2025")

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = "Lax"

    TEMPLATES_AUTO_RELOAD = True

    DB_PATH = str(DATABASE_FILE)

    DEBUG = True
    ENV = "development"
