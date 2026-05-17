"""Production settings for the KwaCart Django application.

Inherits all defaults from ``config.settings.base`` and overrides values
that must differ in the live environment:
- ``DEBUG`` is forced to ``False``.
- ``SECRET_KEY``, ``ALLOWED_HOSTS``, and ``CSRF_TRUSTED_ORIGINS`` are read
  from environment variables so they can be rotated without a code deploy.
- HTTPS redirect is deliberately disabled because Replit's proxy terminates
  SSL before requests reach Gunicorn; the connection is already secure.
"""
import os
from .base import *  # noqa: F401,F403,F405

DEBUG = False

# In production SECRET_KEY must be set via the environment — an empty key will
# cause Django to raise ImproperlyConfigured on the first request.
SECRET_KEY = os.environ.get('SECRET_KEY', '')

# ALLOWED_HOSTS is read from a comma-separated environment variable so it can
# be updated without a code deploy.
_allowed = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [h.strip() for h in _allowed.split(',') if h.strip()]

# CSRF_TRUSTED_ORIGINS is similarly env-driven; required when Django runs
# behind a proxy and requests arrive via a non-standard port or HTTPS scheme.
_csrf = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf.split(',') if o.strip()]

# Replit terminates SSL at its proxy layer, so we must NOT redirect to HTTPS
# ourselves (it causes redirect loops). Tell Django to trust the forwarded header.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# If a DATABASE_URL environment variable is present, switch from the SQLite
# default (defined in base.py) to that database.  conn_max_age=600 enables
# persistent connections, reducing per-request connection overhead.
# When DATABASE_URL is absent the base.py SQLite setting is used unchanged,
# so the application still starts correctly without the variable.
import dj_database_url as _dj_db_url  # noqa: E402
_db_url = os.environ.get('DATABASE_URL')
if _db_url:
    DATABASES = {'default': _dj_db_url.config(default=_db_url, conn_max_age=600)}  # noqa: F405

# CompressedManifestStaticFilesStorage appends a content hash to each filename
# for long-lived cache headers and serves pre-compressed .gz versions when
# the client signals Accept-Encoding: gzip.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# W008: Replit's proxy handles SSL termination; redirect at app level would loop
SILENCED_SYSTEM_CHECKS = ['security.W008']
