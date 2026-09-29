from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.movie import Movie, Favorite


async def favorite_movie_by_id(
        user_id: int,
        movie_id: int,
        db: AsyncSession
) -> Favorite:
    result = await db.execute(select(Movie).filter(Movie.id == movie_id))

    movie = result.scalar_one_or_none()

    if movie is None:
        raise ValueError("Movie not found")

    result = await db.execute(
        select(Favorite)
        .where(
            Favorite.movie_id == movie_id,
            Favorite.user_id == user_id
        )
    )

    favorite = result.scalar_one_or_none()

    if favorite is not None:
        raise FileExistsError("Movie already favorited")

    favorite = Favorite(
        movie_id=movie_id,
        user_id=user_id
    )

    db.add(favorite)

    await db.commit()
    await db.refresh(favorite)

    return favorite


async def remove_movie_from_favorite(
        movie_id: int,
        user_id: int,
        db: AsyncSession
) -> None:
    result = await db.execute(
        select(Movie).where(Movie.id == movie_id)
    )

    movie = result.scalar_one_or_none()

    if movie is None:
        raise ValueError("Movie not found")

    result = await db.execute(
        select(Favorite)
        .where(
            Favorite.movie_id == movie_id,
            Favorite.user_id == user_id
        )
    )

    favorite = result.scalar_one_or_none()

    if favorite is None:
        raise ValueError("Favorite not found")

    await db.delete(favorite)
    await db.commit()
