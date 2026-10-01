from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.movie import Certification
from app.schemas.movie.movie import NamedEntityCreateModel, NamedEntityUpdateModel


async def create_certification(
    data: NamedEntityCreateModel,
    db: AsyncSession,
) -> Certification:
    certification = Certification(**data.model_dump())

    db.add(certification)
    await db.commit()
    await db.refresh(certification)

    return certification


async def get_certifications(
    db: AsyncSession,
) -> list[Certification]:
    result = await db.execute(select(Certification))

    certifications = result.scalars().all()

    return list(certifications)


async def get_certification_by_id(
    certification_id: int,
    db: AsyncSession,
) -> Certification | None:
    result = await db.execute(
        select(Certification).where(Certification.id == certification_id)
    )

    certification = result.scalar_one_or_none()

    return certification


async def update_certification(
    data: NamedEntityUpdateModel,
    certification_id: int,
    db: AsyncSession,
) -> Certification | None:
    certification = await get_certification_by_id(
        certification_id,
        db,
    )

    if certification is None:
        return None

    certification.name = data.name

    await db.commit()
    await db.refresh(certification)

    return certification


async def delete_certification(
    certification_id: int,
    db: AsyncSession,
) -> bool:
    certification = await get_certification_by_id(
        certification_id,
        db,
    )

    if certification is None:
        return False

    await db.delete(certification)
    await db.commit()

    return True
