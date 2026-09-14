from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import auth_user
from db.models.author import Author
from db.queries.author import delete_author, update_author
from db.session import get_db
from schemas.author import AuthorRead, AuthorUpdate


router = APIRouter(tags=["User profile"])


@router.get("/profile", response_model=AuthorRead)
async def get_profile(user: Author = Depends(auth_user)) -> Author:
    return user


@router.patch("/profile", response_model=AuthorRead)
async def update_profile(
    payload: AuthorUpdate,
    db: AsyncSession = Depends(get_db),
    user: Author = Depends(auth_user),
) -> Author:
    fields = payload.model_dump(exclude_unset=True)
    return await update_author(db, user, **fields)


@router.delete("/profile", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    db: AsyncSession = Depends(get_db),
    user: Author = Depends(auth_user),
) -> None:
    await delete_author(db, user)
