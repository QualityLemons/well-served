from django.urls import path

from .views import ArchiveDashboardView, ArchiveDetailView, waiting_list_signup
from .views_downloads import secure_download, secure_session_download

app_name = 'archive'

urlpatterns = [
    path('dashboard/', ArchiveDashboardView.as_view(), name='dashboard'),
    path('view/<int:pk>/', ArchiveDetailView.as_view(), name='detail'),
    path('download/<int:instance_id>/<str:file_type>/', secure_download, name='download'),
    path('session-download/<uuid:session_id>/<str:file_type>/', secure_session_download, name='session_download'),
]
