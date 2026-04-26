from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path


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
    path('waiting-list/', include('archive.urls_waitinglist')),
    path('request-a-feature/', include('archive.urls_feature_request')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
