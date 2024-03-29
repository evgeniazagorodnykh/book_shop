from typing import Set, Optional

from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter import FilterDepends
from fastapi_filter.contrib.sqlalchemy import Filter

from database import BookOrm, GenreOrm


class SGenreAdd(BaseModel):
    name: str

    __hash__ = object.__hash__


class SGenre(SGenreAdd):
    id: int


class SBookAddBase(BaseModel):
    name: str
    author: str
    price: float


class SBookAdd(SBookAddBase):
    genres: Set[str]


class SBook(SBookAddBase):
    id: int
    genres: Set[SGenreAdd]
    photo: str


class GenreFilter(Filter):
    model_config = ConfigDict(populate_by_name=True)

    name: Optional[str] = Field(default=None, alias="genre")

    class Constants(Filter.Constants):
        model = GenreOrm


class BookFilter(Filter):
    model_config = ConfigDict(populate_by_name=True)

    name__like: Optional[str] = Field(default=None, alias="name")
    author__like: Optional[str] = Field(default=None, alias="author")
    genre: Optional[GenreFilter] = FilterDepends(GenreFilter)
    price__lte: Optional[float] = Field(default=None, alias="price_to")
    price__qte: Optional[float] = Field(default=None, alias="price_from")

    class Constants(Filter.Constants):
        model = BookOrm
