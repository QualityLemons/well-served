import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from archive.models import ToolInstance
from exporters.pipeline import run_export_pipeline

from .registry import TOOL_CATALOG, get_tool_instance
from .utils import get_tool_metadata


@login_required
def tool_catalog(request):
    """Lists all available tools from the registry, grouped by category."""
    categories = {}
    for slug, info in TOOL_CATALOG.items():
        cat = info.get('category', 'General')
        info['slug'] = slug
        categories.setdefault(cat, []).append(info)

    return render(request, 'tools/catalog.html', {'categories': categories})


@login_required
def draft_editor(request, tool_slug, instance_id=None):
    """Render the drafting interface for a given tool."""
    tool_meta = get_tool_metadata(tool_slug)
    if not tool_meta:
        return redirect('tools:catalog')

    instance = None
    if instance_id:
        instance = get_object_or_404(
            ToolInstance, id=instance_id, user=request.user, status='draft'
        )

    return render(request, 'tools/draft_editor.html', {
        'tool_slug': tool_slug,
        'tool_meta': tool_meta,
        'instance': instance,
    })


@login_required
@require_POST
def autosave_endpoint(request, tool_slug):
    """AJAX endpoint that persists in-progress draft input."""
    data = json.loads(request.body or '{}')
    instance_id = data.get('instance_id')
    form_data = data.get('form_data') or {}

    if instance_id:
        instance = get_object_or_404(
            ToolInstance, id=instance_id, user=request.user, status='draft'
        )
    else:
        tool_class = get_tool_instance(tool_slug)
        instance = ToolInstance.objects.create(
            user=request.user,
            tool_slug=tool_slug,
            tool_version=getattr(tool_class, 'version', '1.0'),
            status='draft',
        )

    instance.payload_input = form_data
    instance.save()

    return JsonResponse({
        'status': 'success',
        'instance_id': instance.id,
        'last_saved': instance.updated_at.strftime('%H:%M:%S'),
    })


@login_required
@require_POST
def submit_tool(request, instance_id):
    """Run the tool's logic and transition the draft to an archived record."""
    instance = get_object_or_404(
        ToolInstance, id=instance_id, user=request.user, status='draft'
    )

    try:
        with transaction.atomic():
            tool_class = get_tool_instance(instance.tool_slug, instance.payload_input)
            if not tool_class:
                raise Exception('Tool definition not found in registry.')

            result_data = tool_class.execute()

            instance.payload_output = result_data
            instance.status = 'archived'
            instance.submitted_at = timezone.now()
            instance.save()

            run_export_pipeline(instance)

        messages.success(request, 'Tool execution successful. Files generated.')
        return redirect('archive:detail', pk=instance.id)

    except ValidationError as e:
        messages.error(request, f'Validation Error: {e.message}')
        return redirect('tools:draft_edit', tool_slug=instance.tool_slug,
                        instance_id=instance.id)
    except Exception as e:
        messages.error(request, f'System Error: {str(e)}')
        return redirect('tools:draft_edit', tool_slug=instance.tool_slug,
                        instance_id=instance.id)
