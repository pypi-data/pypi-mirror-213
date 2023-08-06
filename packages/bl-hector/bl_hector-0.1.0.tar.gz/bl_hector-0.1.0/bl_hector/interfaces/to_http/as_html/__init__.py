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

import logging
from http import HTTPStatus as HTTP
from pathlib import Path
from typing import Any, Callable, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2_fragments import render_block
from werkzeug.datastructures import MultiDict

from bl_hector.application.use_cases import (
    add_book,
    display_book,
    look_up_book,
    search_books,
    update_book,
)
from bl_hector.domain.collection_management import errors, validators
from bl_hector.domain.collection_management.entities import Book
from bl_hector.domain.collection_management.value_objects import Isbn
from bl_hector.interfaces import User, l10n, translate_error
from bl_hector.interfaces.to_http import HttpPresenter

ENVIRONMENT = Environment(
    loader=FileSystemLoader([Path(__file__).parent / "templates"]),
    autoescape=select_autoescape(),
    extensions=["bl_hector.interfaces.utils.PatchedPyPugJSExtension"],
)


def register_jinja_global(key: str, value: Any) -> None:
    ENVIRONMENT.globals[key] = value


def url_for(*args: Any, **kwargs: Any) -> str:
    if "url_for" not in ENVIRONMENT.globals:
        raise RuntimeError("`url_for` is not declared on the environment!")
    return ENVIRONMENT.globals["url_for"](*args, **kwargs)  # type: ignore


class JinjaPresenter(HttpPresenter):
    def __init__(
        self,
        template: str,
        /,
        *,
        fragment: str = "",
        user: Optional[User] = None,
        **context: Any,
    ) -> None:
        self.__status_code = HTTP.OK
        self.__headers = {"Content-Type": "text/html; charset=UTF-8"}
        self.__template = template if template.endswith(".pug") else f"{template}.pug"
        self.__fragment = fragment
        self.__user = user
        self.__context: dict[str, Any] = {**context, "_": self._, "user": user}
        self.__error = ""

        self.__adapt_to(user)

    def __adapt_to(self, user: Optional[User] = None) -> None:
        locale = user.locale if (user and user.locale) else l10n.DEFAULT_LOCALE
        self.__localization = l10n.localization(locale)

    def _(self, message_id: str, **kwargs: Any) -> str:
        return str(self.__localization.format_value(message_id, kwargs))

    def translate_error(self, error: Optional[errors.IncorrectValue] = None) -> str:
        return translate_error(self._, error)

    def status_code(self) -> int:
        return int(self.__status_code)

    def headers(self) -> dict[str, str]:
        return self.__headers

    def data(self) -> str:
        return self.render()

    def set_status_code(self, status_code: HTTP) -> None:
        self.__status_code = status_code

    def set_header(self, name: str, value: str) -> None:
        self.__headers[name] = value

    def error(self, message: str, status_code: HTTP) -> None:
        self.__error = message
        self.set_status_code(status_code)

    def redirect(self, url: str, status_code: HTTP = HTTP.SEE_OTHER) -> None:
        if "Content-Type" in self.__headers:
            del self.__headers["Content-Type"]
        self.__headers["Location"] = url
        self.set_status_code(status_code)

    def not_authorized(self) -> None:
        if self.__user:
            self.set_status_code(HTTP.FORBIDDEN)
            self.__error = self._("access-forbidden")
        else:
            self.set_status_code(HTTP.UNAUTHORIZED)
            self.__error = self._("access-not-authorized")

    def render(self, **context: Any) -> str:
        if self.__error:
            return ENVIRONMENT.get_template("error.pug").render(
                **self.__context, **context, message=self.__error
            )
        if self.__fragment:
            return render_block(  # type: ignore
                ENVIRONMENT,
                self.__template,
                self.__fragment,
                **self.__context,
                **context,
            )
        return ENVIRONMENT.get_template(self.__template).render(
            **self.__context, **context
        )


