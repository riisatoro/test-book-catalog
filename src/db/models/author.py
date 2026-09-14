from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.session import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    birth_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    books: Mapped[list["Book"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
