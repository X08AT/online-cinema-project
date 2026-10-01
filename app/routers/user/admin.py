from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db, require_admin
from app.models.user import User, UserGroup
from app.schemas.user.admin import AdminChangeGroupModel

router = APIRouter(tags=["Admin"])

DbSession = Annotated[AsyncSession, Depends(get_db)]
AdminUser = Annotated[User, Depends(require_admin)]


@router.patch(
    "/admin/users/{user_id}/group",
    status_code=200,
    summary="Change user group",
    description=(
        "Changes the group of a specified user. "
        "This operation is available only to administrators."
    ),
)
async def admin_update_group(
    user_id: int,
    data: AdminChangeGroupModel,
    db: DbSession,
    _admin: AdminUser,
):
    user_result = await db.execute(select(User).where(User.id == user_id))

    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    group_result = await db.execute(
        select(UserGroup).where(UserGroup.name == data.user_group)
    )

    new_group = group_result.scalar_one_or_none()

    if new_group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found",
        )

    user.group_id = new_group.id

    await db.commit()

    return {"message": "User group changed successfully"}


@router.patch(
    "/admin/users/{user_id}/activate",
    status_code=200,
    summary="Activate user account",
    description=(
        "Manually activates a specified user account. "
        "This operation is available only to administrators."
    ),
)
async def admin_activate_user(
    user_id: int,
    db: DbSession,
    _admin: AdminUser,
):
    result = await db.execute(select(User).where(User.id == user_id))

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if user.is_active:
        raise HTTPException(
            status_code=409,
            detail="User is already active",
        )

    user.is_active = True

    await db.commit()

    return {"message": "User activated successfully"}
