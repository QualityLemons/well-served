"""
Pytest configuration for the test suite.

Provides a `timer_html` fixture that pre-renders the timer widget template as a
plain string.  Browser tests use page.set_content() to load it directly, so no
live Django server is required — the timer widget is fully client-side once it
has been rendered.
"""

import os
from types import SimpleNamespace

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

# Chromium (Playwright) requires libgbm.so.1 which lives in the Nix profile
# library directory on Replit.  Prepend it to LD_LIBRARY_PATH before Django
# or any browser subprocess is launched so Playwright can find it without
# requiring a manual shell export.
_nix_lib = "/home/runner/.nix-profile/lib"
if os.path.isdir(_nix_lib):
    _existing = os.environ.get("LD_LIBRARY_PATH", "")
    if _nix_lib not in _existing:
        os.environ["LD_LIBRARY_PATH"] = f"{_nix_lib}:{_existing}" if _existing else _nix_lib

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
