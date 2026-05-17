# App namespace: 'archive'
# Named URLs exposed by this module:
#   archive:dashboard        — paginated list of solo submissions and sessions
#   archive:detail           — single ToolInstance detail page
#   archive:delete           — POST-only deletion endpoint for a ToolInstance
#   archive:download         — per-instance file download (md, rtf, html)
#   archive:session_download — combined session export download (md, rtf)
from django.urls import path

from .views import ArchiveDashboardView, ArchiveDetailView, archive_record_delete
from .views_downloads import secure_download, secure_session_download

app_name = 'archive'

urlpatterns = [
    path('dashboard/', ArchiveDashboardView.as_view(), name='dashboard'),
    path('detail/<int:pk>/', ArchiveDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', archive_record_delete, name='delete'),
    path('download/<int:instance_id>/<str:file_type>/', secure_download, name='download'),
    path('session-download/<uuid:session_id>/<str:file_type>/', secure_session_download, name='session_download'),
]
