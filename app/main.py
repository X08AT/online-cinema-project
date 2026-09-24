from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.admin import router as admin_router
from app.routers.profile import router as profile_router

app = FastAPI(title="Online Cinema", version="1.0")

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(profile_router)
