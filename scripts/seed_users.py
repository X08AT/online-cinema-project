import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.core.settings import settings
from app.db.session import SessionLocal
from app.models import movie  # noqa: F401
from app.models.user import User, UserGroup, UserGroupEnum


async def create_user_if_not_exists(
    db: AsyncSession,
    email: str,
    password: str,
    group_name: UserGroupEnum,
) -> None:
    user_result = await db.execute(select(User).where(User.email == email))
    existing_user = user_result.scalar_one_or_none()

    if existing_user is not None:
        print(f"User {email} already exists")
        return

    group_result = await db.execute(
        select(UserGroup).where(UserGroup.name == group_name.value)
    )
    group = group_result.scalar_one_or_none()

    if group is None:
        raise RuntimeError(
            f"Group {group_name.value} does not exist. " "Run Alembic migrations first."
        )

    user = User(
        email=email,
        hashed_password=hash_password(password),
        is_active=True,
        group_id=group.id,
    )

    db.add(user)

    print(f"Created {group_name.value}: {email}")


async def seed_users() -> None:
    async with SessionLocal() as db:
        await create_user_if_not_exists(
            db,
            settings.DEFAULT_USER_EMAIL,
            settings.DEFAULT_USER_PASSWORD,
            UserGroupEnum.USER,
        )

        await create_user_if_not_exists(
            db,
            settings.DEFAULT_MODERATOR_EMAIL,
            settings.DEFAULT_MODERATOR_PASSWORD,
            UserGroupEnum.MODERATOR,
        )

        await create_user_if_not_exists(
            db,
            settings.DEFAULT_ADMIN_EMAIL,
            settings.DEFAULT_ADMIN_PASSWORD,
            UserGroupEnum.ADMIN,
        )

        await db.commit()


if __name__ == "__main__":
    asyncio.run(seed_users())
