from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import decode_access_token
from db.models.author import Author
from db.queries.author import get_author_by_id
from db.session import get_db

authorization_header = APIKeyHeader(
    name="Authorization",
    scheme_name="Authorization",
    description="JWT from /api/v1/login or /api/v1/register.",
    auto_error=False,
)


async def auth_user(
    authorization: Annotated[str | None, Depends(authorization_header)],
    db: AsyncSession = Depends(get_db),
) -> Author:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    if not authorization:
        raise credentials_exception
    try:
        payload = decode_access_token(authorization)
        author_id = payload.get("sub")
        if author_id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    author = await get_author_by_id(db, int(author_id))
    if author is None:
        raise credentials_exception
    return author
