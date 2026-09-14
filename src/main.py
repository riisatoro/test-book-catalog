from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from api.authorization import router as auth_router
from api.books.books import router as books_router
from api.books.catalog import router as catalog_router
from api.profile.profile import router as profile_router
from db.models import Author, Book  # noqa: F401 — register metadata before create_all
from db.session import Base, engine


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="Book Catalog",
    lifespan=lifespan,
    swagger_ui_parameters={"persistAuthorization": True},
)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(profile_router, prefix="/api/v1")
app.include_router(books_router, prefix="/api/v1")
app.include_router(catalog_router, prefix="/api/v1")
