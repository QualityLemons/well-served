import os
from pathlib import Path
import environ # Using django-environ

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent

# config/settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security & Auth Configuration
AUTH_USER_MODEL = 'accounts.User'

# Session & Cookie Security (Tactic 1 hardening)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not env.bool('DEBUG', default=False)
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'tools:catalog'
LOGOUT_REDIRECT_URL = 'accounts:login'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 10}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Our Apps
    'accounts',
    'tools',
    'archive',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'audit_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/audit.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'audit': {
            'handlers': ['audit_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

