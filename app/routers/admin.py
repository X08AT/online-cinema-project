from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db, require_admin
from app.models.user import User, UserGroup
from app.schemas.admin import AdminChangeGroupModel

router = APIRouter()


@router.patch("/admin/users/{user_id}/group", status_code=200)
async def admin_update_group(
        user_id: int,
        data: AdminChangeGroupModel,
        db: AsyncSession = Depends(get_db),
        _admin: User = Depends(require_admin)
):
    result = await db.execute(select(User).where(User.id == user_id))

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    result = await db.execute(select(UserGroup)
                              .where(UserGroup.name == data.user_group))

    new_group = result.scalar_one_or_none()

    if new_group is None:
        raise HTTPException(status_code=404, detail="Group not found")

    user.group_id = new_group.id

    await db.commit()

    return {"message": "User group changed successfully"}
