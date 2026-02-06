from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token
from app.schemas.auth import LoginRequest, TokenResponse

from app.core.deps import get_db
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.models import User, Role
from app.schemas.user import UserCreate, UserResponse, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Get default role
    default_role = db.query(Role).filter(Role.name == "viewer").first()
    if not default_role:
        raise HTTPException(
            status_code=500,
            detail="Default role not found"
        )

    # Create user
    user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        roles=[default_role],
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return UserResponse(
        id=user.id,
        email=user.email,
        roles=[role.name for role in user.roles],
    )


@router.post("/login")
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()

    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
@router.post("/login", response_model=TokenResponse)
def login_user(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token({
        "sub": str(user.id),
        "roles": [role.name for role in user.roles]
    })

    return {"access_token": token}
