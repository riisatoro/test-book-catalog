from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from api.authorization import router as auth_router
from db.models import Author  # noqa: F401 — register metadata before create_all
from db.session import Base, engine


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="Book Catalog", lifespan=lifespan)
app.include_router(auth_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        app_dir=str(Path(__file__).resolve().parent),
    )
