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

from dataclasses import dataclass
from typing import Any, Optional

from bl_hector.domain.administration.enumerations import Permissions
from bl_hector.domain.collection_management import errors
from bl_hector.interfaces.l10n import Translator


@dataclass
class User:
    id: str
    locale: str
    permissions: list[Permissions]

    def __getattribute__(self, name: str) -> Any:
        PREFIX = "can_"
        if name.startswith(PREFIX):
            return self.has_permission(name[len(PREFIX) :].upper())
        return super().__getattribute__(name)

    def has_permission(self, permission: str) -> bool:
        if not self.id:
            return False
        try:
            return Permissions[permission] in self.permissions
        except KeyError:
            return False


def translate_error(
    translator: Translator, error: Optional[errors.IncorrectValue] = None
) -> str:
    if not error:
        return ""

    # Dispatching errors based on class is not very LSP!?
    if isinstance(error, errors.IncorrectValue):
        return translator("incorrect-value")
    return translator("unknown-error")
