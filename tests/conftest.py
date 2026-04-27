"""
Pytest configuration for the test suite.

Provides a `timer_html` fixture that pre-renders the timer widget template as a
plain string.  Browser tests use page.set_content() to load it directly, so no
live Django server is required — the timer widget is fully client-side once it
has been rendered.

Also provides `archive_detail_html` and `session_closed_html` fixtures that
pre-render those full-page templates using lightweight mock context objects so
that the browser-based axe-core tests can load them without a running server.
"""

import os
from types import SimpleNamespace

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

# pytest-playwright uses an asyncio event loop for its session-scoped browser
# fixture.  Django 6.0 added a strict guard that raises SynchronousOnlyOperation
# whenever synchronous ORM operations (including connection.close() during test
# DB creation) are called from within an async context.  The env var below is
# the sanctioned override for test environments where this is harmless.
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

# ---------------------------------------------------------------------------
# Chromium / Playwright library path setup for Replit
# ---------------------------------------------------------------------------
# On Replit the Nix environment exposes REPLIT_LD_LIBRARY_PATH which already
# contains the Mesa (libgbm) library path required by Chromium.  We prepend
# it to LD_LIBRARY_PATH so the browser subprocess can find the shared
# libraries it needs.
#
# If REPLIT_LD_LIBRARY_PATH is not set (e.g. local development outside
# Replit) we fall back to the old heuristic of checking
# /home/runner/.nix-profile/lib.
_replit_lib = os.environ.get("REPLIT_LD_LIBRARY_PATH", "")
_nix_lib = "/home/runner/.nix-profile/lib"
_lib_path = _replit_lib or (_nix_lib if os.path.isdir(_nix_lib) else "")
if _lib_path:
    _existing = os.environ.get("LD_LIBRARY_PATH", "")
    if _lib_path not in _existing:
        os.environ["LD_LIBRARY_PATH"] = (
            f"{_lib_path}:{_existing}" if _existing else _lib_path
        )

import django
import pytest

django.setup()


TEST_PHASES = [
    {"label": "Alpha", "seconds": 3},
    {"label": "Beta", "seconds": 3},
    {"label": "Gamma", "seconds": 3},
]


@pytest.fixture(scope="session")
def timer_html() -> str:
    """
    Pre-render the timer widget template with three 3-second phases.
    Tests load this HTML via page.set_content() — no server required.
    """
    from django.template.loader import render_to_string

    tool_meta = SimpleNamespace(
        phases=TEST_PHASES,
        timer_seconds=9,
        title="Test Timer",
    )
    return render_to_string(
        "tools/timer_test_page.html",
        {"tool_meta": tool_meta, "timer_session_id": None},
    )


@pytest.fixture(scope="session")
def simple_timer_html() -> str:
    """
    Pre-render the timer widget template in simple (no-phases) mode with a
    60-second countdown.  Used by visibility re-sync tests.
    """
    from django.template.loader import render_to_string

    tool_meta = SimpleNamespace(
        phases=None,
        timer_seconds=60,
        title="Simple Timer",
    )
    return render_to_string(
        "tools/timer_test_page.html",
        {"tool_meta": tool_meta, "timer_session_id": None},
    )


# ---------------------------------------------------------------------------
# Session-mode fixtures (clock-skew tests)
# ---------------------------------------------------------------------------

# A fake session UUID used only for rendering URLs in the template.
# The value never hits the database; fetch() calls are intercepted by
# page.route() before they reach any network.
_TEST_SESSION_ID = "00000000-0000-0000-0000-000000000001"

# Base URL injected via a <base> tag so that the relative status-poll URL
# produced by {% url ... %} resolves to something page.route() can intercept.
_TEST_BASE = "http://testhost"


def _inject_base(html: str) -> str:
    """Insert a <base> tag so relative fetch URLs resolve to _TEST_BASE."""
    return html.replace("<head>", f'<head><base href="{_TEST_BASE}/">', 1)


@pytest.fixture(scope="session")
def host_timer_html() -> str:
    """
    Pre-render the phase timer widget with ``is_host=True``.

    Used by the long-pause host reminder tests to verify that the
    ``.timer-paused-badge.long-paused`` class and "Still paused — X min"
    text appear for host views after ``PAUSE_REMINDER_THRESHOLD_SEC`` (300 s)
    have elapsed since the pause.
    """
    from django.template.loader import render_to_string

    tool_meta = SimpleNamespace(
        phases=TEST_PHASES,
        timer_seconds=9,
        title="Host Timer",
    )
    return render_to_string(
        "tools/timer_test_page.html",
        {"tool_meta": tool_meta, "timer_session_id": None, "is_host": True},
    )


