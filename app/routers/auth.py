import secrets
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.db.dependencies import get_db
from app.models.user import User, UserGroup, UserGroupEnum, ActivationToken
from app.schemas.auth import RegistrationModel

router = APIRouter()

@router.post("/auth/register", status_code=201)
async def register(data: RegistrationModel, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))

    user = result.scalar_one_or_none()

    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    result = await db.execute(select(UserGroup).where(UserGroup.name == UserGroupEnum.USER.value))

    group = result.scalar_one_or_none()

    if group is None:
        raise HTTPException(status_code=500, detail="Internal server error")

    hashed_password = hash_password(data.password)

    user = User(
        email=data.email,
        hashed_password=hashed_password,
        is_active=False,
        group_id=group.id,
    )

    db.add(user)
    await db.flush()

    activation_token = ActivationToken(
        token=secrets.token_urlsafe(32),
        user_id=user.id,
        expires_at = datetime.now(timezone.utc) + timedelta(hours=24),
    )

    db.add(activation_token)
    await db.commit()

    return {
        "message": "User registered successfully",
        "user_id": user.id,
        "activation_token": activation_token.token,
    }
