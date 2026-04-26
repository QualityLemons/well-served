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

_nix_lib = "/home/runner/.nix-profile/lib"
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
