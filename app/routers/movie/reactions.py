from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.movie.reaction import remove_movie_reaction, set_movie_reaction
from app.db.dependencies import get_db, get_current_user
from app.models.movie import ReactionEnum
from app.models.user import User

router = APIRouter(tags=["Reactions"])


@router.post("/movies/{movie_id}/like", status_code=201)
async def like_movie(
        movie_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        await set_movie_reaction(movie_id, ReactionEnum.LIKE, current_user, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {"message": "Movie liked successfully"}


@router.post("/movies/{movie_id}/dislike", status_code=201)
async def dislike_movie(
        movie_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        await set_movie_reaction(
            movie_id,
            ReactionEnum.DISLIKE,
            current_user,
            db
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "Movie disliked successfully"}


@router.delete("/movies/{movie_id}/reaction", status_code=200)
async def delete_movie_reaction(
        movie_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        deleted = await remove_movie_reaction(movie_id, current_user, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    if not deleted:
        raise HTTPException(status_code=404, detail="Movie reaction not found")

    return {"message": "Movie reaction deleted successfully"}
