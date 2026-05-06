from fastapi import Header, HTTPException
from app.db.database import get_connection
from app.core.security import hash_api_key


def verify_api_key(x_api_key: str = Header(...)):
    """
    Dependency: validates X-Api-Key header.
    Returns the key row id on success.
    Raises 401 if invalid or revoked.
    """
    key_hash = hash_api_key(x_api_key)
    conn = get_connection()
    row = conn.execute(
        "SELECT id FROM api_keys WHERE key_hash = ? AND is_active = 1",
        (key_hash,)
    ).fetchone()

    if not row:
        raise HTTPException(status_code=401, detail="Invalid or revoked API key")

    # Track usage
    conn.execute(
        "UPDATE api_keys SET usage_count = usage_count + 1 WHERE id = ?",
        (row["id"],)
    )
    conn.commit()
    conn.close()
    return row["id"]
