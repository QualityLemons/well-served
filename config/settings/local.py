from .base import *

# This overrides whatever is in the .env file 
# to ensure your local dev experience is smooth.
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

# Use SQLite locally to avoid needing Docker/Postgres immediately
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}