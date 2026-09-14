from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import create_access_token, verify_password
from db.queries.author import get_author_by_username
from db.session import get_db
from schemas.author import AuthorLogin, AuthorRead, Token

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    payload: AuthorLogin,
    db: AsyncSession = Depends(get_db),
) -> Token:
    author = await get_author_by_username(db, payload.username)
    if author is None or not verify_password(payload.password, author.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return Token(
        access_token=create_access_token(str(author.id)),
        author=AuthorRead.model_validate(author),
    )
