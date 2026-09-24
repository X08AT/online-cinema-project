from typing import AsyncGenerator

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.db.session import SessionLocal
from app.models.user import User, UserGroup, UserGroupEnum

security = HTTPBearer()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_current_user(
    credentials=Depends(security), db: AsyncSession = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid access token")

    result = await db.execute(select(User).where(User.id == int(user_id)))

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    return user


async def require_admin(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(UserGroup)
                              .where(UserGroup.id == current_user.group_id))

    group = result.scalar_one_or_none()

    if group is None or group.name != UserGroupEnum.ADMIN.value:
        raise HTTPException(
            status_code=403,
            detail="You are not an admin"
        )

    return current_user


async def require_moderator(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(UserGroup)
                              .where(UserGroup.id == current_user.group_id))

    group = result.scalar_one_or_none()

    if group is None or (
            group.name != UserGroupEnum.ADMIN.value
            and group.name != UserGroupEnum.MODERATOR.value
    ):
        raise HTTPException(
            status_code=403,
            detail="You are not a moderator"
        )

    return current_user
