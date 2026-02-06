from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Role

DEFAULT_ROLES = ["admin", "analyst", "viewer"]

def seed_roles():
    db: Session = SessionLocal()

    try:
        for role_name in DEFAULT_ROLES:
            exists = db.query(Role).filter(Role.name == role_name).first()
            if not exists:
                db.add(Role(name=role_name))
        db.commit()
    finally:
        db.close()
