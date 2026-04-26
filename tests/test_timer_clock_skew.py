"""
Browser tests for clock-skew correction in the timer widget.

Both the multi-phase and simple timer variants track a ``clockSkew`` value
(milliseconds) computed from ``server_now`` on the first successful poll::

    clockSkew = new Date(data.server_now).getTime() - Date.now();

``applyServerTimestamp`` then uses ``Date.now() + clockSkew`` as the
reference time so elapsed-time calculations reflect the *server* clock even
when the client clock differs.

Test strategy
-------------
1. ``page.clock.install()`` freezes ``Date.now()`` (and pauses
   ``setInterval`` / ``setTimeout``) at the current real system time.
2. ``page.evaluate("Date.now()")`` reads the exact frozen value (``T``).
3. ``page.route()`` intercepts the status-poll fetch and returns a
   synthetic response built from ``T``:
   - *with-skew* tests:   ``server_now = T + SKEW``, ``timer_started_at``
     set so that server-elapsed == the target duration.
   - *no-server_now* tests: same ``timer_started_at`` but the ``server_now``
     field is omitted, so ``clockSkew`` stays 0 and ``referenceTime ==
     Date.now() == T``.
4. Because timers are paused, ``setInterval(tick, 1000)`` never fires and
   the display remains stable after the poll — no race conditions.

The pre-rendered HTML fixtures include a ``<base href="http://testhost/">``
tag so the relative poll URL resolves to an absolute URL that
``page.route()`` can intercept.  No live Django server is needed.
"""

import datetime
import json

import pytest


_ROUTE_PATTERN = "http://testhost/**"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _iso(ms_from_epoch: int) -> str:
    """Convert an integer ms-from-epoch value to an ISO-8601 UTC string."""
    dt = (
        datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
        + datetime.timedelta(milliseconds=ms_from_epoch)
    )
    ms_part = ms_from_epoch % 1000
    return dt.strftime(f"%Y-%m-%dT%H:%M:%S.{ms_part:03d}Z")


def _setup(page, html, *, elapsed_ms: int, skew_ms: int = 0):
    """
    Full test setup:

    1. Install the fake clock (pauses timers, freezes Date.now()).
    2. Read the frozen Date.now() value ``T`` from the browser.
    3. Compute ``timer_started_at`` and (if ``skew_ms != 0``) ``server_now``
       relative to ``T`` so elapsed and clock-skew are exact.
    4. Install a route that answers every poll with the fake response.
    5. Load the timer HTML.
    """
    page.clock.install()
    T = page.evaluate("Date.now()")

    server_now_ms = T + skew_ms
    timer_started_at_ms = server_now_ms - elapsed_ms

    data: dict = {
        "status": "open",
        "timer_started_at": _iso(timer_started_at_ms),
        "timer_paused_at": None,
    }
    if skew_ms:
        data["server_now"] = _iso(server_now_ms)

    body = json.dumps(data)
    page.route(_ROUTE_PATTERN, lambda route: route.fulfill(
        content_type="application/json", body=body
    ))

    page.set_content(html, wait_until="domcontentloaded")
    page.wait_for_selector(".timer-widget")


# ---------------------------------------------------------------------------
# Phase-timer tests  (3 × 3 s = 9 s total, phases: Alpha / Beta / Gamma)
# ---------------------------------------------------------------------------

class TestPhaseTimerClockSkew:
    """
    Skew scenario for the phase timer
    ----------------------------------
    * Server is 3 s ahead of client  (skew_ms = +3 000)
    * Timer started 5 server-seconds ago  (elapsed_ms = 5 000)
    * ``referenceTime = Date.now() + clockSkew = T + 3 000``
    * ``elapsedSec = floor((T + 3 000 − (T + 3 000 − 5 000)) / 1 000) = 5 s``
    * Phase 0 = Alpha (0–3 s), Phase 1 = Beta (3–6 s): at 5 s → Beta
    Without skew correction (no server_now):
    * ``referenceTime = T``
    * ``elapsedSec = floor((T − (T − 2 000)) / 1 000) = 2 s`` → Alpha
    """

    def test_skew_corrects_phase_position(self, page, session_phase_timer_html):
        """Clock-skew correction advances the displayed phase from Alpha to Beta."""
        _setup(page, session_phase_timer_html, elapsed_ms=5_000, skew_ms=3_000)

        page.wait_for_function(
            "document.querySelector('.timer-phase-label').textContent === 'Beta'"
        )

        label = page.locator(".timer-phase-label").inner_text()
        assert label == "Beta", (
            f"Expected 'Beta' with +3 s clock skew (server elapsed = 5 s), got '{label}'"
        )

    def test_no_server_now_uses_client_clock(self, page, session_phase_timer_html):
        """Without server_now, clockSkew = 0; client elapsed = 2 s → phase Alpha."""
        _setup(page, session_phase_timer_html, elapsed_ms=2_000, skew_ms=0)

        page.wait_for_function(
            "document.querySelector('.timer-display').textContent === '00:01'"
        )

        label = page.locator(".timer-phase-label").inner_text()
        assert label == "Alpha", (
            f"Expected 'Alpha' (no clock skew, client elapsed = 2 s), got '{label}'"
        )


