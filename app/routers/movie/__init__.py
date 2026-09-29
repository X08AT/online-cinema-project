from fastapi import APIRouter

from app.routers.movie import (
    favorites,
    management,
    comments,
    reactions,
    ratings,
    notifications,
    catalog,
)

router = APIRouter()

router.include_router(favorites.router)
router.include_router(management.router)
router.include_router(comments.router)
router.include_router(reactions.router)
router.include_router(ratings.router)
router.include_router(notifications.router)
router.include_router(catalog.router)
