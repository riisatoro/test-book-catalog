from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.book import Book


async def get_book_by_id(db: AsyncSession, book_id: int) -> Book | None:
    result = await db.execute(select(Book).where(Book.id == book_id))
    return result.scalar_one_or_none()


async def get_author_book(
    db: AsyncSession,
    book_id: int,
    author_id: int,
) -> Book | None:
    result = await db.execute(
        select(Book).where(Book.id == book_id, Book.author_id == author_id)
    )
    return result.scalar_one_or_none()


async def list_books(
    db: AsyncSession,
    *,
    offset: int,
    limit: int,
    author_id: int | None = None,
) -> tuple[list[Book], int]:
    books_query = select(Book)
    count_query = select(func.count()).select_from(Book)
    if author_id is not None:
        books_query = books_query.where(Book.author_id == author_id)
        count_query = count_query.where(Book.author_id == author_id)

    total = await db.scalar(count_query)
    result = await db.execute(
        books_query.order_by(Book.id.desc()).offset(offset).limit(limit)
    )
    return list(result.scalars().all()), int(total or 0)


async def create_book(
    db: AsyncSession,
    *,
    title: str,
    published_year: int,
    author_id: int,
) -> Book:
    book = Book(title=title, published_year=published_year, author_id=author_id)
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book


async def update_book(db: AsyncSession, book: Book, **fields) -> Book:
    for key, value in fields.items():
        setattr(book, key, value)
    await db.commit()
    await db.refresh(book)
    return book


async def delete_book(db: AsyncSession, book: Book) -> None:
    await db.delete(book)
    await db.commit()
