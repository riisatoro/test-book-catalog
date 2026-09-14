from pydantic import BaseModel, ConfigDict, Field


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    published_year: int = Field(ge=1, le=2100)


class BookUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=1, max_length=255)
    published_year: int | None = Field(default=None, ge=1, le=2100)


class BookRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    published_year: int
    author_id: int


class Pagination(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int


class BookList(BaseModel):
    items: list[BookRead]
    pagination: Pagination

    @classmethod
    def from_page(
        cls,
        books: list,
        *,
        page: int,
        page_size: int,
        total_items: int,
    ) -> "BookList":
        total_pages = (total_items + page_size - 1) // page_size if total_items else 0
        return cls(
            items=[BookRead.model_validate(book) for book in books],
            pagination=Pagination(
                page=page,
                page_size=page_size,
                total_items=total_items,
                total_pages=total_pages,
            ),
        )
