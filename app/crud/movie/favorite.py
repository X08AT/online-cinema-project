from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.movie import Director, Favorite, Movie, Star


async def favorite_movie_by_id(
    user_id: int,
    movie_id: int,
    db: AsyncSession,
) -> Favorite:
    movie_result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = movie_result.scalar_one_or_none()

    if movie is None:
        raise ValueError("Movie not found")

    favorite_result = await db.execute(
        select(Favorite).where(
            Favorite.movie_id == movie_id,
            Favorite.user_id == user_id,
        )
    )
    favorite = favorite_result.scalar_one_or_none()

    if favorite is not None:
        raise FileExistsError("Movie already favorited")

    favorite = Favorite(
        movie_id=movie_id,
        user_id=user_id,
    )

    db.add(favorite)

    await db.commit()
    await db.refresh(favorite)

    return favorite


async def remove_movie_from_favorite(
    movie_id: int,
    user_id: int,
    db: AsyncSession,
) -> None:
    movie_result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = movie_result.scalar_one_or_none()

    if movie is None:
        raise ValueError("Movie not found")

    favorite_result = await db.execute(
        select(Favorite).where(
            Favorite.movie_id == movie_id,
            Favorite.user_id == user_id,
        )
    )
    favorite = favorite_result.scalar_one_or_none()

    if favorite is None:
        raise ValueError("Favorite not found")

    await db.delete(favorite)
    await db.commit()


async def favorite_movies_list(
    user_id: int,
    db: AsyncSession,
    skip: int,
    limit: int,
    year: int | None = None,
    imdb: float | None = None,
    sort_by: str | None = None,
    sort_order: str = "asc",
    search: str | None = None,
) -> list[Movie]:
    query = (
        select(Movie)
        .options(
            selectinload(Movie.certification),
            selectinload(Movie.genres),
            selectinload(Movie.stars),
            selectinload(Movie.directors),
            selectinload(Movie.reactions),
        )
        .join(Favorite)
        .where(Favorite.user_id == user_id)
    )

    if year is not None:
        query = query.where(Movie.year == year)

    if imdb is not None:
        query = query.where(Movie.imdb >= imdb)

    sort_fields = {
        "price": Movie.price,
        "year": Movie.year,
        "votes": Movie.votes,
    }

    sort_column = sort_fields.get(sort_by) if sort_by is not None else None

    if sort_column is not None:
        if sort_order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

    if search is not None:
        query = query.where(
            or_(
                Movie.name.ilike(f"%{search}%"),
                Movie.description.ilike(f"%{search}%"),
                Movie.stars.any(Star.name.ilike(f"%{search}%")),
                Movie.directors.any(Director.name.ilike(f"%{search}%")),
            )
        )

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    movies = result.scalars().all()

    return list(movies)
