import sqlite3
import os
from app.core.config import DATABASE_URL


def get_db_path() -> str:
    return DATABASE_URL.replace("sqlite:///", "")


def get_connection() -> sqlite3.Connection:
    path = get_db_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row   # dict-like rows
    return conn
