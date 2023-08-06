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
from pathlib import Path
from typing import Optional

from bl_hector.domain.collection_management.entities import Book
from bl_hector.domain.collection_management.repositories import Books
from bl_hector.domain.collection_management.services import InfoProvider
from bl_hector.domain.collection_management.value_objects import Isbn


@dataclass(frozen=True)
class Request:
    path: str


class Presenter(ABC):
    @abstractmethod
    def file_does_not_exist(self, path: str) -> None:
        ...

    @abstractmethod
    def line_skipped(self, line_number: int, text: str, reason: str) -> None:
        ...

    @abstractmethod
    def book_already_exists(self, book: Book) -> None:
        ...

    @abstractmethod
    def book_info_not_found(self, isbn: Isbn) -> None:
        ...

    @abstractmethod
    def book_added(self, book: Book) -> None:
        ...


@dataclass(frozen=True)
class Interactor:
    """
    **WARNING:** This use case is not specified, for it is not trivial!
    It is also not a use case that should actually be used! It might even be removed.
    It might be better to implement it by wireing the other commands together.
    This would solve the problem of the commit of the data. For the time being
    the commit only happens once at the end of the command, even if thousands of books
    have to be imported!?
    """

    presenter: Presenter
    info_provider: InfoProvider
    books: Books

    def execute(self, request: Request) -> None:
        path = Path(request.path)
        if not path.is_file():
            return self.presenter.file_does_not_exist(request.path)

        for isbn in self.__extract_isbn_from_file(path):
            if book := self.books.by_isbn(isbn):
                self.presenter.book_already_exists(book)
                continue
            if not (book := self.info_provider.look_up(isbn)):
                self.presenter.book_info_not_found(isbn)
                continue
            self.books.add(book)
            self.presenter.book_added(book)

    def __extract_isbn_from_file(self, path: Path) -> list[Isbn]:
        return [
            isbn
            for number, text in enumerate(path.read_text().splitlines())
            if (isbn := self.__extract_isbn_from_line(number, text))
        ]

    def __extract_isbn_from_line(self, number: int, text: str) -> Optional[Isbn]:
        _text = text.strip()
        if "#" in _text:
            if _text.startswith("#"):
                return None
            _text = text.split("#", 1)[0]

        try:
            return Isbn.instanciate(_text)
        except Exception as exc:
            return self.presenter.line_skipped(number, text, str(exc))
