from fastapi_filter import FilterDepends
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import BookOrm, new_session, GenreOrm
from schemas import BookFilter, SBook, SBookAdd, SGenreAdd


class BookRepository:
    @classmethod
    async def add_one_book(cls, data: SBookAdd, file_bytes: bytes) -> int:
        async with new_session() as session:
            book_dict = data.model_dump()
            book_dict["photo"] = file_bytes
            genres = book_dict.pop("genres")
            book = BookOrm(**book_dict)
            for genre in genres:
                query = select(GenreOrm).where(GenreOrm.name == genre)
                result = await session.execute(query)
                book.genres.add(result.scalars().first())
            session.add(book)
            await session.flush()
            await session.commit()
            return book.id

    @classmethod
    async def find_all_books(
        cls,
        book_filter: BookFilter = FilterDepends(BookFilter)
    ) -> list[SBook]:
        async with new_session() as session:
            query = book_filter.filter(
                select(BookOrm)
                .options(selectinload(BookOrm.genres).load_only(GenreOrm.name))
            )
            result = await session.execute(query)
            book_models = result.unique().scalars().all()
            print(f"{book_models=}")
            book_schemas = [SBook.model_validate(
                book_model, from_attributes=True) for book_model in book_models]
            return book_schemas

    @classmethod
    async def add_one_genre(cls, data: SGenreAdd) -> int:
        async with new_session() as session:
            genre_dict = data.model_dump()

            genre = GenreOrm(**genre_dict)
            session.add(genre)
            await session.flush()
            await session.commit()
            return genre.name