@pytest.fixture(scope="session")
def host_timer_html_threshold_120() -> str:
    """
    Pre-render the phase timer widget with ``is_host=True`` and a custom
    ``pause_reminder_threshold_js`` of 120 seconds.

    Used to verify that the ``long-paused`` class appears at 120 s rather
    than the default 300 s.
    """
    from django.template.loader import render_to_string

    tool_meta = SimpleNamespace(
        phases=TEST_PHASES,
        timer_seconds=9,
        title="Host Timer Threshold 120",
    )
    return render_to_string(
        "tools/timer_test_page.html",
        {
            "tool_meta": tool_meta,
            "timer_session_id": None,
            "is_host": True,
            "pause_reminder_threshold_js": "120",
        },
    )


@pytest.fixture(scope="session")
def host_timer_html_threshold_null() -> str:
    """
    Pre-render the phase timer widget with ``is_host=True`` and
    ``pause_reminder_threshold_js`` set to ``null`` (disabled).

    Used to verify that the ``long-paused`` class never appears when the
    reminder threshold is disabled, regardless of elapsed pause time.
    """
    from django.template.loader import render_to_string

    tool_meta = SimpleNamespace(
        phases=TEST_PHASES,
        timer_seconds=9,
        title="Host Timer Threshold Null",
    )
    return render_to_string(
        "tools/timer_test_page.html",
        {
            "tool_meta": tool_meta,
            "timer_session_id": None,
            "is_host": True,
            "pause_reminder_threshold_js": "null",
        },
    )


@pytest.fixture(scope="session")
def host_session_timer_html() -> str:
    """
    Pre-render the phase timer widget with ``is_host=True`` **and** a real
    fake session ID so that the ``{% elif is_host %}`` branch is taken and
    only the Start and Reset buttons are rendered (no Pause button).

    The ``timer_session_id=None`` path takes ``{% if not timer_session_id %}``
    and renders all three buttons (Start / Pause / Reset).  To get the
    host-only control set the session ID must be truthy.

    A ``<base href="http://testhost/">`` tag is injected so that the
    relative start/reset URLs resolve to absolute URLs that can be
    intercepted by ``page.route()`` in the tests.
    """
    from django.template.loader import render_to_string

    tool_meta = SimpleNamespace(
        phases=TEST_PHASES,
        timer_seconds=9,
        title="Host Session Timer",
    )
    html = render_to_string(
        "tools/timer_test_page.html",
        {
            "tool_meta": tool_meta,
            "timer_session_id": _TEST_SESSION_ID,
            "timer_started_at": None,
            "timer_paused_at": None,
            "is_host": True,
        },
    )
    return _inject_base(html)


@pytest.fixture(scope="session")
def session_phase_timer_html() -> str:
    """
    Phase timer (3 × 3 s) rendered in session mode with a fake session ID.
    The status-poll URL is intercepted by page.route() in the tests; no live
    server is required.
    """
    from django.template.loader import render_to_string

    tool_meta = SimpleNamespace(
        phases=TEST_PHASES,
        timer_seconds=9,
        title="Session Phase Timer",
    )
    html = render_to_string(
        "tools/timer_test_page.html",
        {
            "tool_meta": tool_meta,
            "timer_session_id": _TEST_SESSION_ID,
            "timer_started_at": None,
            "timer_paused_at": None,
        },
    )
    return _inject_base(html)


@pytest.fixture(scope="session")
def session_long_phase_timer_html() -> str:
    """
    Phase timer (3 × 120 s = 6 minutes per phase) rendered in session mode.

    Used by pause-resume cycle tests (task #91) where the fake-clock advances
    across multiple 4 s poll intervals.  The long phases ensure the timer
    never expires mid-test, avoiding spurious "Now in Beta" / "All phases
    complete" announcements that would break the observer count assertions.
    """
    from django.template.loader import render_to_string

    long_phases = [
        {"label": "Alpha", "seconds": 120},
        {"label": "Beta", "seconds": 120},
        {"label": "Gamma", "seconds": 120},
    ]
    tool_meta = SimpleNamespace(
        phases=long_phases,
        timer_seconds=360,
        title="Session Long Phase Timer",
    )
    html = render_to_string(
        "tools/timer_test_page.html",
        {
            "tool_meta": tool_meta,
            "timer_session_id": _TEST_SESSION_ID,
            "timer_started_at": None,
            "timer_paused_at": None,
        },
    )
    return _inject_base(html)


@pytest.fixture(scope="session")
def session_simple_timer_html() -> str:
    """
    Simple (no-phases) timer (60 s) rendered in session mode with a fake
    session ID.  The status-poll URL is intercepted by page.route().
    """
    from django.template.loader import render_to_string

    tool_meta = SimpleNamespace(
        phases=None,
        timer_seconds=60,
        title="Session Simple Timer",
    )
    html = render_to_string(
        "tools/timer_test_page.html",
        {
            "tool_meta": tool_meta,
            "timer_session_id": _TEST_SESSION_ID,
            "timer_started_at": None,
            "timer_paused_at": None,
        },
    )
    return _inject_base(html)


