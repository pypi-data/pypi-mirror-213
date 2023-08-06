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

from bl_hector.domain.administration.enumerations import Permissions as P
from bl_hector.domain.administration.repositories import Permissions
from bl_hector.domain.administration.value_objects import UserId

ONLY_USER = "admin"


class DummyPermissions(Permissions):
    def for_user(self, user_id: UserId) -> list[P]:
        return [p for p in P]

    def is_authorized_to(self, user_id: UserId, permission: P) -> bool:
        return bool(str(user_id))
