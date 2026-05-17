"""Root URL configuration for the KwaCart project.

Mounts four application routers under their respective prefixes and
defines two lightweight inline views (``home`` and ``about``) that render
static marketing pages without requiring a dedicated views module.

URL map
-------
``/``                   → landing page (home)
``/about/``             → about page
``/admin/``             → Django admin
``/accounts/``          → accounts app (login, logout, sign-up)
``/tools/``             → tools app (catalog, draft, session, guest flows)
``/archive/``           → archive app (dashboard, detail, downloads)
``/waiting-list/``      → waiting-list sign-up page
``/request-a-feature/`` → feature-request submission page
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path


# home and about are simple template-only views.  Defining them inline here
# avoids creating a dedicated views.py just for two trivial render() calls.
def home(request):
    return render(request, 'landing.html')


def about(request):
    return render(request, 'about.html')


urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('tools/', include('tools.urls')),
    path('archive/', include('archive.urls')),
    path('waiting-list/', include('archive.urls_waiting_list')),
    path('request-a-feature/', include('archive.urls_feature_request')),
    # static() returns [] in production (WhiteNoise serves files instead).
    # In development it adds a URL pattern so the dev server can serve uploads.
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
