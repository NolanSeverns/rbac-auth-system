from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

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
    try:
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

        # Create audit log entry
        log = AuditLog(
            user_id=current_user.id,
            action="PROMOTE_USER",
            target=f"user_id={user.id}",
        )

        db.add(log)

        # Commit everything atomically
        db.commit()
        db.refresh(user)

        return {
            "message": "User promoted to admin",
            "user_id": user.id,
            "roles": [role.name for role in user.roles],
        }

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to promote user",
        )


@router.get("/audit-logs")
def view_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    logs = (
        db.query(AuditLog)
        .order_by(AuditLog.timestamp.desc())
        .all()
    )

    return [
        {
            "id": log.id,
            "actor_user_id": log.user_id,
            "action": log.action,
            "target": log.target,
            "timestamp": log.timestamp,
        }
        for log in logs
    ]
