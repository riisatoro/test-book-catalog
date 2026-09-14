from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.author import Author


async def get_author_by_id(db: AsyncSession, author_id: int) -> Author | None:
    result = await db.execute(select(Author).where(Author.id == author_id))
    return result.scalar_one_or_none()


async def get_author_by_username(db: AsyncSession, username: str) -> Author | None:
    result = await db.execute(select(Author).where(Author.username == username))
    return result.scalar_one_or_none()


async def create_author(
    db: AsyncSession,
    *,
    username: str,
    name: str,
    hashed_password: str,
    bio: str | None = None,
    birth_year: int | None = None,
) -> Author:
    author = Author(
        username=username,
        name=name,
        bio=bio,
        birth_year=birth_year,
        hashed_password=hashed_password,
    )
    db.add(author)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise
    await db.refresh(author)
    return author


async def update_author(db: AsyncSession, author: Author, **fields) -> Author:
    for key, value in fields.items():
        setattr(author, key, value)
    await db.commit()
    await db.refresh(author)
    return author


async def delete_author(db: AsyncSession, author: Author) -> None:
    await db.delete(author)
    await db.commit()
