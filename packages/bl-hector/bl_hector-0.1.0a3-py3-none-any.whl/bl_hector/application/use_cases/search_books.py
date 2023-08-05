# Hector --- A collection manager.
# Copyright © 2023 Bioneland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from bl_hector.domain.collection_management.entities import Book
from bl_hector.domain.collection_management.exceptions import IncorrectValue
from bl_hector.domain.collection_management.repositories import Books
from bl_hector.domain.collection_management.value_objects import (
    Author,
    Genre,
    Isbn,
    Title,
    Year,
)


@dataclass(frozen=True)
class Request:
    isbn: Optional[str] = None
    title: Optional[str] = None
    year: Optional[int] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    page_number: Optional[int] = None
    page_size: Optional[int] = None


class Presenter(ABC):
    @abstractmethod
    def bad_request(self) -> None:
        ...

    @abstractmethod
    def book(self, book: Book) -> None:
        ...


@dataclass(frozen=True)
class Interactor:
    presenter: Presenter
    books: Books

    def execute(self, request: Request) -> None:
        isbn = None
        title = None
        year = None
        author = None
        genre = None

        try:
            if request.isbn:
                isbn = Isbn.instanciate(request.isbn)
            if request.title:
                title = Title.instanciate(request.title)
            if request.year is not None:
                year = Year.instanciate(request.year)
            if request.author:
                author = Author.instanciate(request.author)
            if request.genre:
                genre = Genre.instanciate(request.genre)
        except IncorrectValue:
            return self.presenter.bad_request()

        books = self.books.search(
            isbn=isbn,
            title=title,
            year=year,
            author=author,
            genre=genre,
            page_number=request.page_number,
            page_size=request.page_size,
        )
        for book in books:
            self.presenter.book(book)
