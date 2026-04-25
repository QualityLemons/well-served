import os
import dj_database_url
# This pulls in the core settings (like Middleware, Templates, etc.)
from .base import * # --- 1. SECURITY & DEBUG ---
# On Railway/Local, we keep DEBUG True during development
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# '*' allows the app to run on any Railway domain without 400 errors
ALLOWED_HOSTS = ['*']

# --- 2. DATABASE CONFIGURATION ---
# This looks for Railway's Postgres; if not found, it uses your local SQLite file
DEFAULT_DB = f"sqlite:///{BASE_DIR}/db.sqlite3"
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', DEFAULT_DB),
        conn_max_age=600
    )
}

# --- 3. APP EXTENSIONS ---
# Use += to add local-only apps to the list defined in base.py
INSTALLED_APPS += [
    # 'debug_toolbar', 
]

# --- 4. STATIC FILES ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')