from fastapi import APIRouter, HTTPException, Header
from app.db.database import get_connection
from app.core.security import generate_api_key, hash_api_key
from app.core.config import ADMIN_TOKEN
from pydantic import BaseModel

router = APIRouter()


class CreateKeyRequest(BaseModel):
    name: str


def require_admin(x_admin_token: str = Header(...)):
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Admin access required")


# ── Create a new API key ──────────────────────────────────────────
@router.post("/create")
def create_key(body: CreateKeyRequest, x_admin_token: str = Header(...)):
    require_admin(x_admin_token)

    raw_key  = generate_api_key()
    key_hash = hash_api_key(raw_key)

    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO api_keys (name, key_hash) VALUES (?, ?)",
            (body.name, key_hash)
        )
        conn.commit()
    except Exception:
        raise HTTPException(status_code=400, detail="Key creation failed")
    finally:
        conn.close()

    return {
        "api_key": raw_key,
        "name": body.name,
        "warning": "Save this key now — it will NOT be shown again!"
    }


# ── List all keys (hashes hidden) ────────────────────────────────
@router.get("/list")
def list_keys(x_admin_token: str = Header(...)):
    require_admin(x_admin_token)
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, name, is_active, usage_count, created_at FROM api_keys ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Revoke a key ──────────────────────────────────────────────────
@router.patch("/revoke/{key_id}")
def revoke_key(key_id: int, x_admin_token: str = Header(...)):
    require_admin(x_admin_token)
    conn = get_connection()
    conn.execute("UPDATE api_keys SET is_active = 0 WHERE id = ?", (key_id,))
    conn.commit()
    conn.close()
    return {"message": f"Key {key_id} revoked successfully"}


# ── Delete a key permanently ──────────────────────────────────────
@router.delete("/delete/{key_id}")
def delete_key(key_id: int, x_admin_token: str = Header(...)):
    require_admin(x_admin_token)
    conn = get_connection()
    conn.execute("DELETE FROM api_keys WHERE id = ?", (key_id,))
    conn.commit()
    conn.close()
    return {"message": f"Key {key_id} deleted permanently"}
