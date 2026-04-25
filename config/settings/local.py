from .base import *
import os
import dj_database_url

# 1. SECURITY & DEBUG
# We use 'True' as a string check for environment variables
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# On Railway, you need '*' to accept their generated domain. 
# Locally, 'localhost' is already covered by this.
ALLOWED_HOSTS = ['*']

# 2. DATABASE CONFIGURATION
# This is the "Smart Connector":
# - If on Railway: It uses the DATABASE_URL (Postgres).
# - If on your laptop: It defaults to the SQLite file.
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f"sqlite:///{BASE_DIR}/db.sqlite3"),
        conn_max_age=600
    )
}

# 3. APP EXTENSIONS
# Keeping your logic for adding local-only apps
INSTALLED_APPS += [
    # 'debug_toolbar', 
]

# 4. STATIC FILES (Required for Railway/Production)
# This ensures CSS/Images don't break when you deploy
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')