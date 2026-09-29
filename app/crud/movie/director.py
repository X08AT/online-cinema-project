from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.movie import Director
from app.schemas.movie.movie import (
    NamedEntityCreateModel,
    NamedEntityUpdateModel
)


async def create_director(
    data: NamedEntityCreateModel,
    db: AsyncSession
) -> Director:
    director = Director(**data.model_dump())

    db.add(director)
    await db.commit()
    await db.refresh(director)

    return director


async def get_directors(db: AsyncSession) -> list[Director]:
    result = await db.execute(select(Director))

    directors = result.scalars().all()

    return directors


async def get_director_by_id(
    director_id: int,
    db: AsyncSession
) -> Director | None:
    result = await db.execute(
        select(Director).where(Director.id == director_id)
    )

    director = result.scalar_one_or_none()

    return director


async def update_director(
    data: NamedEntityUpdateModel,
    director_id: int,
    db: AsyncSession
) -> Director | None:
    director = await get_director_by_id(director_id, db)

    if director is None:
        return None

    director.name = data.name

    await db.commit()
    await db.refresh(director)

    return director


async def delete_director(
    director_id: int,
    db: AsyncSession
) -> bool:
    director = await get_director_by_id(director_id, db)

    if director is None:
        return False

    await db.delete(director)
    await db.commit()

    return True
