# Hector — a collection manager

## Install

For the time being, Hector cannot be installed from PyPI.
See [CONTRIBUTING.md]() to set up a development environment.


## Configure

Hector is configured using environment variables.
All the variable names are prefixed with `HECTOR_`.

```console
$ export HECTOR_SECRET_KEY="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
$ export HECTOR_DSN="sqlite:///data.sqlite"
```

The secret can be generated using the `token_hex()` function from
the Python's `secrets` module.

Additional Python database drivers might be required depending on the DSN.

See [the `settings` module](bl_hector/infrastructure/settings.py) for
a comprehensive list of configuration variables.


## Authentication

To enable WebAuthn authentication, you must install extra dependencies (`bl-hector[webauthn]`)
and enable it explicitly:

```console
$ export HECTOR_WEBAUTHN=1
```


## Initialise

Once configured, you must initialise Hector's database with the dedicated command:

```console
$ hector init-db
```


## Run

Hector being a Flask application, it can be run using any WSGI server,
for instance, with [Gunicorn](https://gunicorn.org):

```console
$ gunicorn --access-logfile="-" -w 4 -b 127.0.0.1:3000 "bl_hector.configuration.wsgi:app()"
```
