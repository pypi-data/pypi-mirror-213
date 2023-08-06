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
from typing import Optional

import bl_seth


@dataclass(frozen=True)
class TotpSettings(bl_seth.Settings):
    SECRET: str
    """The secret key.
    It can be generated with `pyotp.random_base32()`.
    """


@dataclass(frozen=True)
class WebAuthnSettings(bl_seth.Settings):
    # Could have been done with a simple `WEBAUTHN: bool = False`,
    # but this way it's similar to TOTP configuration.
    ENABLED: bool = False
    """To enable WebAuthn authentication."""


@dataclass(frozen=True)
class WsgiSettings(bl_seth.Settings):
    SECRET_KEY: str
    """The secret key for Flask sessions.
    See: <https://flask.palletsprojects.com/en/2.3.x/quickstart/#sessions>."""

    DSN: str
    """The data source name to access the database.
    See: <https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls>."""

    PROXIED: bool = False
    """To let Flask know that it runs behind a proxy.
    See: <https://flask.palletsprojects.com/en/2.3.x/deploying/proxy_fix/>.
    """

    DEBUG_SQL: bool = False
    """To enable SqlAlchemy logging.
    See: <https://docs.sqlalchemy.org/en/20/core/engines.html#configuring-logging>."""

    # Authentication mechanisms

    TOTP: Optional[TotpSettings] = None
    """To configure time-based one-time password.
    Extra dependencies must be installed: `bl-hector[totp]`.
    """

    WEBAUTHN: Optional[WebAuthnSettings] = None
    """To enable WebAuthn authentication.
    Extra dependencies must be installed: `bl-hector[webauthn]`.
    """


@dataclass(frozen=True)
class CliSettings(bl_seth.Settings):
    DSN: str
    """The data source name to access the database.
    See: <https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls>."""

    DEBUG_SQL: bool = False
    """To enable SqlAlchemy logging.
    See: <https://docs.sqlalchemy.org/en/20/core/engines.html#configuring-logging>."""
