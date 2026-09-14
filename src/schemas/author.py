from pydantic import BaseModel, ConfigDict, Field


class AuthorRegister(BaseModel):
    username: str = Field(min_length=3, max_length=64, pattern=r"^[a-zA-Z0-9_]+$")
    name: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=8)


class AuthorLogin(BaseModel):
    username: str
    password: str


class AuthorUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=255)
    bio: str | None = None
    birth_year: int | None = Field(default=None, ge=1, le=2100)


class AuthorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    name: str
    bio: str | None
    birth_year: int | None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
