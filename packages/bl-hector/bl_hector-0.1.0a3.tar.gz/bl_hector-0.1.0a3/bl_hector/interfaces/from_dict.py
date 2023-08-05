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

from typing import Any, Optional

from werkzeug.datastructures import MultiDict

from bl_hector.application.use_cases import add_book, search_books, update_book
from bl_hector.interfaces import validators


class SearchBooks:
    def __init__(
        self, data: MultiDict[str, Any], /, *, page_size: Optional[int] = None
    ) -> None:
        self.__data = data
        self.__page_size = page_size

    def call(self, interactor: search_books.Interactor) -> None:
        if not self.__data:
            return

        validator = validators.SearchBooks(self.__data)
        if not validator.is_ok:
            return

        d = self.__data
        interactor.execute(
            search_books.Request(
                isbn=str(v) if (v := d.get("isbn")) else None,
                title=str(v) if (v := d.get("title")) else None,
                year=int(v) if (v := d.get("year")) else None,
                author=str(v) if (v := d.get("author")) else None,
                genre=str(v) if (v := d.get("genre")) else None,
                page_number=int(v) if (v := d.get("page")) else None,
                page_size=self.__page_size,
            )
        )


class AddBook:
    def __init__(self, data: MultiDict[str, Any]) -> None:
        self.__data = data

    def call(self, interactor: add_book.Interactor) -> None:
        if not self.__data:
            return

        validator = validators.AddBook(self.__data)
        if not validator.is_ok:
            return

        d = self.__data
        interactor.execute(
            add_book.Request(
                isbn=str(d.get("isbn", "")),
                title=str(d.get("title", "")),
                year=int(d.get("year", "")),
                authors=[a.strip() for a in d.get("authors", "").split(",")],
                genres=[g.strip() for g in d.get("genres", "").split(",")],
                cover=str(d.get("cover", "")),
            )
        )


class UpdateBook:
    def __init__(self, isbn: str, data: MultiDict[str, Any]) -> None:
        self.__isbn = isbn
        self.__data = data

    def call(self, interactor: update_book.Interactor) -> None:
        if not self.__data:
            return

        validator = validators.UpdateBook(self.__data)
        if not validator.is_ok:
            return

        d = self.__data
        interactor.execute(
            update_book.Request(
                isbn=self.__isbn,
                title=str(d.get("title", "")),
                year=int(d.get("year", "")),
                authors=[a.strip() for a in d.get("authors", "").split(",")],
                genres=[g.strip() for g in d.get("genres", "").split(",")],
                cover=str(d.get("cover", "")),
            )
        )
