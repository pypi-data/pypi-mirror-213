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
from typing import Any

from bl_hector.domain.administration.enumerations import Permissions


@dataclass
class User:
    id: str
    locale: str

    def __getattribute__(self, name: str) -> Any:
        PREFIX = "can_"
        if name.startswith(PREFIX):
            return self.has_permission(name[len(PREFIX) :].upper())
        return super().__getattribute__(name)

    def has_permission(self, permission: str) -> bool:
        if not self.id:
            return False
        try:
            Permissions[permission]
        except KeyError:
            return False
        return True