class SearchBooks(JinjaPresenter, search_books.Presenter):
    PAGE_SIZE = 9

    def __init__(
        self,
        data: MultiDict[str, Any],
        /,
        *,
        fragment: str = "",
        user: Optional[User] = None,
    ) -> None:
        super().__init__("books/search", fragment=fragment, user=user)
        self.__data = data
        self.__context: dict[str, Any] = {"errors": {}}

        self.__set_page_urls()

        if data:
            # Handle the case when the search returns no book.
            self.__context["books"] = []

    def __set_page_urls(self) -> None:
        self.__context["previous_page_url"] = self.__build_url(
            {**self.__data, "page": self.__previous_page_number()}
        )
        # FIXME How to know if there are more results?!
        self.__context["next_page_url"] = self.__build_url(
            {**self.__data, "page": self.__next_page_number()}
        )

    def __build_url(self, params: dict[str, str]) -> str:
        if params.get("page", "0") == "0":
            return ""
        return url_for("books.search") + "?" + self.__join_params(params)

    def __join_params(self, params: dict[str, str]) -> str:
        return "&".join([f"{k}={v}" for k, v in params.items() if v])

    def __next_page_number(self) -> str:
        n = int(self.__data.get("page", "1"))
        return f"{n + 1}"

    def __previous_page_number(self) -> str:
        if n := int(self.__data.get("page", "0")):
            return f"{n - 1}"
        return ""

    def render(self, **context: Any) -> str:
        return super().render(**self.__context, **context, data=self.__data)

    def bad_request(self, errors: search_books.Errors) -> None:
        self.set_status_code(HTTP.OK)
        self.__context["errors"] = {
            "isbn": self.translate_error(errors.isbn),
            "title": self.translate_error(errors.title),
            "year": self.translate_error(errors.year),
            "author": self.translate_error(errors.author),
            "genre": self.translate_error(errors.genre),
        }

    def book(self, book: Book) -> None:
        if "books" not in self.__context:
            self.__context["books"] = []
        self.__context["books"].append(
            {
                "isbn": str(book.isbn),
                "title": str(book.title),
                "year": int(book.year),
                "authors": [str(a) for a in book.authors],
                "genres": [str(g) for g in book.genres],
                "cover": str(book.cover) if book.cover else "",
            }
        )


class AddBook(JinjaPresenter, add_book.Presenter):
    def __init__(
        self,
        data: MultiDict[str, Any],
        /,
        *,
        notify: Callable[[str, str], None] = lambda m, t: None,
        user: Optional[User] = None,
    ) -> None:
        super().__init__("books/add", user=user)
        self.set_status_code(HTTP.OK)
        self.__data = data
        self.__notify = notify
        self.__context: dict[str, Any] = {"errors": {}}

    def render(self, **context: Any) -> str:
        return super().render(**self.__context, **context, data=self.__data)

    def bad_request(self, errors: add_book.Errors) -> None:
        self.__context["errors"] = {
            "isbn": self.translate_error(errors.isbn),
            "title": self.translate_error(errors.title),
            "year": self.translate_error(errors.year),
            "authors": self.translate_error(errors.authors),
        }

    def book_already_exists(self, book: Book) -> None:
        self.__notify(self._("book-already-exists"), "info")
        self.redirect(url_for("books.display", isbn=str(book.isbn)))

    def book_added(self, book: Book) -> None:
        self.__notify(
            self._(
                "book-added-html",
                isbn=str(book.isbn),
                url=url_for("books.display", isbn=str(book.isbn)),
            ),
            "success",
        )
        self.redirect(url_for("books.add"))


class LookUpBook(JinjaPresenter, look_up_book.Presenter):
    def __init__(self, /, *, user: Optional[User] = None) -> None:
        super().__init__("books/add", fragment="form", user=user)
        self.__data: dict[str, Any] = {}
        self.__context: dict[str, Any] = {"errors": {}}

    def render(self, **context: Any) -> str:
        return super().render(**self.__context, **context, data=self.__data)

    def not_an_isbn(self, isbn: str) -> None:
        self.__data["isbn"] = isbn
        self.__context["errors"] = {"isbn": self._("not-an-isbn")}

    def unknown_error(self, message: str) -> None:
        logging.error(f"LookUpBook: {message}")
        self.__context["errors"] = {"isbn": self._("unknown-error")}

    def book_not_found(self, isbn: Isbn) -> None:
        self.__data["isbn"] = str(isbn)
        self.__context["errors"] = {"isbn": self._("unknown-isbn")}

    def book(self, book: Book) -> None:
        self.__data = {
            "isbn": str(book.isbn),
            "title": str(book.title),
            "year": int(book.year),
            "authors": ", ".join([str(a) for a in book.authors]),
            "genres": ", ".join([str(g) for g in book.genres]),
            "cover": str(book.cover),
        }


