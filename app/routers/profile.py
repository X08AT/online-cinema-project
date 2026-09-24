from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.profile import (
    get_profile_by_user_id,
    create_profile,
    update_profile
)
from app.db.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.profile import (
    ProfileCreateModel,
    ProfileResponseModel,
    ProfileUpdateModel
)
from app.services.minio_service import upload_avatar

router = APIRouter()


@router.post(
    "/profile",
    status_code=201,
    response_model=ProfileResponseModel
)
async def profile_create(
        data: ProfileCreateModel = Depends(ProfileCreateModel.as_form),
        avatar: UploadFile = File(...),
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    profile = await get_profile_by_user_id(current_user.id, db)

    if profile:
        raise HTTPException(status_code=409, detail="Profile already created")

    avatar_path = upload_avatar(avatar)

    new_profile = await create_profile(current_user.id, db, data, avatar_path)

    return new_profile


@router.get(
    "/profile",
    status_code=200,
    response_model=ProfileResponseModel
)
async def get_profile(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    profile = await get_profile_by_user_id(current_user.id, db)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@router.patch("/profile", response_model=ProfileResponseModel)
async def profile_update(
        data: ProfileUpdateModel = Depends(ProfileUpdateModel.as_form),
        avatar: UploadFile | None = File(None),
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    profile = await get_profile_by_user_id(current_user.id, db)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    avatar_path = None

    if avatar is not None:
        avatar_path = upload_avatar(avatar)

    updated_profile = await update_profile(
        current_user.id,
        db,
        data,
        avatar_path
    )

    return updated_profile
