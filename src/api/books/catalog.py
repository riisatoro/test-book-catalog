from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.book import Book
from db.queries.book import get_book_by_id, list_books
from db.session import get_db
from schemas.book import BookList, BookRead

router = APIRouter(tags=["Catalog"])
DEFAULT_PAGE_SIZE = 10


@router.get("/catalog", response_model=BookList)
async def get_catalog(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=DEFAULT_PAGE_SIZE, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> BookList:
    offset = (page - 1) * page_size
    books, total_items = await list_books(db, offset=offset, limit=page_size)
    return BookList.from_page(
        books,
        page=page,
        page_size=page_size,
        total_items=total_items,
    )


@router.get("/catalog/{book_id}", response_model=BookRead)
async def get_catalog_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
) -> Book:
    book = await get_book_by_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book
