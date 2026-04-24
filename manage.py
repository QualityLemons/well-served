# manage.py
def main():
    # Default to 'local' for safety
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
    # ... rest of file