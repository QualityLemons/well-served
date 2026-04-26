"""
Browser tests for the paused-join announcement (Task #36).

When a participant opens a session page while the timer is paused,
``applyServerTimestamp()`` fires on ``firstSync`` with ``timerPausedAt``
set and announces via ``#phase-announcer``:

* Phase timer: "Timer is paused — about X seconds remaining in <phase>"
* Simple timer: "Timer is paused — about X seconds remaining"

Test strategy
-------------
1. ``page.clock.install()`` — freezes ``Date.now()`` (T) and pauses
   ``setTimeout``/``setInterval``.
2. A ``page.route()`` handler returns a synthetic paused status: the
   ``timer_started_at`` is placed a few seconds before T and
   ``timer_paused_at`` is set to T.
3. ``page.set_content()`` loads the session-mode HTML.  The timer's
   ``pollTimerState()`` fires an immediate ``fetch()`` call — network
   requests are *not* paused by the fake clock, so the route handler
   intercepts it instantly.
4. ``page.wait_for_function()`` waits for ``applyServerTimestamp`` to
   have updated the display (the remaining-time update is synchronous).
5. ``page.clock.run_for(200)`` advances the fake clock past
   ``ANNOUNCE_DELAY_MS`` (50 ms) so the deferred ``textContent`` write
   fires and the live region is populated.
6. The test reads ``#phase-announcer.innerText`` and asserts on its
   content.

Fixtures used
-------------
* ``session_phase_timer_html`` — 3 × 3 s phase timer in session mode
  (``conftest.py``).
* ``session_simple_timer_html`` — 60 s simple timer in session mode
  (``conftest.py``).

No running Django server is required; all fetch calls are intercepted by
``page.route()``.
"""

import datetime
import json

import pytest


_ROUTE_PATTERN = "http://testhost/**"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _iso(ms_from_epoch: int) -> str:
    """Convert a millisecond-epoch integer to an ISO-8601 UTC string."""
    dt = (
        datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
        + datetime.timedelta(milliseconds=ms_from_epoch)
    )
    ms_part = ms_from_epoch % 1000
    return dt.strftime(f"%Y-%m-%dT%H:%M:%S.{ms_part:03d}Z")


def _setup_route(page, T: int, *, elapsed_ms: int, paused: bool) -> None:
    """
    Install a ``page.route`` that answers every status-poll fetch with a
    synthetic response.

    Parameters
    ----------
    T:
        The frozen ``Date.now()`` value read from the browser.
    elapsed_ms:
        How many milliseconds ago the timer was started (relative to T for
        a running timer, or relative to the pause time for a paused timer).
    paused:
        If ``True`` the response includes ``timer_paused_at = T``.
    """
    data = {
        "status": "open",
        "timer_started_at": _iso(T - elapsed_ms),
        "timer_paused_at": _iso(T) if paused else None,
    }
    body = json.dumps(data)
    page.route(_ROUTE_PATTERN, lambda route: route.fulfill(
        content_type="application/json", body=body
    ))


def _load_session(page, html: str) -> None:
    """Load the session-mode HTML and wait for the timer widget to appear."""
    page.set_content(html, wait_until="domcontentloaded")
    page.wait_for_selector(".timer-widget")


def _wait_display(page, expected: str) -> None:
    """
    Block until the timer display shows ``expected``.

    This is used as a synchronisation point to confirm that
    ``applyServerTimestamp`` has finished processing the poll response
    before we advance the fake clock to fire the announcement timeout.
    """
    page.wait_for_function(
        f"document.querySelector('.timer-display').textContent === '{expected}'"
    )


def _settle(page, ms: int = 200) -> None:
    """Advance the fake clock ``ms`` milliseconds past ``ANNOUNCE_DELAY_MS``."""
    page.clock.run_for(ms)


