from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.movie import Star
from app.schemas.movie.movie import (
    NamedEntityCreateModel,
    NamedEntityUpdateModel
)


async def create_star(data: NamedEntityCreateModel, db: AsyncSession) -> Star:
    star = Star(**data.model_dump())

    db.add(star)
    await db.commit()
    await db.refresh(star)

    return star


async def get_stars(db: AsyncSession) -> list[Star]:
    result = await db.execute(select(Star))

    stars = result.scalars().all()

    return stars


async def get_star_by_id(star_id: int, db: AsyncSession) -> Star | None:
    result = await db.execute(select(Star).where(Star.id == star_id))

    star = result.scalar_one_or_none()

    return star


async def update_star(
        data: NamedEntityUpdateModel,
        star_id: int,
        db: AsyncSession
) -> Star | None:
    star = await get_star_by_id(star_id, db)

    if star is None:
        return None

    star.name = data.name

    await db.commit()
    await db.refresh(star)

    return star


async def delete_star(star_id: int, db: AsyncSession) -> bool:
    star = await get_star_by_id(star_id, db)

    if star is None:
        return False

    await db.delete(star)
    await db.commit()

    return True
