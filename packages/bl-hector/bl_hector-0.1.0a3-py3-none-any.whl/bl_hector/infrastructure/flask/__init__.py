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

from flask import Flask, g, get_flashed_messages, request, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

from bl_hector import __version__
from bl_hector.infrastructure.flask import services
from bl_hector.infrastructure.flask.aliases import blueprint as aliases
from bl_hector.infrastructure.flask.auth import blueprint as auth
from bl_hector.infrastructure.flask.books import blueprint as books
from bl_hector.infrastructure.settings import WsgiSettings
from bl_hector.interfaces import l10n


def build_app(settings: WsgiSettings) -> Flask:
    services.define_settings(settings)

    app = Flask(__name__)

    # FIXME make it configurable?!
    app.wsgi_app = ProxyFix(app.wsgi_app, x_host=1)  # type: ignore

    app.config.update(
        SECRET_KEY=settings.SECRET_KEY,
    )

    register_blueprints(app, settings)
    register_jinja_globals()

    app.teardown_appcontext(services.close_connection)

    @app.before_request
    def guess_locale() -> None:
        g.locale = (
            request.accept_languages.best_match(l10n.LOCALES) or l10n.DEFAULT_LOCALE
        )

    return app


def register_blueprints(app: Flask, settings: WsgiSettings) -> None:
    app.register_blueprint(aliases, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(books, url_prefix="/books")
    if settings.WEBAUTHN:
        from bl_hector.infrastructure.flask.webauthn import blueprint as webauthn

        app.register_blueprint(webauthn, url_prefix="/auth/webauthn")


def register_jinja_globals() -> None:
    from bl_hector.interfaces.to_http import as_html as presenters

    presenters.register_jinja_global("version", __version__)
    presenters.register_jinja_global("url_for", url_for)
    presenters.register_jinja_global("get_flashed_messages", get_flashed_messages)
