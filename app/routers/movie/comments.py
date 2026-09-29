from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.movie.comment import (
    remove_like,
    create_reply,
    delete_comment,
    update_comment,
    like_comment,
    create_comment,
    get_comments_by_movie_id
)
from app.db.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.movie.comment import (
    CommentResponseModel,
    CommentCreateModel,
    ReplyResponseModel,
    CommentUpdateModel
)

router = APIRouter()


@router.post(
    "/movies/{movie_id}/comments",
    status_code=201,
    response_model=CommentResponseModel
)
async def comment_movie(
        data: CommentCreateModel,
        movie_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        comment = await create_comment(current_user.id, movie_id, data, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return comment


@router.get(
    "/movies/{movie_id}/comments",
    status_code=200,
    response_model=list[CommentResponseModel]
)
async def movie_comments(
        movie_id: int,
        db: AsyncSession = Depends(get_db),
):
    comments = await get_comments_by_movie_id(movie_id, db)

    return comments


@router.patch(
    "/comments/{comment_id}",
    status_code=200,
    response_model=CommentResponseModel
)
async def comment_update(
        comment_id: int,
        data: CommentUpdateModel,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        comment = await update_comment(comment_id, current_user.id, data, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    return comment


@router.delete(
    "/comments/{comment_id}",
    status_code=200,
)
async def comment_delete(
        comment_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        await delete_comment(comment_id, current_user.id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    return {"message": "Comment deleted successfully"}


@router.post(
    "/comments/{comment_id}/replies",
    status_code=201,
    response_model=ReplyResponseModel
)
async def reply_on_comment(
        comment_id: int,
        data: CommentCreateModel,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        reply = await create_reply(comment_id, current_user.id, data, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return reply


@router.post(
    "/comments/{comment_id}/like",
    status_code=201,
)
async def comment_like(
        comment_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        await like_comment(comment_id, current_user.id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except FileExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))

    return {"message": "Comment liked successfully"}


@router.delete(
    "/comments/{comment_id}/like",
    status_code=204,
)
async def remove_comment_like(
        comment_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        await remove_like(comment_id, current_user.id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
