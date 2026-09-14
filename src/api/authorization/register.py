from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import create_access_token, hash_password
from db.queries.author import create_author, get_author_by_username
from db.session import get_db
from schemas.author import AuthorRegister, Token

router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    payload: AuthorRegister,
    db: AsyncSession = Depends(get_db),
) -> Token:
    existing = await get_author_by_username(db, payload.username)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Author with this username already exists",
        )

    try:
        author = await create_author(
            db,
            username=payload.username,
            name=payload.name,
            hashed_password=hash_password(payload.password),
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Author with this username already exists",
        )

    return Token(
        access_token=create_access_token(str(author.id)),
    )
