from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=PROJECT_ROOT / ".env", extra="ignore")

    SECRET_KEY: str = "dev-secret-change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = f"sqlite+aiosqlite:///{PROJECT_ROOT / 'book_catalog.db'}"

    @field_validator("DATABASE_URL")
    @classmethod
    def resolve_sqlite_url(cls, value: str) -> str:
        prefix = "sqlite+aiosqlite:///"
        if not value.startswith(prefix):
            return value
        db_path = Path(value.removeprefix(prefix))
        if not db_path.is_absolute():
            db_path = PROJECT_ROOT / db_path
        return f"sqlite+aiosqlite:///{db_path.resolve().as_posix()}"


settings = Settings()
