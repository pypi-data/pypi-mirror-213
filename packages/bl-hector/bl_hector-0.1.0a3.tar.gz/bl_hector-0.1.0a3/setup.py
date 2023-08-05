# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bl_hector',
 'bl_hector.application',
 'bl_hector.application.use_cases',
 'bl_hector.configuration',
 'bl_hector.domain',
 'bl_hector.domain.administration',
 'bl_hector.domain.collection_management',
 'bl_hector.infrastructure',
 'bl_hector.infrastructure.flask',
 'bl_hector.infrastructure.flask.aliases',
 'bl_hector.infrastructure.flask.auth',
 'bl_hector.infrastructure.flask.books',
 'bl_hector.infrastructure.flask.webauthn',
 'bl_hector.infrastructure.isbnlib',
 'bl_hector.infrastructure.sqlalchemy',
 'bl_hector.infrastructure.typer',
 'bl_hector.interfaces',
 'bl_hector.interfaces.l10n',
 'bl_hector.interfaces.to_http',
 'bl_hector.interfaces.to_http.as_html',
 'bl_hector.interfaces.to_http.as_json',
 'bl_hector.interfaces.to_terminal']

package_data = \
{'': ['*'],
 'bl_hector.infrastructure.flask': ['static/*',
                                    'static/css/*',
                                    'static/img/placeholders/*',
                                    'static/js/*',
                                    'static/webfonts/*'],
 'bl_hector.interfaces.l10n': ['en-GB/*', 'fr-FR/*'],
 'bl_hector.interfaces.to_http.as_html': ['templates/*',
                                          'templates/auth/*',
                                          'templates/books/*',
                                          'templates/books/mixins/*',
                                          'templates/mixins/*',
                                          'templates/webauthn/*']}

install_requires = \
['Flask>=2.3.2,<3.0.0',
 'SQLAlchemy>=2.0.15,<3.0.0',
 'bl-seth>=0.1.2,<0.2.0',
 'bl3d>=0.3.0,<0.4.0',
 'fluent.runtime>=0.4.0,<0.5.0',
 'isbnlib>=3.10.14,<4.0.0',
 'jinja2-fragments>=0.3.0,<0.4.0',
 'pypugjs>=5.9.12,<6.0.0',
 'typer>=0.9.0,<0.10.0']

extras_require = \
{'webauthn': ['webauthn>=1.8.1,<2.0.0']}

entry_points = \
{'console_scripts': ['hector = bl_hector.configuration.cli:cli']}

setup_kwargs = {
    'name': 'bl-hector',
    'version': '0.1.0a3',
    'description': 'A collection manager.',
    'long_description': '# Hector — a collection manager\n\n## Install\n\nFor the time being, Hector cannot be installed from PyPI.\nSee [CONTRIBUTING.md]() to set up a development environment.\n\n\n## Configure\n\nHector is configured using environment variables.\nAll the variable names are prefixed with `HECTOR_`.\n\n```console\n$ export HECTOR_SECRET_KEY="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"\n$ export HECTOR_DSN="sqlite:///data.sqlite"\n```\n\nThe secret can be generated using the `token_hex()` function from\nthe Python\'s `secrets` module.\n\nAdditional Python database drivers might be required depending on the DSN.\n\nSee [the `settings` module](bl_hector/infrastructure/settings.py) for\na comprehensive list of configuration variables.\n\n\n## Authentication\n\nTo enable WebAuthn authentication, you must install extra dependencies (`bl-hector[webauthn]`)\nand enable it explicitly:\n\n```console\n$ export HECTOR_WEBAUTHN=1\n```\n\n\n## Initialise\n\nOnce configured, you must initialise Hector\'s database with the dedicated command:\n\n```console\n$ hector init-db\n```\n\n\n## Run\n\nHector being a Flask application, it can be run using any WSGI server,\nfor instance, with [Gunicorn](https://gunicorn.org):\n\n```console\n$ gunicorn --access-logfile="-" -w 4 -b 127.0.0.1:3000 "bl_hector.configuration.wsgi:app()"\n```\n',
    'author': 'Tanguy Le Carrour',
    'author_email': 'tanguy@bioneland.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
