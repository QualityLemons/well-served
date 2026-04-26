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


def _install_announcer_observer(page) -> None:
    """
    Inject a MutationObserver that records every textContent change on
    ``#phase-announcer`` into ``window.__announcerChanges``.

    Mirrors the helper of the same name in ``test_timer_a11y_browser.py``.
    Call this *after* the timer is visible but *before* the action under
    test so that every mutation is captured.
    """
    page.evaluate("""
        () => {
            window.__announcerChanges = [];
            const el = document.getElementById('phase-announcer');
            const obs = new MutationObserver(muts => {
                muts.forEach(m => {
                    window.__announcerChanges.push(m.target.textContent.trim());
                });
            });
            obs.observe(el, { childList: true, subtree: true, characterData: true });
        }
    """)


def _get_announcer_changes(page) -> list:
    """Return the list of textContent snapshots captured by the observer."""
    return page.evaluate("() => window.__announcerChanges")


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


class TestPausedJoinThenPauseResumeCycle:
    """
    Verify that ``_wasFSPaused`` does not suppress announcements for
    subsequent pause/resume transitions after the initial paused-join cue.

    Background
    ----------
    Task #62 added ``_wasFSPaused`` to silence the generic "Timer paused" cue
    when the richer firstSync paused-join cue fires simultaneously.  That guard
    is intentionally scoped to ``firstSync`` only, but no test previously
    confirmed that later pause/resume events still produce exactly one
    announcement each.

    Sequence tested
    ---------------
    1. ``firstSync`` poll → paused state → paused-join cue fires
       (precondition, verified by ``TestPausedJoinAnnouncement`` above).
    2. Second poll → running state → exactly one "Timer resumed" fires.
    3. Third poll → paused again → exactly one "Timer paused" fires.

    The 60 s simple timer (``session_simple_timer_html``) is used so the
    timer cannot expire during the ~8 s of fake-clock advances.

    A ``MutationObserver`` is installed before each observed action and
    ``window.__announcerChanges`` is inspected to count non-empty mutations.
    The observer is installed once; the list is reset between steps using a
    direct JS assignment to avoid attaching a second observer.
    """

    _POLL_MS = 4_100
    _SETTLE_MS = 200

    def test_resume_after_paused_join_fires_exactly_once(
        self, page, session_simple_timer_html
    ):
        """
        After joining a paused session (firstSync), the first server poll that
        shows the timer running must fire exactly one "Timer resumed"
        announcement — ``_wasFSPaused`` must not leak into non-firstSync cycles.
        """
        page.clock.install()
        T = page.evaluate("Date.now()")

        state = ["paused"]

        def handle_route(route):
            if state[0] == "paused":
                data = {
                    "status": "open",
                    "timer_started_at": _iso(T - 1_000),
                    "timer_paused_at": _iso(T),
                }
            else:
                data = {
                    "status": "open",
                    "timer_started_at": _iso(T - 1_000),
                    "timer_paused_at": None,
                }
            route.fulfill(content_type="application/json", body=json.dumps(data))

        page.route(_ROUTE_PATTERN, handle_route)
        _load_session(page, session_simple_timer_html)
        _wait_display(page, "00:59")
        _settle(page)

        first_text = _announcer_text(page)
        assert "Timer is paused" in first_text, (
            f"Precondition: firstSync must produce paused-join cue, got: '{first_text}'"
        )

        state[0] = "running"
        _install_announcer_observer(page)
        page.clock.run_for(self._POLL_MS)
        _settle(page)

        changes = _get_announcer_changes(page)
        non_empty = [c for c in changes if c]

        assert len(non_empty) == 1, (
            f"Expected exactly 1 non-empty announcement on resume after paused-join, "
            f"got {len(non_empty)}: {non_empty}"
        )
        assert non_empty[0] == "Timer resumed", (
            f"Expected 'Timer resumed', got: '{non_empty[0]}'"
        )

    def test_repause_after_resume_fires_exactly_once(
        self, page, session_simple_timer_html
    ):
        """
        After a paused-join → resume cycle in session mode, a subsequent
        server poll that shows the timer paused again must fire exactly one
        "Timer paused" announcement — ``_wasFSPaused`` must not permanently
        suppress the generic pause cue.
        """
        page.clock.install()
        T = page.evaluate("Date.now()")

        state = ["paused"]

        def handle_route(route):
            if state[0] == "paused":
                data = {
                    "status": "open",
                    "timer_started_at": _iso(T - 1_000),
                    "timer_paused_at": _iso(T),
                }
            elif state[0] == "running":
                data = {
                    "status": "open",
                    "timer_started_at": _iso(T - 1_000),
                    "timer_paused_at": None,
                }
            else:
                data = {
                    "status": "open",
                    "timer_started_at": _iso(T - 1_000),
                    "timer_paused_at": _iso(T + self._POLL_MS),
                }
            route.fulfill(content_type="application/json", body=json.dumps(data))

        page.route(_ROUTE_PATTERN, handle_route)
        _load_session(page, session_simple_timer_html)
        _wait_display(page, "00:59")
        _settle(page)

        assert "Timer is paused" in _announcer_text(page), (
            "Precondition: firstSync must produce paused-join cue"
        )

        state[0] = "running"
        page.clock.run_for(self._POLL_MS)
        _settle(page)

        state[0] = "paused-again"
        _install_announcer_observer(page)
        page.clock.run_for(self._POLL_MS)
        _settle(page)

        changes = _get_announcer_changes(page)
        non_empty = [c for c in changes if c]

        assert len(non_empty) == 1, (
            f"Expected exactly 1 non-empty announcement on re-pause after paused-join, "
            f"got {len(non_empty)}: {non_empty}"
        )
        assert non_empty[0] == "Timer paused", (
            f"Expected 'Timer paused', got: '{non_empty[0]}'"
        )
