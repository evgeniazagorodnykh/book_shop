from fastapi import APIRouter, Depends, File
from typing import Annotated

from fastapi_filter import FilterDepends

from repository import BookRepository
from schemas import SBook, SBookAdd, SGenreAdd, BookFilter


router = APIRouter(
    prefix="/books",
    tags=["Книги"],
)


@router.post("/add_genre")
async def add_genre(
    genre: Annotated[SGenreAdd, Depends()],
):
    genre = await BookRepository.add_one_genre(genre)
    return genre


@router.post("/add_books")
async def add_books(
    book: Annotated[SBookAdd, Depends()],
    file_bytes: bytes = File()
) -> dict:
    await BookRepository.add_one_book(book, str(file_bytes))
    return {"sucsess": True}


@router.get("/find_books")
async def find_books(
    book_filter: BookFilter = FilterDepends(BookFilter)
) -> list[SBook]:
    books = await BookRepository.find_all_books(book_filter)
    return books
