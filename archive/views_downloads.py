from django.http import FileResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from .models import ToolInstance

def secure_download(request, instance_id, file_type):
    # ... (existing logic) ...
    
    log_action(
        user=request.user, 
        action='download', 
        resource_id=instance_id, 
        metadata={'file_type': file_type}
    )
    return FileResponse(file_handle, as_attachment=True)