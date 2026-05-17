"""View functions and class-based views for the tools application.

Covers three user journeys:
- **Public try-it** (``tool_try``) — unauthenticated preview for the two
  featured free tools (Min Specs and 15% Solutions).
- **Solo drafting** (``draft_editor``, ``autosave_endpoint``, ``submit_tool``)
  — an authenticated user works through a tool form, autosaving as they go,
  then submitting to produce an archived record and downloadable export files.
- **Collaborative session** (``session_create`` through ``guest_respond``) —
  a host opens a session, shares a link (and QR code) with participants, each
  person fills in the form, and the host closes the session to run the tool
  across all contributions simultaneously.
"""
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from archive.models import ToolInstance, ToolSession
from exporters.pipeline import run_export_pipeline, run_session_export_pipeline

from .registry import TOOL_CATALOG, get_tool_form_class, get_tool_instance
from .utils import extract_canvas_from_payload, get_tool_metadata, _normalize_meta


# Only these slugs are accepted by the anonymous /try/ page.
# All other tool slugs require the user to be logged in.
FREE_TOOL_SLUGS = {'min-specs', '15-percent-solutions'}


def tool_try(request, tool_slug):
    """Anonymous single-page try-it view for the two featured free tools."""
    if tool_slug not in FREE_TOOL_SLUGS:
        raise Http404

    tool_meta = get_tool_metadata(tool_slug)
    form_class = get_tool_form_class(tool_slug)
    result = None
    result_fields = []

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            try:
                tool = get_tool_instance(tool_slug, form.cleaned_data)
                if tool:
                    result = tool.execute()
                    phases = getattr(tool, 'PHASES', ())
                    # Filter out phases whose output is empty so the result
                    # section does not render blank headings.
                    result_fields = [
                        (label, result.get(field, ''))
                        for field, label in phases
                        if result.get(field, '').strip()
                    ]
            except Exception as exc:
                result = {'error': str(exc)}
    else:
        form = form_class()

    return render(request, 'tools/tool_try.html', {
        'tool_meta': tool_meta,
        'form': form,
        'result': result,
        'result_fields': result_fields,
        'tool_slug': tool_slug,
        'try_timer_seconds': tool_meta.get('try_timer_seconds', 0),
        'try_timer_label': tool_meta.get('try_timer_label', ''),
    })


@login_required
def tool_catalog(request):
    """Lists all available tools from the registry, grouped by category."""
    categories = {}
    for slug, info in TOOL_CATALOG.items():
        cat = info.get('category', 'General')
        categories.setdefault(cat, []).append(_normalize_meta(slug, info))

    return render(request, 'tools/catalog.html', {'categories': categories})


# --- Solo flow ---------------------------------------------------------------

@login_required
def draft_editor(request, tool_slug, instance_id=None):
    """Render the drafting interface for a given tool and persist drafts on POST.

    When ``instance_id`` is omitted a new draft is created on the first POST.
    When ``instance_id`` is provided the existing draft is loaded for editing.
    """
    tool_meta = get_tool_metadata(tool_slug)
    if not tool_meta:
        return redirect('tools:catalog')

    instance = None
    if instance_id:
        instance = get_object_or_404(
            ToolInstance, id=instance_id, user=request.user,
            status='draft', session__isnull=True,
        )

    form_class = get_tool_form_class(tool_slug)
    form = None

    if form_class is not None:
        if request.method == 'POST':
            form = form_class(request.POST)
            if form.is_valid():
                try:
                    tool_class = get_tool_instance(tool_slug)
                    if instance is None:
                        instance = ToolInstance.objects.create(
                            user=request.user,
                            tool_slug=tool_slug,
                            tool_version=getattr(tool_class, 'version', '1.0'),
                            status='draft',
                        )
                    instance.payload_input = extract_canvas_from_payload(
                        form.cleaned_data, tool_slug, request.user.id,
                    )
                    instance.save()
                    messages.success(request, 'Draft saved.')
                    return redirect('tools:draft_edit',
                                    tool_slug=tool_slug, instance_id=instance.id)
                except Exception:
                    messages.error(
                        request,
                        'Unable to save your draft — please try again.',
                    )
        else:
            initial = (instance.payload_input if instance else None) or {}
            form = form_class(initial=initial)

    return render(request, 'tools/draft_editor.html', {
        'tool_slug': tool_slug,
        'tool_meta': tool_meta,
        'instance': instance,
        'form': form,
    })