def _announcer_text(page) -> str:
    return page.locator("#phase-announcer").inner_text()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestPausedJoinAnnouncement:
    """
    Verify the first-sync paused-join announcement in both timer variants.

    Phase timer maths (3 × 3 s, phases: Alpha / Beta / Gamma)
    ----------------------------------------------------------
    * ``elapsed_ms = 1 000`` → ``elapsedSec = 1``
    * Phase 0 (Alpha): 0–3 s active → ``remaining = 3 − 1 = 2``
    * ``approxLabel(2)`` → "about 2 seconds"
    * Expected: "Timer is paused — about 2 seconds remaining in Alpha"

    Simple timer maths (60 s)
    -------------------------
    * ``elapsed_ms = 30 000`` → ``elapsedSec = 30``
    * ``remaining = 60 − 30 = 30``
    * ``approxLabel(30)`` → "about 30 seconds"
    * Expected: "Timer is paused — about 30 seconds remaining"
    """

    def test_phase_timer_announces_paused_cue_on_first_sync(
        self, page, session_phase_timer_html
    ):
        """
        Participant joining a paused phase-timer session must hear
        "Timer is paused — about 2 seconds remaining in Alpha".
        """
        page.clock.install()
        T = page.evaluate("Date.now()")

        _setup_route(page, T, elapsed_ms=1_000, paused=True)
        _load_session(page, session_phase_timer_html)
        _wait_display(page, "00:02")
        _settle(page)

        text = _announcer_text(page)
        expected = "Timer is paused \u2014 about 2 seconds remaining in Alpha"
        assert text == expected, (
            f"Phase-timer paused-join announcement mismatch.\n"
            f"  expected: '{expected}'\n"
            f"  got:      '{text}'"
        )

    def test_simple_timer_announces_paused_cue_on_first_sync(
        self, page, session_simple_timer_html
    ):
        """
        Participant joining a paused simple-timer session must hear
        "Timer is paused — about 30 seconds remaining" (no phase name).
        """
        page.clock.install()
        T = page.evaluate("Date.now()")

        _setup_route(page, T, elapsed_ms=30_000, paused=True)
        _load_session(page, session_simple_timer_html)
        _wait_display(page, "00:30")
        _settle(page)

        text = _announcer_text(page)
        expected = "Timer is paused \u2014 about 30 seconds remaining"
        assert text == expected, (
            f"Simple-timer paused-join announcement mismatch.\n"
            f"  expected: '{expected}'\n"
            f"  got:      '{text}'"
        )

    def test_phase_timer_running_join_does_not_say_paused(
        self, page, session_phase_timer_html
    ):
        """
        Participant joining a *running* phase-timer session must NOT hear
        "Timer is paused".  They should receive the normal position cue
        ("about 2 seconds remaining in Alpha").
        """
        page.clock.install()
        T = page.evaluate("Date.now()")

        _setup_route(page, T, elapsed_ms=1_000, paused=False)
        _load_session(page, session_phase_timer_html)
        _wait_display(page, "00:02")
        _settle(page)

        text = _announcer_text(page)
        assert "Timer is paused" not in text, (
            f"Running-timer join must not announce 'Timer is paused', "
            f"got: '{text}'"
        )

    def test_simple_timer_running_join_does_not_say_paused(
        self, page, session_simple_timer_html
    ):
        """
        Participant joining a *running* simple-timer session must NOT hear
        "Timer is paused".
        """
        page.clock.install()
        T = page.evaluate("Date.now()")

        _setup_route(page, T, elapsed_ms=30_000, paused=False)
        _load_session(page, session_simple_timer_html)
        _wait_display(page, "00:30")
        _settle(page)

        text = _announcer_text(page)
        assert "Timer is paused" not in text, (
            f"Running simple-timer join must not announce 'Timer is paused', "
            f"got: '{text}'"
        )

    def test_phase_timer_paused_join_announces_only_once(
        self, page, session_phase_timer_html
    ):
        """
        The paused-join cue must fire exactly once (firstSync only).

        After the first poll the announcer is manually cleared; then the
        fake clock is advanced past the 4 000 ms poll interval so a second
        ``pollTimerState`` fires.  The second poll must NOT re-announce the
        paused cue because ``firstSync`` is already ``false``.
        """
        page.clock.install()
        T = page.evaluate("Date.now()")

        _setup_route(page, T, elapsed_ms=1_000, paused=True)
        _load_session(page, session_phase_timer_html)
        _wait_display(page, "00:02")
        _settle(page)

        first_text = _announcer_text(page)
        assert "Timer is paused" in first_text, (
            f"First poll must produce paused-join cue, got: '{first_text}'"
        )

        page.evaluate("document.getElementById('phase-announcer').textContent = ''")
        page.clock.run_for(4_200)

        second_text = _announcer_text(page)
        assert "Timer is paused" not in second_text, (
            f"Second poll must NOT repeat paused-join cue (firstSync=false), "
            f"got: '{second_text}'"
        )
