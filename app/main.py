from fastapi import FastAPI

from app.database import Base, engine
from app.models import User, Role
from app.routes.auth import router as auth_router
from app.routes.protected import router as protected_router

app = FastAPI(title="RBAC Auth System")

# Create tables
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(auth_router)
app.include_router(protected_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
from app.routes.admin import router as admin_router

app.include_router(admin_router)