# ---------------------------------------------------------------------------
# Simple-timer tests  (60 s, no phases)
# ---------------------------------------------------------------------------

class TestSimpleTimerClockSkew:
    """
    Skew scenario for the simple timer
    ------------------------------------
    * Server is 10 s ahead of client  (skew_ms = +10 000)
    * Timer started 20 server-seconds ago  (elapsed_ms = 20 000)
    * ``referenceTime = T + 10 000``
    * ``elapsedSec = floor((T + 10 000 − (T + 10 000 − 20 000)) / 1 000) = 20 s``
    * ``remaining = max(0, 60 − 20) = 40 s`` → display '00:40'
    Without skew correction (no server_now):
    * ``referenceTime = T``
    * ``elapsedSec = floor((T − (T − 10 000)) / 1 000) = 10 s``
    * ``remaining = max(0, 60 − 10) = 50 s`` → display '00:50'
    """

    def test_skew_corrects_remaining_time(self, page, session_simple_timer_html):
        """Clock-skew correction shows 40 s remaining instead of 50 s."""
        _setup(page, session_simple_timer_html, elapsed_ms=20_000, skew_ms=10_000)

        page.wait_for_function(
            "document.querySelector('.timer-display').textContent === '00:40'"
        )

        display = page.locator(".timer-display").inner_text()
        assert display == "00:40", (
            f"Expected '00:40' with +10 s clock skew (server elapsed = 20 s), got '{display}'"
        )

    def test_no_server_now_uses_client_clock(self, page, session_simple_timer_html):
        """Without server_now, clockSkew = 0; client elapsed = 10 s → '00:50'."""
        _setup(page, session_simple_timer_html, elapsed_ms=10_000, skew_ms=0)

        page.wait_for_function(
            "document.querySelector('.timer-display').textContent === '00:50'"
        )

        display = page.locator(".timer-display").inner_text()
        assert display == "00:50", (
            f"Expected '00:50' (no clock skew, client elapsed = 10 s), got '{display}'"
        )


# ---------------------------------------------------------------------------
# Re-measurement tests  — verify skew is updated on *every* poll
# ---------------------------------------------------------------------------

class TestClockSkewUpdatedEachPoll:
    """
    Verify that ``clockSkew`` is re-measured on every successful poll, not
    just the first.  This matters for tabs that are left open across a laptop
    sleep or mobile background: the first poll sets an initial skew, but
    subsequent polls must keep it fresh.

    Scenario (simple timer, 60 s)
    --------------------------------
    * First poll  (at fake time T):
        server_now = T + 10 000  →  clockSkew = +10 000
        timer_started_at = T − 10 000  →  elapsed = 20 s  →  remaining = 40 s
    * Clock advances 4 s (four ticks fire): remaining 40 → 36
    * Second poll fires at T + 4 000:
        server_now = T + 4 000  →  clockSkew is now re-measured to 0
        timer_started_at = T + 4 000 − 10 000 = T − 6 000  →  elapsed = 10 s
        →  remaining = 50 s  →  display '00:50'
    The jump from 36 s to 50 s proves clockSkew was updated on the second poll.
    """

    def test_skew_remeasured_on_second_poll(self, page, session_simple_timer_html):
        """Second poll updates clockSkew; remaining jumps from 36 s to 50 s."""
        page.clock.install()
        T = page.evaluate("Date.now()")

        call_count = [0]

        def _handler(route):
            call_count[0] += 1
            if call_count[0] == 1:
                body = json.dumps({
                    "status": "open",
                    "timer_started_at": _iso(T - 10_000),
                    "timer_paused_at": None,
                    "server_now": _iso(T + 10_000),
                })
            else:
                body = json.dumps({
                    "status": "open",
                    "timer_started_at": _iso(T - 6_000),
                    "timer_paused_at": None,
                    "server_now": _iso(T + 4_000),
                })
            route.fulfill(content_type="application/json", body=body)

        page.route(_ROUTE_PATTERN, _handler)
        page.set_content(session_simple_timer_html, wait_until="domcontentloaded")
        page.wait_for_selector(".timer-widget")

        page.wait_for_function(
            "document.querySelector('.timer-display').textContent === '00:40'"
        )

        page.clock.run_for(4_000)

        page.wait_for_function(
            "document.querySelector('.timer-display').textContent === '00:50'"
        )

        display = page.locator(".timer-display").inner_text()
        assert display == "00:50", (
            f"Expected '00:50' after second poll re-measured clockSkew to 0, "
            f"got '{display}'"
        )
