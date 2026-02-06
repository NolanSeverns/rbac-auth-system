from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.auth import require_role
from app.models import User, Role
from app.models.audit_log import AuditLog

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/promote/{user_id}")
def promote_to_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    # Find target user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Find admin role
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    if not admin_role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Admin role not found",
        )

    # Prevent duplicate promotion
    if admin_role in user.roles:
        return {
            "message": "User is already an admin",
            "user_id": user.id,
            "roles": [role.name for role in user.roles],
        }

    # Promote user
    user.roles.append(admin_role)

    # Audit log
    log = AuditLog(
        user_id=current_user.id,
        action="PROMOTE_USER",
        target=f"user_id={user.id}",
    )

    db.add(log)
    db.commit()
    db.refresh(user)

    return {
        "message": "User promoted to admin",
        "user_id": user.id,
        "roles": [role.name for role in user.roles],
    }
