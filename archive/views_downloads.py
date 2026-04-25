from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404

from accounts.utils import log_action

from .models import ToolInstance


VALID_FILE_TYPES = {'md', 'rtf', 'html'}


@login_required
def secure_download(request, instance_id, file_type):
    if file_type not in VALID_FILE_TYPES:
        raise Http404('Unknown file type.')

    instance = get_object_or_404(ToolInstance, id=instance_id, user=request.user)
    file_field = getattr(instance, f'{file_type}_file', None)
    if not file_field:
        raise Http404('File is not available.')

    log_action(
        user=request.user,
        action='download',
        resource_id=instance_id,
        metadata={'file_type': file_type},
    )
    return FileResponse(file_field.open('rb'), as_attachment=True)
