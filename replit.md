# Well-Served

Milestone Project 3 for a Level 5 Diploma in Web Software Engineering. A Django project intended to facilitate constructive dialogue and feedback for organisations.

## Stack

- Python 3.12 (Replit module)
- Django 5
- SQLite (development) via `db.sqlite3`
- Whitenoise for static files
- Gunicorn for production

## Project Layout

- `manage.py` — Django entry point. Uses `config.settings.local` by default.
- `config/` — Django project package.
  - `config/settings/base.py` — shared Django settings.
  - `config/settings/local.py` — local/dev settings (`DEBUG=True`, `ALLOWED_HOSTS=['*']`).
  - `config/settings/production.py` — production settings (legacy, not used by the workflow).
  - `config/urls.py` — root URL configuration. Currently exposes `/` (placeholder home) and `/admin/`.
  - `config/wsgi.py` — WSGI entry point.
- `accounts/`, `tools/`, `archive/`, `apps/`, `exporters/`, `library/` — partially-implemented domain modules from the original GitHub import. They contain skeleton code that is **not** wired into `INSTALLED_APPS` yet because several files are incomplete (missing imports, empty `__init__.py`, duplicate definitions). These can be enabled progressively as the implementation is finished.
- `templates/`, `static/` — Django templates and static assets shared across apps.

## Replit Setup

- Workflow `Start application` runs `python manage.py runserver 0.0.0.0:5000` on port 5000 (webview).
- `ALLOWED_HOSTS = ['*']` and `CSRF_TRUSTED_ORIGINS` cover the Replit proxied iframe.
- SQLite database file `db.sqlite3` lives at the project root.

## Common Commands

- Apply migrations: `python manage.py migrate`
- Create a superuser: `python manage.py createsuperuser`
- Collect static files: `python manage.py collectstatic --noinput`

## Deployment

Configured for Autoscale via `gunicorn`:

```
gunicorn --bind=0.0.0.0:5000 --reuse-port config.wsgi:application
```

Migrations are run as part of the deployment build step.

## Notes / Known Issues

The original codebase contains many in-progress files with broken imports (for example `tools/views.py` references `transaction`, `timezone`, `messages` and `ValidationError` without importing them; `archive/views.py` calls `order_name` instead of `order_by`; both `config/settings.py` and `config/settings/` exist). These were left untouched so the original work is preserved; only the minimum required to boot Django was added.
