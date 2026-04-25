import os
from django.core.wsgi import get_wsgi_application  # type: ignore

# Ensure this matches your settings directory structure
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

application = get_wsgi_application()