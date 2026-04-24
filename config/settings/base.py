from pathlib import Path
import os

try:
    import environ  # type: ignore[import]
except ImportError:
    environ = None  # type: ignore[assignment]

# If your structure is: project/config/settings/base.py
# You need THREE .parent calls to get back to the project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

print(f"DEBUG: BASE_DIR is {BASE_DIR}")  # Add this for one run

if environ is not None:
    env = environ.Env()
    env.read_env()
else:
    env = os.environ

# Application definition
# config/settings/base.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.tools.apps.ToolsConfig',   # <--- MUST USE THE APPS CONFIG PATH
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# Auth & Security
AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT_URL = 'tools:catalog'
# ... other shared settings