# ---------------------------------------------------------------------------
# Archive detail and session-closed page fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def archive_detail_html() -> str:
    """
    Pre-render the archive detail template using a lightweight mock record.

    No database access is required — all context values are supplied via
    SimpleNamespace objects.  The payload sections and download buttons are
    omitted (payload_output/input and md_file/rtf_file are falsy) so that
    no URL reversals for dynamic PKs are needed.
    """
    from datetime import datetime
    from django.template.loader import render_to_string

    record = SimpleNamespace(
        tool_slug="wise-crowds",
        tool_version="1.0",
        submitted_at=datetime(2025, 1, 15, 10, 30),
        user=SimpleNamespace(email="tester@example.com"),
        payload_output=None,
        payload_input=None,
        md_file=None,
        rtf_file=None,
    )
    return render_to_string("archive/detail.html", {"record": record})


@pytest.fixture(scope="session")
def canvas_html() -> str:
    """
    Pre-render the drawing-canvas partial template wrapped in a minimal HTML
    page so Playwright can load it via page.set_content().

    No database access is required — the canvas widget is entirely client-side
    once the HTML has been rendered.
    """
    from django.template.loader import render_to_string

    fragment = render_to_string("tools/_drawing_canvas.html", {})
    return (
        "<!DOCTYPE html>"
        "<html lang='en'>"
        "<head><meta charset='utf-8'><title>Canvas Test</title></head>"
        f"<body>{fragment}</body>"
        "</html>"
    )


@pytest.fixture(scope="session")
def phase_timer_milestone_html() -> str:
    """
    Pre-render the phase timer with a single 15-second phase.

    This fixture is used by milestone-count tests.  With a 15-second phase the
    only milestone that fires is the 10-second one (MILESTONES = [300, 120, 60,
    30, 10]).  After 5 simulated seconds the remaining time reaches 10 s and
    ``checkMilestones()`` emits "10 seconds remaining in Alpha" exactly once.
    """
    from django.template.loader import render_to_string

    tool_meta = SimpleNamespace(
        phases=[{"label": "Alpha", "seconds": 15}],
        timer_seconds=15,
        title="Milestone Timer",
    )
    return render_to_string(
        "tools/timer_test_page.html",
        {"tool_meta": tool_meta, "timer_session_id": None},
    )


@pytest.fixture(scope="session")
def phase_timer_long_milestone_html() -> str:
    """
    Pre-render the phase timer with a single 360-second phase.

    This fixture is used by milestone-count tests that must exercise the
    5-minute (300 s) milestone — the highest-priority entry in MILESTONES =
    [300, 120, 60, 30, 10].  With a 360-second phase the 300 s milestone fires
    after 60 simulated seconds of countdown (remaining goes from 361 → 300).
    ``checkMilestones()`` must emit "5 minutes remaining in Alpha" exactly once.
    """
    from django.template.loader import render_to_string

    tool_meta = SimpleNamespace(
        phases=[{"label": "Alpha", "seconds": 360}],
        timer_seconds=360,
        title="Long Milestone Timer",
    )
    return render_to_string(
        "tools/timer_test_page.html",
        {"tool_meta": tool_meta, "timer_session_id": None},
    )


@pytest.fixture(scope="session")
def archive_detail_with_payload_html() -> str:
    """
    Pre-render the archive detail template with both payload_output and
    payload_input present.

    The template renders extra <h2> sections ("Results" and "Your input") and
    key/value pairs when these fields are non-empty.  This fixture exercises
    those branches so that axe-core and heading-level tests can confirm the
    additional markup is accessible.
    """
    from datetime import datetime
    from django.template.loader import render_to_string

    record = SimpleNamespace(
        tool_slug="wise-crowds",
        tool_version="1.0",
        submitted_at=datetime(2025, 1, 15, 10, 30),
        user=SimpleNamespace(email="tester@example.com"),
        payload_output={
            "summary": "The group identified three key patterns.",
            "themes": "Trust, communication, shared goals.",
        },
        payload_input={
            "challenge": "How do we improve cross-team collaboration?",
            "context": "We are a team of 12 distributed across three time zones.",
        },
        md_file=None,
        rtf_file=None,
    )
    return render_to_string("archive/detail.html", {"record": record})


@pytest.fixture(scope="session")
def session_closed_html() -> str:
    """
    Pre-render the session-closed template using lightweight mock objects.

    The instances list is empty so the {% empty %} branch is taken and no
    per-participant URL reversals are needed.  Download links are suppressed
    by setting md_file and rtf_file to falsy values.
    """
    from datetime import datetime
    from django.template.loader import render_to_string

    tool_meta = SimpleNamespace(title="Wise Crowds")
    session = SimpleNamespace(
        closed_at=datetime(2025, 1, 15, 11, 0),
        host=SimpleNamespace(email="host@example.com"),
        md_file=None,
        rtf_file=None,
    )
    return render_to_string(
        "tools/session_closed.html",
        {"tool_meta": tool_meta, "session": session, "instances": []},
    )
