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

from typing import Any

from flask import Blueprint, current_app, session, url_for

from bl_hector.infrastructure.flask import services
from bl_hector.infrastructure.flask.utils import presenter_to_response
from bl_hector.interfaces.to_http import Redirection, as_html

blueprint = Blueprint("auth", __name__)


@blueprint.get("")
@presenter_to_response
def root() -> Any:
    return Redirection(url_for("books.search"))


@blueprint.get("/login")
@presenter_to_response
def login() -> Any:
    auth_links = current_app.auth_links  # type: ignore[attr-defined]
    if not auth_links:
        return Redirection(url_for("aliases.root"))
    if len(auth_links) == 1:
        return Redirection(url_for(auth_links[0]["route"]))
    return as_html.JinjaPresenter(
        "auth/login", links=auth_links, user=services.get_user()
    )


@blueprint.get("/logout")
@presenter_to_response
def logout() -> Any:
    session.clear()
    return Redirection(url_for("aliases.root"))
