class ToolsConfig(AppConfig):
    default_auto_field = 'django.db.backends.BigAutoField'
    name = 'apps.tools'  # MUST match the folder path

    # apps/tools/apps.py
from django.apps import AppConfig

class ToolsConfig(AppConfig):
    default_auto_field = 'django.db.backends.BigAutoField'
    name = 'apps.tools'  # The actual Python path
    label = 'tools'       # The "ID" Django uses for the database

    from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.backends.BigAutoField'
    name = 'apps.accounts'  # <--- MUST HAVE THE 'apps.' PREFIX