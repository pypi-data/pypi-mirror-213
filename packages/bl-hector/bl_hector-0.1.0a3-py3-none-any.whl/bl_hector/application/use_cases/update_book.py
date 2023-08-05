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

from bl_hector.domain.collection_management.entities import Book
from bl_hector.domain.collection_management.exceptions import IncorrectValue
from bl_hector.domain.collection_management.repositories import Books
from bl_hector.domain.collection_management.value_objects import (
    Author,
    Cover,
    Genre,
    Isbn,
    Title,
    Year,
)


@dataclass(frozen=True)
class Request:
    isbn: str
    title: str
    year: int
    authors: list[str]
    genres: list[str]
    cover: str = ""


class Presenter(ABC):
    @abstractmethod
    def bad_request(self) -> None:
        ...

    @abstractmethod
    def book_not_found(self, isbn: Isbn) -> None:
        ...

    @abstractmethod
    def book_updated(self, book: Book) -> None:
        ...


@dataclass(frozen=True)
class Interactor:
    presenter: Presenter
    books: Books

    def execute(self, request: Request) -> None:
        try:
            # There's no business logic to apply when updating a book.
            book = Book.instanciate(
                Isbn.instanciate(request.isbn),
                Title.instanciate(request.title),
                Year.instanciate(request.year),
                [Author.instanciate(a) for a in request.authors if a],
                [Genre.instanciate(g) for g in request.genres if g],
                Cover.instanciate(request.cover) if request.cover else None,
            )
        except IncorrectValue:
            return self.presenter.bad_request()

        if not self.books.search(isbn=book.isbn):
            return self.presenter.book_not_found(book.isbn)

        self.books.update(book)
        self.presenter.book_updated(book)
