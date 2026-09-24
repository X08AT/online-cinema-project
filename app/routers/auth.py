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
    ResendActivationTokenModel,
    LoginModel,
    TokenRefreshModel,
    LogoutModel,
    ChangePasswordModel,
    ResetPasswordRequestModel,
    ResetPasswordModel,
)
from app.services.email_service import send_email

router = APIRouter()


@router.post("/auth/register", status_code=201)
async def register(
        data: RegistrationModel,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == data.email))

    user = result.scalar_one_or_none()

    if user is not None:
        raise HTTPException(status_code=409, detail="Email already registered")

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

    activation_link = (
        f"http://localhost:8000/auth/activate"
        f"?token={activation_token.token}"
    )

    email_body = (
        "Hello!\n\n"
        "Your account has been successfully registered.\n\n"
        "Please activate your account using the link below:\n"
        f"{activation_link}\n\n"
        "This link is valid for 24 hours."
    )

    send_email(
        user.email,
        "Activate your Online Cinema account",
        email_body
    )

    return {
        "message": "Registration successful."
                   " Check your email to activate your account."
    }


@router.get("/auth/activate", status_code=200)
async def activate(
        token: str,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ActivationToken).where(ActivationToken.token == token)
    )

    token_obj = result.scalar_one_or_none()

    if token_obj is None:
        raise HTTPException(status_code=404, detail="Token does not exist")

    if token_obj.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="Activation token has expired"
        )

    result = await db.execute(select(User).where(User.id == token_obj.user_id))

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")

    user.is_active = True

    await db.delete(token_obj)
    await db.commit()

    return {"message": "Account activated"}


@router.post("/auth/resend-activation", status_code=200)
async def resend_activation(
    data: ResendActivationTokenModel,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == data.email)
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User does not exist"
        )

    if user.is_active:
        raise HTTPException(
            status_code=409,
            detail="User is already active"
        )

    result = await db.execute(
        select(ActivationToken).where(
            ActivationToken.user_id == user.id
        )
    )

    old_activation_token = result.scalar_one_or_none()

    if old_activation_token:
        await db.delete(old_activation_token)
        await db.flush()

    new_activation_token = ActivationToken(
        token=secrets.token_urlsafe(32),
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
    )

    db.add(new_activation_token)
    await db.commit()

    activation_link = (
        f"http://localhost:8000/auth/activate"
        f"?token={new_activation_token.token}"
    )

    email_body = (
        "Hello!\n\n"
        "Here is your new activation link:\n"
        f"{activation_link}\n\n"
        "This link is valid for 24 hours."
    )

    send_email(
        user.email,
        "New activation link",
        email_body
    )

    return {"message": "Activation email sent"}


@router.post("/auth/login", status_code=200)
async def login(data: LoginModel, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is not active")

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

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
            status_code=401,
            detail="Invalid refresh token"
        )

    if refresh_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=401,
            detail="Refresh token has expired"
        )

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
        raise HTTPException(status_code=400, detail="Incorrect old password")

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
        raise HTTPException(status_code=403, detail="User is not active")

    result = await db.execute(
        select(PasswordResetToken).where(
            PasswordResetToken.user_id == user.id
        )
    )
    old_password_reset_token = result.scalar_one_or_none()

    if old_password_reset_token:
        await db.delete(old_password_reset_token)
        await db.flush()

    new_password_reset_token = PasswordResetToken(
        token=secrets.token_urlsafe(32),
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
    )

    db.add(new_password_reset_token)
    await db.commit()

    password_reset_link = (
        f"http://localhost:8000/auth/password-reset/confirm"
        f"?token={new_password_reset_token.token}"
    )

    email_body = (
        "Hello!\n\n"
        "Here is your password reset link:\n"
        f"{password_reset_link}\n\n"
        "This link is valid for 24 hours."
    )

    send_email(
        user.email,
        "Reset Your Password",
        email_body
    )

    return {
        "message": "Password reset link sent to your email"
    }


@router.post("/auth/password-reset/confirm", status_code=200)
async def password_reset(
        token: str,
        data: ResetPasswordModel,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(PasswordResetToken)
        .where(PasswordResetToken.token == token)
    )

    token_obj = result.scalar_one_or_none()

    if token_obj is None:
        raise HTTPException(
            status_code=404, detail="Password reset token does not exist"
        )

    if token_obj.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="Password reset token expired"
        )

    result = await db.execute(select(User).where(User.id == token_obj.user_id))

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is not active")

    new_hashed_password = hash_password(data.new_password)

    user.hashed_password = new_hashed_password
    await db.delete(token_obj)
    await db.commit()

    return {"message": "Password reset successfully"}
