from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.movie import Movie, MovieRating
from app.schemas.movie.rating import MovieRatingModel


async def set_movie_rating(
    movie_id: int,
    user_id: int,
    data: MovieRatingModel,
    db: AsyncSession,
) -> MovieRating:
    movie_result = await db.execute(select(Movie).where(Movie.id == movie_id))

    movie = movie_result.scalar_one_or_none()

    if movie is None:
        raise ValueError("Movie not found")

    rating_result = await db.execute(
        select(MovieRating).where(
            MovieRating.movie_id == movie_id,
            MovieRating.user_id == user_id,
        )
    )

    rating = rating_result.scalar_one_or_none()

    if rating is None:
        rating = MovieRating(
            movie_id=movie.id,
            user_id=user_id,
            **data.model_dump(),
        )
        db.add(rating)

    rating.rating = data.rating

    await db.commit()
    await db.refresh(rating)

    return rating


async def delete_movie_rating(
    movie_id: int,
    user_id: int,
    db: AsyncSession,
) -> None:
    movie_result = await db.execute(select(Movie).where(Movie.id == movie_id))

    movie = movie_result.scalar_one_or_none()

    if movie is None:
        raise ValueError("Movie not found")

    rating_result = await db.execute(
        select(MovieRating).where(
            MovieRating.movie_id == movie_id,
            MovieRating.user_id == user_id,
        )
    )

    rating = rating_result.scalar_one_or_none()

    if rating is None:
        raise ValueError("Rating not found")

    await db.delete(rating)
    await db.commit()


async def get_movie_ratings(
    movie_id: int,
    user_id: int,
    db: AsyncSession,
) -> dict:
    movie_result = await db.execute(select(Movie).where(Movie.id == movie_id))

    movie = movie_result.scalar_one_or_none()

    if movie is None:
        raise ValueError("Movie not found")

    ratings_result = await db.execute(
        select(
            func.avg(MovieRating.rating),
            func.count(MovieRating.id),
        ).where(
            MovieRating.movie_id == movie_id,
        )
    )

    average_rating, ratings_count = ratings_result.one()

    user_rating_result = await db.execute(
        select(MovieRating.rating).where(
            MovieRating.movie_id == movie_id,
            MovieRating.user_id == user_id,
        )
    )

    user_rating = user_rating_result.scalar_one_or_none()

    return {
        "average_rating": (
            float(average_rating) if average_rating is not None else None
        ),
        "ratings_count": ratings_count,
        "user_rating": user_rating,
    }
