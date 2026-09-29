from fastapi import APIRouter

from app.routers.user import admin, auth, profile

router = APIRouter()

router.include_router(admin.router)
router.include_router(auth.router)
router.include_router(profile.router)
