from fastapi import APIRouter, Depends

from app.core.auth import get_current_user, require_role
from app.models import User

router = APIRouter(prefix="/protected", tags=["protected"])


@router.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "roles": [role.name for role in current_user.roles],
    }


@router.get("/admin")
def admin_only(user: User = Depends(require_role("admin"))):
    return {
        "message": "Welcome, admin.",
        "user": user.email,
    }
