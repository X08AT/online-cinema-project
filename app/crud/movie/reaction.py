from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.movie import MovieReaction, ReactionEnum, Movie
from app.models.user import User


async def set_movie_reaction(
    movie_id: int,
    reaction_type: ReactionEnum,
    user: User,
    db: AsyncSession,
) -> None:
    movie_result = await db.execute(select(Movie).where(Movie.id == movie_id))

    movie = movie_result.scalar_one_or_none()

    if movie is None:
        raise ValueError("Movie not found")

    reaction_result = await db.execute(
        select(MovieReaction).where(
            MovieReaction.movie_id == movie_id,
            MovieReaction.user_id == user.id,
        )
    )

    reaction = reaction_result.scalar_one_or_none()

    if reaction is None:
        reaction = MovieReaction(
            movie_id=movie_id,
            user_id=user.id,
            reaction=reaction_type,
        )
        db.add(reaction)
    else:
        reaction.reaction = reaction_type

    await db.commit()


async def remove_movie_reaction(
    movie_id: int,
    user: User,
    db: AsyncSession,
) -> bool:
    movie_result = await db.execute(select(Movie).where(Movie.id == movie_id))

    movie = movie_result.scalar_one_or_none()

    if movie is None:
        raise ValueError("Movie not found")

    reaction_result = await db.execute(
        select(MovieReaction).where(
            MovieReaction.movie_id == movie_id,
            MovieReaction.user_id == user.id,
        )
    )

    reaction = reaction_result.scalar_one_or_none()

    if reaction is None:
        return False

    await db.delete(reaction)
    await db.commit()

    return True
