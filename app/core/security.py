import secrets
import hashlib
from app.core.config import KEY_PREFIX


def generate_api_key() -> str:
    """Generate a cryptographically secure API key."""
    return KEY_PREFIX + secrets.token_urlsafe(32)


def hash_api_key(raw_key: str) -> str:
    """Hash an API key using SHA-256 before storing."""
    return hashlib.sha256(raw_key.encode()).hexdigest()


def verify_api_key(raw_key: str, stored_hash: str) -> bool:
    """Check if a raw key matches a stored hash."""
    return hash_api_key(raw_key) == stored_hash
