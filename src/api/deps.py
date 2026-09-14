from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import decode_access_token
from db.models.author import Author
from db.queries.author import get_author_by_id
from db.session import get_db

bearer_scheme = HTTPBearer()


async def auth_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> Author:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(credentials.credentials)
        author_id = payload.get("sub")
        if author_id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    author = await get_author_by_id(db, int(author_id))
    if author is None:
        raise credentials_exception
    return author