@login_required
@require_POST
def autosave_endpoint(request, tool_slug):
    """AJAX endpoint that persists in-progress draft input.

    If ``instance_id`` is present in the request body the draft already
    exists and is updated in place.  Otherwise a new draft is created and
    its ID is returned so the client can reference it on subsequent saves.
    """
    if tool_slug not in TOOL_CATALOG:
        return JsonResponse({'error': 'unknown tool'}, status=400)
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'invalid request body'}, status=400)
    instance_id = data.get('instance_id')
    form_data = data.get('form_data') or {}
    if not isinstance(form_data, dict):
        return JsonResponse({'error': 'form_data must be an object'}, status=400)

    if instance_id:
        instance = get_object_or_404(
            ToolInstance, id=instance_id, user=request.user, status='draft',
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
    """Run the tool's logic and transition the draft to an archived record.

    The ``session__isnull=True`` guard ensures this endpoint only handles solo
    submissions.  Session contributions are submitted by ``session_close``,
    not by this view.
    """
    instance = get_object_or_404(
        ToolInstance, id=instance_id, user=request.user,
        status='draft', session__isnull=True,
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


# --- Collaborative session flow ---------------------------------------------

@login_required
@require_POST
def session_create(request, tool_slug):
    """Create a new collaborative session for the given tool."""
    if tool_slug not in TOOL_CATALOG:
        return redirect('tools:catalog')

    tool_class = get_tool_instance(tool_slug)
    # getattr is used defensively; BaseTool subclasses always define version,
    # but the '1.0' fallback guards against any future class that omits it.
    session = ToolSession.objects.create(
        host=request.user,
        tool_slug=tool_slug,
        tool_version=getattr(tool_class, 'version', '1.0'),
    )
    messages.success(
        request, 'Session started. Share the link with participants.'
    )
    return redirect('tools:session_detail', session_id=session.id)


@login_required
def session_detail(request, session_id):
    """Render the session page (form while open, combined view when closed)."""
    session = get_object_or_404(ToolSession, id=session_id)
    tool_meta = get_tool_metadata(session.tool_slug)
    if not tool_meta:
        return redirect('tools:catalog')

    is_host = (session.host_id == request.user.id)

    if session.status == 'closed':
        instances = (
            ToolInstance.objects
            .filter(session=session)
            .select_related('user')
            .order_by('submitted_at')
        )
        return render(request, 'tools/session_closed.html', {
            'session': session,
            'tool_meta': tool_meta,
            'instances': instances,
            'is_host': is_host,
        })

    instance, _ = ToolInstance.objects.get_or_create(
        session=session,
        user=request.user,
        defaults={
            'tool_slug': session.tool_slug,
            'tool_version': session.tool_version,
            'status': 'draft',
        },
    )

    form_class = get_tool_form_class(session.tool_slug)
    form = None
    if form_class is not None:
        if request.method == 'POST':
            form = form_class(request.POST)
            if form.is_valid():
                try:
                    instance.payload_input = extract_canvas_from_payload(
                        form.cleaned_data, session.tool_slug, request.user.id,
                    )
                    instance.save()
                    messages.success(request, 'Your response was saved.')
                    return redirect('tools:session_detail', session_id=session.id)
                except Exception:
                    messages.error(
                        request,
                        'Unable to save your response — please try again.',
                    )
        else:
            form = form_class(initial=instance.payload_input or {})

    participants = (
        ToolInstance.objects
        .filter(session=session)
        .select_related('user')
        .order_by('created_at')
    )
    share_url = request.build_absolute_uri(
        reverse('tools:session_detail', args=[session.id])
    )
    guest_join_url = request.build_absolute_uri(
        reverse('tools:guest_join', args=[session.id, session.guest_token])
    )
    # timer_started_at and timer_paused_at are serialised as ISO strings for
    # the JavaScript timer widget, which computes elapsed time client-side
    # using these as reference points rather than relying on its own clock.
    timer_started_at = (
        session.timer_started_at.isoformat()
        if session.timer_started_at else None
    )
    timer_paused_at = (
        session.timer_paused_at.isoformat()
        if session.timer_paused_at else None
    )

    threshold = session.pause_reminder_threshold_sec
    # JS literal for the timer widget: null disables the reminder, integer enables it.
    pause_reminder_threshold_js = 'null' if threshold is None else threshold

    initial_responder_names = [
        p.user.email if p.user_id else (p.guest_name or 'Guest')
        for p in participants
        if p.payload_input
    ]

    return render(request, 'tools/session_open.html', {
        'session': session,
        'tool_meta': tool_meta,
        'instance': instance,
        'form': form,
        'is_host': is_host,
        'participants': participants,
        'share_url': share_url,
        'guest_join_url': guest_join_url,
        'timer_started_at': timer_started_at,
        'timer_paused_at': timer_paused_at,
        'pause_reminder_threshold_sec': threshold,
        'pause_reminder_threshold_js': pause_reminder_threshold_js,
        'initial_responder_names': initial_responder_names,
    })


@login_required
@require_POST
def session_close(request, session_id):
    """Host closes the session: lock everyone's contribution and run the tool."""
    session = get_object_or_404(ToolSession, id=session_id, host=request.user)
    if session.status == 'closed':
        return redirect('tools:session_detail', session_id=session.id)

    with transaction.atomic():
        session.status = 'closed'
        session.closed_at = timezone.now()
        session.save()

        for instance in ToolInstance.objects.filter(session=session, status='draft'):
            # Errors are captured per-instance so that a broken tool definition
            # for one participant does not abort the close and leave all other
            # contributions un-archived.
            try:
                tool = get_tool_instance(session.tool_slug, instance.payload_input)
                instance.payload_output = tool.execute() if tool else {}
            except ValidationError as e:
                instance.payload_output = {
                    'error': e.message_dict if hasattr(e, 'message_dict') else e.messages
                }
            except Exception as e:
                instance.payload_output = {'error': str(e)}
            instance.status = 'archived'
            instance.submitted_at = timezone.now()
            instance.save()

        try:
            run_session_export_pipeline(session)
        except Exception:
            messages.warning(
                request,
                'Session closed, but the combined export could not be generated.',
            )
            return redirect('tools:session_detail', session_id=session.id)

    messages.success(request, 'Session closed. Combined results are now visible.')
    return redirect('tools:session_detail', session_id=session.id)


def session_status(request, session_id):
    """Lightweight JSON endpoint for participant-list / status polling.

    Accessible to authenticated participants and to unauthenticated guests who
    hold a valid guest_instance_id in their browser session for this session.
    """
    session = get_object_or_404(ToolSession, id=session_id)

    if request.user.is_authenticated:
        is_participant = (
            session.host_id == request.user.id
            or ToolInstance.objects.filter(session=session, user=request.user).exists()
        )
        if not is_participant:
            return JsonResponse({'error': 'forbidden'}, status=403)
    else:
        guest_instance_id = request.session.get(f'guest_instance_{session_id}')
        if not guest_instance_id:
            return JsonResponse({'error': 'forbidden'}, status=403)
        if not ToolInstance.objects.filter(id=guest_instance_id, session=session).exists():
            return JsonResponse({'error': 'forbidden'}, status=403)

    participants = (
        ToolInstance.objects
        .filter(session=session)
        .select_related('user')
        .order_by('created_at')
    )
    timer_started_at = (
        session.timer_started_at.isoformat()
        if session.timer_started_at else None
    )
    tool_meta = get_tool_metadata(session.tool_slug) or {}
    return JsonResponse({
        'status': session.status,
        'server_now': timezone.now().isoformat(),
        'timer_started_at': timer_started_at,
        # timer_phases and timer_seconds are returned so that participants who
        # join mid-session (or poll after a page reload) can initialise their
        # timer widget without needing a full page reload.
        'timer_phases': tool_meta.get('phases') or None,
        'timer_seconds': tool_meta.get('timer_seconds') or 0,
        'participants': [
            {
                'display_name': p.user.email if p.user_id else (p.guest_name or 'Guest'),
                'is_host': p.user_id is not None and p.user_id == session.host_id,
                'has_response': bool(p.payload_input),
            }
            for p in participants
        ],
    })


# Timer control — host only, POST required.
# Host-only enforcement is done via get_object_or_404(host=request.user)
# so non-hosts receive a 404 rather than a 403.

@login_required
@require_POST
def timer_start(request, session_id):
    """Host records the timer start time on the server so all clients can sync."""
    session = get_object_or_404(ToolSession, id=session_id, host=request.user)
    if session.status != 'open':
        return JsonResponse({'error': 'session not open'}, status=400)
    session.timer_started_at = timezone.now()
    session.save(update_fields=['timer_started_at'])
    return JsonResponse({'timer_started_at': session.timer_started_at.isoformat()})


@login_required
@require_POST
def timer_reset(request, session_id):
    """Host clears the server-side timer start time so the timer can restart."""
    session = get_object_or_404(ToolSession, id=session_id, host=request.user)
    if session.status != 'open':
        return JsonResponse({'error': 'session not open'}, status=400)
    session.timer_started_at = None
    session.save(update_fields=['timer_started_at'])
    return JsonResponse({'timer_started_at': None})


@login_required
@require_POST
def session_set_pause_reminder(request, session_id):
    """Host updates the pause-reminder threshold for the session.

    This persists a session-level setting (separate from timer start/reset,
    which manage transient state).
    """
    session = get_object_or_404(ToolSession, id=session_id, host=request.user)
    if session.status != 'open':
        return JsonResponse({'error': 'session not open'}, status=400)
    raw = request.POST.get('pause_reminder_threshold_sec', '')
    if raw == '' or raw is None:
        session.pause_reminder_threshold_sec = None
    else:
        try:
            value = int(raw)
        except (TypeError, ValueError):
            return JsonResponse({'error': 'invalid value'}, status=400)
        if value < 0:
            return JsonResponse({'error': 'value must be >= 0'}, status=400)
        # Zero is treated the same as None (disables the reminder) because a
        # 0-second threshold is not a meaningful configuration.
        session.pause_reminder_threshold_sec = value if value > 0 else None
    session.save(update_fields=['pause_reminder_threshold_sec'])
    return JsonResponse({
        'pause_reminder_threshold_sec': session.pause_reminder_threshold_sec
    })


# --- Guest participant flow --------------------------------------------------
# These views allow unauthenticated participants to join a session via a QR
# code URL that embeds the session's guest_token.  The guest is identified for
# the duration of their visit by a key stored in the Django browser session.

def guest_join(request, session_id, guest_token):
    """Show a name-entry form so unauthenticated users can join as guests.

    On POST a ToolInstance is created with user=None and the supplied name, and
    the instance ID is stored in the browser session so subsequent requests can
    identify the guest without requiring authentication.
    """
    session = get_object_or_404(ToolSession, id=session_id, guest_token=guest_token)

    if session.status == 'closed':
        return redirect('tools:guest_respond', session_id=session_id, guest_token=guest_token)

    # If this browser already joined, skip straight to the form.
    existing_id = request.session.get(f'guest_instance_{session_id}')
    if existing_id and ToolInstance.objects.filter(id=existing_id, session=session).exists():
        return redirect('tools:guest_respond', session_id=session_id, guest_token=guest_token)

    error = None
    if request.method == 'POST':
        name = request.POST.get('guest_name', '').strip()
        if not name:
            error = 'Please enter a name so the host can see who you are.'
        elif len(name) > 200:
            error = 'Name must be 200 characters or fewer.'
        else:
            tool_class = get_tool_instance(session.tool_slug)
            instance = ToolInstance.objects.create(
                user=None,
                guest_name=name,
                session=session,
                tool_slug=session.tool_slug,
                tool_version=getattr(tool_class, 'version', session.tool_version),
                status='draft',
            )
            request.session[f'guest_instance_{session_id}'] = instance.id
            return redirect('tools:guest_respond', session_id=session_id, guest_token=guest_token)

    tool_meta = get_tool_metadata(session.tool_slug)
    return render(request, 'tools/guest_join.html', {
        'session': session,
        'tool_meta': tool_meta,
        'error': error,
    })


def guest_respond(request, session_id, guest_token):
    """Show and save the tool form for a guest participant.

    The guest is identified via the browser session key set by guest_join.
    If the session has been closed this view renders the combined results.
    """
    session = get_object_or_404(ToolSession, id=session_id, guest_token=guest_token)
    tool_meta = get_tool_metadata(session.tool_slug)

    # Re-identify the guest via their browser session.
    instance_id = request.session.get(f'guest_instance_{session_id}')
    if not instance_id:
        return redirect('tools:guest_join', session_id=session_id, guest_token=guest_token)
    instance = get_object_or_404(ToolInstance, id=instance_id, session=session)

    if session.status == 'closed':
        instances = (
            ToolInstance.objects
            .filter(session=session)
            .select_related('user')
            .order_by('submitted_at')
        )
        return render(request, 'tools/guest_session_closed.html', {
            'session': session,
            'tool_meta': tool_meta,
            'instances': instances,
            'guest_instance': instance,
        })

    form_class = get_tool_form_class(session.tool_slug)
    form = None
    if form_class is not None:
        if request.method == 'POST':
            form = form_class(request.POST)
            if form.is_valid():
                try:
                    # Canvas extraction requires a user ID; skip it for guests.
                    cleaned = {
                        k: v for k, v in form.cleaned_data.items()
                        if k != 'canvas_data'
                    }
                    instance.payload_input = cleaned
                    instance.save()
                    messages.success(request, 'Your response was saved.')
                    return redirect('tools:guest_respond', session_id=session_id, guest_token=guest_token)
                except Exception:
                    messages.error(
                        request,
                        'Unable to save your response — please try again.',
                    )
        else:
            form = form_class(initial=instance.payload_input or {})

    timer_started_at = (
        session.timer_started_at.isoformat()
        if session.timer_started_at else None
    )
    timer_paused_at = (
        session.timer_paused_at.isoformat()
        if session.timer_paused_at else None
    )
    threshold = session.pause_reminder_threshold_sec
    pause_reminder_threshold_js = 'null' if threshold is None else threshold

    return render(request, 'tools/guest_respond.html', {
        'session': session,
        'tool_meta': tool_meta,
        'instance': instance,
        'form': form,
        'guest_token': guest_token,
        'timer_started_at': timer_started_at,
        'timer_paused_at': timer_paused_at,
        'pause_reminder_threshold_sec': threshold,
        'pause_reminder_threshold_js': pause_reminder_threshold_js,
    })


def timer_test_page(request):
    """
    Render a bare timer widget for browser-based accessibility testing.
    Only available when DEBUG is True.
    """
    if not settings.DEBUG:
        raise Http404
    from types import SimpleNamespace
    phases = [
        {"label": "Alpha", "seconds": 3},
        {"label": "Beta", "seconds": 3},
        {"label": "Gamma", "seconds": 3},
    ]
    # The SimpleNamespace must carry phases, timer_seconds, and title to match
    # what the _timer.html template expects from the tool_meta object.
    tool_meta = SimpleNamespace(phases=phases, timer_seconds=9, title="Test Timer")
    return render(request, "tools/timer_test_page.html", {"tool_meta": tool_meta, "timer_session_id": None})
