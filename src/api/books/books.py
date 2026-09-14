from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import auth_user
from db.models.author import Author
from db.models.book import Book
from db.queries.book import (
    create_book,
    delete_book,
    get_author_book,
    list_books,
    update_book,
)
from db.session import get_db
from schemas.book import BookCreate, BookList, BookRead, BookUpdate

router = APIRouter(tags=["Author Books"])
DEFAULT_PAGE_SIZE = 10


@router.get("/books/my", response_model=BookList)
async def get_my_books(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=DEFAULT_PAGE_SIZE, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: Author = Depends(auth_user),
) -> BookList:
    offset = (page - 1) * page_size
    books, total_items = await list_books(
        db,
        offset=offset,
        limit=page_size,
        author_id=user.id,
    )
    return BookList.from_page(
        books,
        page=page,
        page_size=page_size,
        total_items=total_items,
    )


@router.post("/books", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book_endpoint(
    payload: BookCreate,
    db: AsyncSession = Depends(get_db),
    user: Author = Depends(auth_user),
) -> Book:
    return await create_book(
        db,
        title=payload.title,
        published_year=payload.published_year,
        author_id=user.id,
    )


@router.get("/books/{book_id}", response_model=BookRead)
async def get_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    user: Author = Depends(auth_user),
) -> Book:
    book = await get_author_book(db, book_id, user.id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.patch("/books/{book_id}", response_model=BookRead)
async def update_book_endpoint(
    book_id: int,
    payload: BookUpdate,
    db: AsyncSession = Depends(get_db),
    user: Author = Depends(auth_user),
) -> Book:
    book = await get_author_book(db, book_id, user.id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    fields = payload.model_dump(exclude_unset=True)
    return await update_book(db, book, **fields)


@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_endpoint(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    user: Author = Depends(auth_user),
) -> None:
    book = await get_author_book(db, book_id, user.id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    await delete_book(db, book)
