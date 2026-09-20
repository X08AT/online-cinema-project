import secrets
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)
from app.db.dependencies import get_db, get_current_user
from app.models.user import (
    User,
    UserGroup,
    UserGroupEnum,
    ActivationToken,
    RefreshToken,
    PasswordResetToken,
)
from app.schemas.auth import (
    RegistrationModel,
    ActivationTokenModel,
    ResendActivationTokenModel,
    LoginModel,
    TokenRefreshModel,
    LogoutModel,
    ChangePasswordModel,
    ResetPasswordRequestModel,
    ResetPasswordModel,
)

router = APIRouter()


@router.post("/auth/register", status_code=201)
async def register(
        data: RegistrationModel,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == data.email))

    user = result.scalar_one_or_none()

    if user is not None:
        raise HTTPException(status_code=400, detail="Email already registered")

    result = await db.execute(
        select(UserGroup).where(UserGroup.name == UserGroupEnum.USER.value)
    )

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
async def activate(
        data: ActivationTokenModel,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ActivationToken).where(ActivationToken.token == data.token)
    )

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
async def resend_activation(
    data: ResendActivationTokenModel, db: AsyncSession = Depends(get_db)
):
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


@router.post("/auth/refresh", status_code=200)
async def refresh_token(
        data: TokenRefreshModel,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(RefreshToken).where(RefreshToken.token == data.refresh_token)
    )

    refresh_token = result.scalar_one_or_none()

    if refresh_token is None:
        raise HTTPException(
            status_code=404,
            detail="Refresh token does not exist"
        )

    if refresh_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Refresh token expired")

    new_access_token = create_access_token(data={"sub": refresh_token.user_id})

    return {"access_token": new_access_token}


@router.post("/auth/logout", status_code=200)
async def logout(data: LogoutModel, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(RefreshToken).where(RefreshToken.token == data.refresh_token)
    )

    refresh_token = result.scalar_one_or_none()

    if refresh_token is None:
        raise HTTPException(
            status_code=404,
            detail="Refresh token does not exist"
        )

    await db.delete(refresh_token)
    await db.commit()

    return {"message": "You have been logged out"}


@router.post("/auth/change-password", status_code=200)
async def change_password(
    data: ChangePasswordModel,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    new_password = hash_password(data.password)

    current_user.hashed_password = new_password

    await db.commit()

    return {"message": "Password changed"}


@router.post("/auth/password-reset/request", status_code=200)
async def password_reset_request(
    data: ResetPasswordRequestModel, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == data.email))

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="User is not active")

    if user.password_reset_token:
        await db.delete(user.password_reset_token)
        await db.flush()

    new_password_reset_token = PasswordResetToken(
        token=secrets.token_urlsafe(32),
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
    )

    db.add(new_password_reset_token)
    await db.commit()
    return {
        "message": f"Password reset token: {new_password_reset_token.token}"
    }


@router.post("/auth/password-reset/confirm", status_code=200)
async def password_reset(
        data: ResetPasswordModel,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(PasswordResetToken)
        .where(PasswordResetToken.token == data.token)
    )

    token = result.scalar_one_or_none()

    if token is None:
        raise HTTPException(
            status_code=404, detail="Password reset token does not exist"
        )

    if token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="Password reset token expired"
        )

    result = await db.execute(select(User).where(User.id == token.user_id))

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="User is not active")

    new_hashed_password = hash_password(data.new_password)

    user.hashed_password = new_hashed_password
    await db.delete(token)
    await db.commit()

    return {"message": "Password reset successfully"}
