from django.http import FileResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from .models import ToolInstance

def secure_download(request, instance_id, file_type):
    record = get_object_or_404(ToolInstance, id=instance_id)
    
    # Tactic 7: The "Golden Rule" of retrieval
    if record.user != request.user:
        return HttpResponseForbidden("You do not have access to this file.")

    if file_type == 'md':
        file_handle = record.md_file.open()
    elif file_type == 'rtf':
        file_handle = record.rtf_file.open()
    else:
        return HttpResponseForbidden("Invalid file type.")

    return FileResponse(file_handle, as_attachment=True)