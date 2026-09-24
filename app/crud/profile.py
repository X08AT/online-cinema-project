from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserProfile
from app.schemas.profile import ProfileCreateModel


async def get_profile_by_user_id(user_id: int, db: AsyncSession):
    result = await db.execute(select(UserProfile)
                              .where(UserProfile.user_id == user_id))

    profile = result.scalar_one_or_none()

    return profile


async def create_profile(
        user_id: int,
        db: AsyncSession,
        data: ProfileCreateModel,
        avatar: str
):
    profile = UserProfile(
        user_id=user_id,
        **data.model_dump(),
        avatar=avatar,
    )

    db.add(profile)

    await db.commit()
    await db.refresh(profile)

    return profile
