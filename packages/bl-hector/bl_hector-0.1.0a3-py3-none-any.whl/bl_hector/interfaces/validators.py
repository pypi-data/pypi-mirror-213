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

from typing import Any, Callable, Protocol

from werkzeug.datastructures import MultiDict

from bl_hector.domain.collection_management.exceptions import IncorrectValue
from bl_hector.domain.collection_management.value_objects import (
    Author,
    Genre,
    Isbn,
    Title,
    Year,
)
from bl_hector.interfaces.l10n import DummyTranslator, Translator


class ValidationResult:
    name: str

    def __init__(self, name: str, error: str = "", **variables: Any) -> None:
        self.name = name
        self.__error = error
        self.__variables = variables

    def __bool__(self) -> bool:
        return not self.__error

    def error(self, translator: Translator = DummyTranslator()) -> str:
        return translator(self.__error, **self.__variables)


class Validator(Protocol):
    def __call__(self, name: str, value: str) -> ValidationResult:
        ...


def mandatory(validator: Validator) -> Validator:
    def wrapper(name: str, value: str) -> ValidationResult:
        if not value:
            return ValidationResult(name, "mandatory-value")
        return validator(name, value)

    return wrapper


def optional(validator: Validator) -> Validator:
    def wrapper(name: str, value: str) -> ValidationResult:
        if not value:
            return ValidationResult(name)
        return validator(name, value)

    return wrapper


def isbn(name: str, value: str) -> ValidationResult:
    try:
        Isbn.instanciate(value)
        return ValidationResult(name)
    except IncorrectValue:
        return ValidationResult(name, "incorrect-value")


def year(name: str, value: str) -> ValidationResult:
    try:
        Year.instanciate(int(value))
        return ValidationResult(name)
    except ValueError:
        return ValidationResult(name, "incorrect-value")
    except IncorrectValue:
        return ValidationResult(name, "incorrect-value")


def title(name: str, value: str) -> ValidationResult:
    try:
        Title.instanciate(value)
        return ValidationResult(name)
    except IncorrectValue:
        return ValidationResult(name, "incorrect-value")


def author(name: str, value: str) -> ValidationResult:
    try:
        Author.instanciate(value)
        return ValidationResult(name)
    except IncorrectValue:
        return ValidationResult(name, "incorrect-value")


def authors(name: str, value: str) -> ValidationResult:
    try:
        for d in [d.strip() for d in value.strip().strip(",").split(",")]:
            Author.instanciate(d)
        return ValidationResult(name)
    except IncorrectValue:
        return ValidationResult(name, "incorrect-value")


def genre(name: str, value: str) -> ValidationResult:
    try:
        Genre.instanciate(value)
        return ValidationResult(name)
    except IncorrectValue:
        return ValidationResult(name, "incorrect-value")


def genres(name: str, value: str) -> ValidationResult:
    try:
        for d in [d.strip() for d in value.strip().strip(",").split(",")]:
            Genre.instanciate(d)
        return ValidationResult(name)
    except IncorrectValue:
        return ValidationResult(name, "incorrect-value")


class DataValidator:
    VALIDATORS: list[tuple[str, Callable[[str, str], ValidationResult]]] = []

    def __init__(self, data: MultiDict[str, Any]) -> None:
        self.__results = []
        for attribute, validator in self.VALIDATORS:
            value = data.get(attribute, "")
            self.__results.append(validator(attribute, str(value)))

    @property
    def is_ok(self) -> bool:
        return all(self.__results)

    def get_errors(self, translator: Translator = DummyTranslator()) -> dict[str, str]:
        if self.is_ok:
            return {}
        return {r.name: r.error(translator) for r in self.__results}


class SearchBooks(DataValidator):
    VALIDATORS = [
        ("isbn", optional(isbn)),
        ("title", optional(title)),
        ("year", optional(year)),
        ("author", optional(author)),
        ("genre", optional(genre)),
    ]


class AddBook(DataValidator):
    VALIDATORS = [
        ("isbn", mandatory(isbn)),
        ("title", mandatory(title)),
        ("year", mandatory(year)),
        ("authors", mandatory(authors)),
        ("genres", optional(genres)),
    ]


class UpdateBook(DataValidator):
    VALIDATORS = [
        ("title", mandatory(title)),
        ("year", mandatory(year)),
        ("authors", mandatory(authors)),
        ("genres", optional(genres)),
    ]
