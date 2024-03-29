from __future__ import annotations
from typing import Set

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

engine = create_async_engine(
    "sqlite+aiosqlite:///books.db"
)
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class GenreOrm(Model):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    books: Mapped[Set["BookOrm"]] = relationship(
        back_populates="genres",
        secondary="genre_book"
    )


class BookOrm(Model):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    author: Mapped[str]
    price: Mapped[float]
    photo: Mapped[str]

    genres: Mapped[Set["GenreOrm"]] = relationship(
        back_populates="books",
        secondary="genre_book"
    )


class GenreBookOrm(Model):
    __tablename__ = "genre_book"

    book_id: Mapped[int] = mapped_column(
        ForeignKey("book.id", ondelete="CASCADE"),
        primary_key=True
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey("genre.id", ondelete="CASCADE"),
        primary_key=True
    )


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
