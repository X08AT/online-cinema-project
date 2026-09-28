from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.movie import (
    MovieComment,
    Movie,
    CommentLike,
    Notification,
    NotificationTypeEnum
)
from app.schemas.movie import CommentCreateModel, CommentUpdateModel


async def create_comment(
        user_id: int,
        movie_id: int,
        data: CommentCreateModel,
        db: AsyncSession
) -> MovieComment:
    result = await db.execute(select(Movie).where(Movie.id == movie_id))

    movie = result.scalar_one_or_none()

    if movie is None:
        raise ValueError("Movie not found")

    comment = MovieComment(
        user_id=user_id,
        movie_id=movie_id,
        **data.model_dump()
    )
    db.add(comment)
    await db.commit()

    return await get_comment_by_id(comment.id, db)


async def get_comments_by_movie_id(
        movie_id: int,
        db: AsyncSession
) -> list[MovieComment]:
    result = await db.execute(
        select(MovieComment)
        .options(
            selectinload(MovieComment.likes),
            selectinload(MovieComment.replies).selectinload(MovieComment.likes)
        )
        .where(
            MovieComment.movie_id == movie_id,
            MovieComment.parent_id.is_(None)
        )
    )

    comments = result.scalars().all()

    return comments


async def update_comment(
        comment_id: int,
        user_id: int,
        data: CommentUpdateModel,
        db: AsyncSession
) -> MovieComment:
    result = await db.execute(
        select(MovieComment)
        .where(MovieComment.id == comment_id)
    )

    comment = result.scalar_one_or_none()

    if comment is None:
        raise ValueError("Comment not found")

    if comment.user_id != user_id:
        raise PermissionError("Not your comment")

    comment.content = data.content

    await db.commit()

    return await get_comment_by_id(comment.id, db)


async def delete_comment(
        comment_id: int,
        user_id: int,
        db: AsyncSession
) -> None:
    result = await db.execute(
        select(MovieComment)
        .where(MovieComment.id == comment_id)
    )

    comment = result.scalar_one_or_none()

    if comment is None:
        raise ValueError("Comment not found")

    if comment.user_id != user_id:
        raise PermissionError("Not your comment")

    await db.delete(comment)
    await db.commit()


async def create_reply(
        comment_id: int,
        user_id: int,
        data: CommentCreateModel,
        db: AsyncSession
) -> MovieComment:
    result = await db.execute(
        select(MovieComment)
        .where(MovieComment.id == comment_id)
    )

    comment = result.scalar_one_or_none()

    if comment is None:
        raise ValueError("Comment not found")

    reply = MovieComment(
        user_id=user_id,
        movie_id=comment.movie_id,
        parent_id=comment_id,
        **data.model_dump()
    )

    db.add(reply)

    if user_id != comment.user_id:
        notification = Notification(
            user_id=comment.user_id,
            comment_id=comment_id,
            notification_type=NotificationTypeEnum.COMMENT_REPLY,
        )

        db.add(notification)

    await db.commit()

    return await get_comment_by_id(reply.id, db)


async def get_comment_by_id(
        comment_id: int,
        db: AsyncSession
) -> MovieComment | None:
    result = await db.execute(
        select(MovieComment)
        .options(
            selectinload(MovieComment.likes),
            selectinload(MovieComment.replies).selectinload(MovieComment.likes)
        )
        .where(MovieComment.id == comment_id)
    )

    return result.scalar_one_or_none()


async def like_comment(
        comment_id: int,
        user_id: int,
        db: AsyncSession
) -> None:
    comment = await get_comment_by_id(comment_id, db)

    if comment is None:
        raise ValueError("Comment not found")

    result = await db.execute(
        select(CommentLike)
        .where(
            CommentLike.comment_id == comment_id,
            CommentLike.user_id == user_id)
    )

    comment_like = result.scalar_one_or_none()

    if comment_like is not None:
        raise FileExistsError("Comment already liked")

    new_comment_like = CommentLike(
        user_id=user_id,
        comment_id=comment_id,
    )

    db.add(new_comment_like)

    if user_id != comment.user_id:
        notification = Notification(
            user_id=comment.user_id,
            comment_id=comment_id,
            notification_type=NotificationTypeEnum.COMMENT_LIKED,
        )

        db.add(notification)

    await db.commit()


async def remove_like(
        comment_id: int,
        user_id: int,
        db: AsyncSession
) -> None:
    result = await db.execute(
        select(CommentLike)
        .where(
            CommentLike.comment_id == comment_id,
            CommentLike.user_id == user_id
        )
    )

    liked = result.scalar_one_or_none()

    if liked is None:
        raise ValueError("Like not found")

    await db.delete(liked)
    await db.commit()