class DisplayBook(JinjaPresenter, display_book.Presenter):
    def __init__(
        self,
        /,
        *,
        notify: Callable[[str, str], None] = lambda m, t: None,
        user: Optional[User] = None,
    ) -> None:
        super().__init__("books/display", user=user)
        self.__context: dict[str, Any] = {"book": {}}
        self.__notify = notify

    def render(self, **context: Any) -> str:
        return super().render(**self.__context, **context)

    def not_an_isbn(self, isbn: str) -> None:
        self.__notify(self._("not-an-isbn"), "warning")
        self.redirect(url_for("books.search"))

    def book_not_found(self, isbn: Isbn) -> None:
        self.__notify(self._("book-does-not-exist"), "warning")
        self.redirect(url_for("books.search"))

    def see_other(self, isbn: Isbn) -> None:
        self.redirect(url_for("books.display", isbn=str(isbn)), HTTP.MOVED_PERMANENTLY)

    def book(self, book: Book) -> None:
        self.__context["book"] = {
            "added_on": self._("date", date=book.added_on.to_date()),
            "updated_on": (
                self._("date", date=book.updated_on.to_date())
                if book.updated_on != book.added_on
                else "-"
            ),
            "isbn": str(book.isbn),
            "title": str(book.title),
            "year": int(book.year),
            "authors": ", ".join([str(a) for a in book.authors]),
            "genres": ", ".join([str(g) for g in book.genres]),
            "cover": str(book.cover) if book.cover else "",
        }


class DisplayBookToUpdate(JinjaPresenter, display_book.Presenter):
    def __init__(
        self,
        isbn: str,
        /,
        *,
        notify: Callable[[str, str], None] = lambda m, t: None,
        user: Optional[User] = None,
    ) -> None:
        super().__init__("books/update", user=user)
        self.__context: dict[str, Any] = {"isbn": isbn, "data": {}, "errors": {}}
        self.__notify = notify

    def render(self, **context: Any) -> str:
        return super().render(**self.__context, **context)

    def not_an_isbn(self, isbn: str) -> None:
        self.__notify(self._("not-an-isbn"), "warning")
        self.redirect(url_for("books.search"))

    def book_not_found(self, isbn: Isbn) -> None:
        self.__notify(self._("book-does-not-exist"), "warning")
        self.redirect(url_for("books.search"))

    def see_other(self, isbn: Isbn) -> None:
        self.redirect(url_for("books.display", isbn=str(isbn)), HTTP.MOVED_PERMANENTLY)

    def book(self, book: Book) -> None:
        self.__context["data"] = {
            "isbn": str(book.isbn),
            "title": str(book.title),
            "year": int(book.year),
            "authors": ", ".join([str(a) for a in book.authors]),
            "genres": ", ".join([str(g) for g in book.genres]),
            "cover": str(book.cover) if book.cover else "",
        }


class UpdateBook(JinjaPresenter, update_book.Presenter):
    def __init__(
        self,
        isbn: str,
        data: MultiDict[str, Any],
        /,
        *,
        notify: Callable[[str, str], None] = lambda m, t: None,
        user: Optional[User] = None,
    ) -> None:
        super().__init__("books/update", user=user)
        self.set_status_code(HTTP.FORBIDDEN)
        self.__data = data
        self.__notify = notify
        self.__context: dict[str, Any] = {"isbn": isbn, "errors": {}}

    def render(self, **context: Any) -> str:
        return super().render(**self.__context, **context, data=self.__data)

    def bad_request(self, errors: update_book.Errors) -> None:
        self.set_status_code(HTTP.OK)
        self.__context["errors"] = {
            "title": self.translate_error(errors.title),
            "year": self.translate_error(errors.year),
            "authors": self.translate_error(errors.authors),
        }

    def book_not_found(self, isbn: Isbn) -> None:
        self.__notify(self._("book-not-found"), "warning")
        self.redirect(url_for("books.search"))

    def book_updated(self, book: Book) -> None:
        self.__notify(self._("update-book-success"), "success")
        self.redirect(url_for("books.display", isbn=str(book.isbn)))


class ValidateIsbn(JinjaPresenter):
    def __init__(
        self, data: MultiDict[str, Any], /, *, user: Optional[User] = None
    ) -> None:
        super().__init__("books/search", fragment="isbn", user=user)
        self.__data = data
        self.__errors = {}

        if isbn := data.get("isbn", ""):
            errors = add_book.Errors(isbn=validators.isbn(isbn))
            self.__errors["isbn"] = self.translate_error(errors.isbn)

    def render(self, **context: Any) -> str:
        return super().render(**context, data=self.__data, errors=self.__errors)
