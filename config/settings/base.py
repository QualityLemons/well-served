from pathlib import Path
import environ

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ... your apps (accounts, tools, archive)
]

# ... (after env = environ.Env() and env.read_env())

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
