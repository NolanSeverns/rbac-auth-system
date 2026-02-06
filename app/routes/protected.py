from fastapi import APIRouter, Depends

from app.core.auth import get_current_user, require_role
from app.models import User

router = APIRouter(prefix="/protected", tags=["protected"])


@router.get("/user")
def user_only(current_user: User = Depends(get_current_user)):
    """
    Any authenticated user can access this route.
    """
    return {
        "message": "Authenticated user access granted.",
        "user_id": current_user.id,
        "email": current_user.email,
        "roles": [role.name for role in current_user.roles],
    }


@router.get("/admin")
def admin_only(current_user: User = Depends(require_role("admin"))):
    """
    Only users with the admin role can access this route.
    """
    return {
        "message": "Admin access granted.",
        "user_id": current_user.id,
        "email": current_user.email,
        "roles": [role.name for role in current_user.roles],
    }
