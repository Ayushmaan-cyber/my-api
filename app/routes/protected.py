from fastapi import APIRouter, Depends
from app.middleware.auth import verify_api_key

router = APIRouter()


@router.get("/data")
def get_data(user_id: int = Depends(verify_api_key)):
    """Example protected endpoint — requires valid API key."""
    return {
        "message": "Access granted!",
        "user_id": user_id,
        "data": {
            "items": ["item_1", "item_2", "item_3"],
            "total": 3
        }
    }


@router.get("/profile")
def get_profile(user_id: int = Depends(verify_api_key)):
    """Another protected endpoint example."""
    return {
        "user_id": user_id,
        "plan": "pro",
        "requests_today": 42
    }
