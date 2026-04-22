from pyexpat.errors import messages

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json

from .registry import get_tool_instance
from archive.models import ToolInstance

@login_required
def draft_editor(request, tool_slug, instance_id=None):
    """
    Standard GET view to render the drafting interface.
    """
    # Fetch existing draft or provide a blank state
    instance = None
    if instance_id:
        instance = get_object_or_404(ToolInstance, id=instance_id, user=request.user, status='draft')
    
    context = {
        'tool_slug': tool_slug,
        'instance': instance,
        # In a real app, we'd pull the tool's form fields from the registry here
    }
    return render(request, 'tools/draft_editor.html', context)

@login_required
@require_POST
def autosave_endpoint(request, tool_slug):
    """
    AJAX endpoint for Tactic 4 (Autosave).
    Expects JSON data: { "instance_id": 1, "form_data": {...} }
    """
    data = json.loads(request.body)
    instance_id = data.get('instance_id')
    form_data = data.get('form_data')

    # 1. Get or Create the Draft
    if instance_id:
        instance = get_object_or_404(ToolInstance, id=instance_id, user=request.user, status='draft')
    else:
        # Tactic 3: Get version from the tool logic
        tool_class = get_tool_instance(tool_slug)
        instance = ToolInstance.objects.create(
            user=request.user,
            tool_slug=tool_slug,
            tool_version=tool_class.version,
            status='draft'
        )

    # 2. Update the Draft Data (Tactic 2)
    instance.payload_input = form_data
    instance.save()

    return JsonResponse({
        'status': 'success',
        'instance_id': instance.id,
        'last_saved': instance.updated_at.strftime("%H:%M:%S")
    })

@login_required
@require_POST
def submit_tool(request, instance_id):
    """
    Tactic 5: Transactions Draft -> Archived.
    Triggers Tool Logic and locks the record.
    """
    # 1. Fetch the draft and ensure ownership
    instance = get_object_or_404(
        ToolInstance, 
        id=instance_id, 
        user=request.user, 
        status='draft'
    )

    try:
        with transaction.atomic():
            # 2. Instantiate the Tool via Registry (Tactic 3)
            # We pass the saved payload_input to the tool
            tool_class = get_tool_instance(instance.tool_slug, instance.payload_input)
            
            if not tool_class:
                raise Exception("Tool definition not found in registry.")

            # 3. Execute Tool Pipeline (Validation -> Processing)
            # This populates the structured results
            result_data = tool_class.execute()

            # 4. Update the Instance (Tactic 5)
            instance.payload_output = result_data
            instance.status = 'archived'
            instance.submitted_at = timezone.now()
            
            # Note: We save here so the Output Gen has access to the final data
            instance.save()

            # 5. Trigger Output Generation (Hook for Tactic 6)
            # We will build these functions next.
            # generate_outputs(instance) 

        messages.success(request, "Tool execution successful. Record archived.")
        return redirect('archive:detail', instance_id=instance.id)

    except ValidationError as e:
        # Handle tool-specific validation errors (e.g., text too short)
        messages.error(request, f"Validation Error: {e.message}")
        return redirect('tools:draft_edit', tool_slug=instance.tool_slug, instance_id=instance.id)
    
    except Exception as e:
        # General safety net (Tactic 8)
        messages.error(request, f"System Error: {str(e)}")
        return redirect('tools:draft_edit', tool_slug=instance.tool_slug, instance_id=instance.id)
    
    
