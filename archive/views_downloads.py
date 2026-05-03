from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404

from accounts.utils import log_action

from .models import ToolInstance, ToolSession


# Whitelist of supported file extensions.  Checked before calling
# getattr(instance, f'{file_type}_file') to prevent arbitrary attribute
# access on the model via a crafted URL parameter.
VALID_FILE_TYPES = {'md', 'rtf', 'html'}


@login_required
def secure_download(request, instance_id, file_type):
    """Serve a file associated with a ToolInstance.

    Enforces that the requesting user owns the instance before the file is
    served; non-owners receive a 404 rather than a 403 to avoid leaking
    whether the instance exists.
    """
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


@login_required
def secure_session_download(request, session_id, file_type):
    """Combined session export download. Allowed for host or participants.

    The Q() filter ensures that only the session host or any user who has a
    ToolInstance in the session (i.e. any participant) can download the
    combined export file.  Non-participants receive a 404.
    """
    if file_type not in VALID_FILE_TYPES:
        raise Http404('Unknown file type.')

    session = get_object_or_404(
        ToolSession.objects.filter(
            # Host OR any participant (anyone with a ToolInstance in the session).
            Q(host=request.user) | Q(instances__user=request.user)
        ).distinct(),
        id=session_id,
    )

    file_field = getattr(session, f'{file_type}_file', None)
    if not file_field:
        raise Http404('File is not available.')

    log_action(
        user=request.user,
        action='download',
        resource_id=str(session_id),
        metadata={'file_type': file_type, 'session': True},
    )
    return FileResponse(file_field.open('rb'), as_attachment=True)
