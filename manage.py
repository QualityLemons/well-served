# manage.py
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django not found.") from exc
    
    print("--- Attempting to execute command ---") # Add this line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    print("--- Entry point reached ---") # Add this line
    main()