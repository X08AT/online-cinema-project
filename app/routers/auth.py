import secrets
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password, create_access_token
from app.db.dependencies import get_db
from app.models.user import User, UserGroup, UserGroupEnum, ActivationToken, RefreshToken
from app.schemas.auth import RegistrationModel, ActivationTokenModel, ResendActivationTokenModel, LoginModel

router = APIRouter()

@router.post("/auth/register", status_code=201)
async def register(data: RegistrationModel, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))

    user = result.scalar_one_or_none()

    if user is not None:
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
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
    )

    db.add(activation_token)
    await db.commit()

    return {
        "message": "User registered successfully",
        "user_id": user.id,
        "activation_token": activation_token.token,
    }


@router.post("/auth/activate", status_code=200)
async def activate(data: ActivationTokenModel, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ActivationToken).where(ActivationToken.token == data.token))

    token = result.scalar_one_or_none()

    if token is None:
        raise HTTPException(status_code=404, detail="Token does not exist")

    if token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=404, detail="Token expired")

    result = await db.execute(select(User).where(User.id == token.user_id))

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")

    user.is_active = True

    await db.delete(token)
    await db.commit()

    return {"message": "Account activated"}


@router.post("/auth/resend-activation", status_code=200)
async def resend_activation(data: ResendActivationTokenModel, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")

    if user.is_active:
        raise HTTPException(status_code=400, detail="User already active")

    if user.activation_token:
        await db.delete(user.activation_token)
        await db.flush()

    new_activation_token = ActivationToken(
        token=secrets.token_urlsafe(32),
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
    )

    db.add(new_activation_token)
    await db.commit()

    return {"message": f"new token: {new_activation_token.token}"}


@router.post("/auth/login", status_code=200)
async def login(data: LoginModel, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="User is not active")

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    access_token = create_access_token(data={"sub": user.id})
    refresh_token = RefreshToken(
        token=secrets.token_urlsafe(32),
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
    )

    db.add(refresh_token)
    await db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token.token}
