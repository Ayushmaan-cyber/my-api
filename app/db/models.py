from app.db.database import get_connection


def create_tables():
    """Create all required database tables."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS api_keys (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            key_hash    TEXT    UNIQUE NOT NULL,
            is_active   INTEGER DEFAULT 1,
            usage_count INTEGER DEFAULT 0,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
