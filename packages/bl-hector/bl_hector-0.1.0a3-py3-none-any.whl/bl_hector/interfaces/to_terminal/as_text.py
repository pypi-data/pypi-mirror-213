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

from typing import Callable

from bl_hector.application.use_cases import add_book, import_books
from bl_hector.domain.collection_management.entities import Book
from bl_hector.domain.collection_management.value_objects import Isbn
from bl_hector.interfaces.l10n import DummyTranslator, Translator
from bl_hector.interfaces.to_terminal import ExitCodes, LookUpBookInterface


class LookUpBook(LookUpBookInterface):
    def __init__(
        self,
        printer: Callable[[str], None],
        /,
        *,
        translator: Translator = DummyTranslator(),
    ) -> None:
        self.__printer = printer
        self.__exit_code = ExitCodes.USAGE
        self._ = translator

    def not_an_isbn(self, isbn: str) -> None:
        self.__exit_code = ExitCodes.BAD_REQUEST
        self.__printer(self._("not-an-isbn"))

    def book_not_found(self, isbn: Isbn) -> None:
        self.__exit_code = ExitCodes.NOT_FOUND
        self.__printer(self._("book-not-found"))

    def book(self, book: Book) -> None:
        self.__exit_code = ExitCodes.OK
        self.__info(self._("book-isbn"), str(book.isbn))
        self.__info(self._("book-title"), str(book.title))
        self.__info(self._("book-year"), str(book.year))
        self.__info(self._("book-authors"), ", ".join([str(b) for b in book.authors]))
        if book.genres:
            self.__info(self._("book-genres"), ", ".join([str(g) for g in book.genres]))

    def __info(self, name: str, value: str) -> None:
        self.__printer(self._("info-line", name=name, value=value))

    def exit_code(self) -> int:
        return self.__exit_code.value


class AddBook(add_book.Presenter):
    def __init__(
        self,
        printer: Callable[[str], None],
        /,
        *,
        translator: Translator = DummyTranslator(),
    ) -> None:
        self.__printer = printer
        self.__exit_code = ExitCodes.USAGE
        self._ = translator

    def bad_request(self) -> None:
        self.__exit_code = ExitCodes.BAD_REQUEST
        self.__printer(self._("book-cannot-be-added"))

    def book_already_exists(self, book: Book) -> None:
        self.__exit_code = ExitCodes.BAD_REQUEST
        self.__printer(self._("book-already-exists"))

    def book_added(self, book: Book) -> None:
        self.__exit_code = ExitCodes.OK
        self.__printer(self._("book-added"))

    def exit_code(self) -> int:
        return self.__exit_code.value


class ImportBooks(import_books.Presenter):
    def __init__(
        self,
        printer: Callable[[str], None],
        # Not l10n… because it might soon be removed!
        translator: Translator = DummyTranslator(),
    ) -> None:
        self.__printer = printer
        self.__exit_code = ExitCodes.OK

    def file_does_not_exist(self, path: str) -> None:
        self.__exit_code = ExitCodes.USAGE
        self.__printer(f"File does not exist: {path}.")

    def line_skipped(self, line_number: int, text: str, reason: str) -> None:
        self.__exit_code = ExitCodes.USAGE
        self.__printer(f"Line {line_number} skipped for '{reason}' was '{text}'.")

    def book_already_exists(self, book: Book) -> None:
        self.__printer(f"Book already in the collection: {book.isbn}.")

    def book_info_not_found(self, isbn: Isbn) -> None:
        self.__printer(f"No info could be found for '{isbn}'.")

    def book_added(self, book: Book) -> None:
        self.__printer(f"Book '{book.isbn}' added: \"{book.title}\".")

    def exit_code(self) -> int:
        return self.__exit_code.value
