"""
Browser-based accessibility tests for the phase timer widget.

These tests use Playwright to run the timer in a real browser (Chromium) and
inject axe-core to catch ARIA violations that only appear at runtime, such as:
  - stale aria-label text on progress segments
  - live regions that stop updating
  - focus-management problems during phase transitions

The tests use Playwright's built-in fake-clock API so phase transitions can be
triggered instantly without waiting for real time to pass.

The timer template is pre-rendered server-side in the `timer_html` fixture and
loaded into the browser via `page.set_content()`, so no running Django server is
needed during the Playwright tests.

Each test loads a fresh copy of the HTML so that clock state is never shared
between tests — this makes the suite deterministic and parallelism-safe.

Clock note
----------
We use `page.clock.run_for()` (not `fast_forward`) because the timer's
`announce()` function defers textContent updates via setTimeout(fn, ANNOUNCE_DELAY_MS).
`run_for` fires both timer callbacks and setTimeout callbacks, so the live region
is always up to date when the assertion runs.

Manual screen-reader verification checklist
-------------------------------------------
The automated suite catches DOM-level regressions but cannot replace real
assistive technology.  Run the following scenario with VoiceOver (macOS) or
NVDA (Windows) after any change to _timer.html:

  Setup
  -----
  1. Open the timer test page (or any session page with a phase timer).
  2. Enable the screen reader (VoiceOver: Cmd+F5 / NVDA: Ctrl+Alt+N).

  Phase timer — start and milestones
  -----------------------------------
  3. Press Start.  SR must say "Running…" (button label change) — no extra
     announcement is expected at this point.
  4. Wait (or use browser dev-tools to jump the clock) until 5 minutes remain
     in the first phase.  SR must announce "5 minutes remaining in <Phase 1>".
  5. Repeat for 2 minutes, 1 minute, 30 seconds, 10 seconds.

  Phase transition
  ----------------
  6. Allow phase 1 to expire.  SR must say "Now entering Phase 2 — <label>".
     The announcement should not be doubled.

  Completion
  ----------
  7. Allow all phases to expire.  SR must say "All phases complete".

  Pause / resume
  --------------
  8. While the timer is running, press Pause (host view).
     SR must say "Timer paused" exactly once.
     The paused elapsed counter ("Paused · 3s" etc.) must NOT be announced
     repeatedly — the badge carries aria-hidden="true" so it is invisible to
     screen readers.
  9. Press Resume (Start).  SR must say "Timer resumed" exactly once.

  Late-join initial cue
  ---------------------
  10. Join a session mid-run (simulate by refreshing the page while the timer
      is active).  SR must announce approximately how much time remains,
      e.g. "about 3 minutes remaining in <Phase 1>".

  Expected: all announcements above are spoken clearly, without doubling or
  swallowing, on both NVDA/Firefox and VoiceOver/Safari.
"""

from pathlib import Path

import pytest

AXE_SCRIPT = Path(__file__).parent / "axe.min.js"

PHASE_SECONDS = 3
PHASE_MS = PHASE_SECONDS * 1000
TICK_MS = PHASE_MS + 500


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_timer(page, timer_html: str) -> None:
    """
    Install a fake clock, load the pre-rendered timer HTML into the browser
    page, and wait for the widget to be visible.

    The clock is installed before `set_content` so that every timer-related
    browser API (setInterval, setTimeout, requestAnimationFrame, Date) is under
    test control from the very first script execution on the page.
    """
    page.clock.install()
    page.set_content(timer_html, wait_until="domcontentloaded")
    page.wait_for_selector(".timer-widget")


def _advance(page, milliseconds: int) -> None:
    """
    Advance the fake clock *and* flush any pending requestAnimationFrame
    callbacks.

    `page.clock.run_for` fires both setTimeout/setInterval timers and rAF
    callbacks, ensuring that the `announce()` helper's rAF-deferred
    textContent update is visible to the test before it reads the live region.
    """
    page.clock.run_for(milliseconds)


def _run_axe(page) -> dict:
    """Inject axe-core (if not already present) and return axe.run() results."""
    if not page.evaluate("typeof window.axe !== 'undefined'"):
        page.add_script_tag(path=str(AXE_SCRIPT))
    results = page.evaluate("""
        async () => {
            const r = await window.axe.run(document.body, {
                runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa'] }
            });
            return {
                violations: r.violations.map(v => ({
                    id: v.id,
                    impact: v.impact,
                    description: v.description,
                    nodes: v.nodes.map(n => n.html).slice(0, 3),
                })),
                passes: r.passes.length,
            };
        }
    """)
    return results


def _assert_no_violations(results: dict, label: str) -> None:
    violations = results.get("violations", [])
    if violations:
        summary = "\n".join(
            f"  [{v['impact']}] {v['id']}: {v['description']}\n"
            f"    nodes: {v['nodes']}"
            for v in violations
        )
        pytest.fail(
            f"axe-core found {len(violations)} violation(s) at stage '{label}':\n{summary}"
        )


def _announcer_text(page) -> str:
    return page.locator("#phase-announcer").inner_text()


def _install_announcer_observer(page) -> None:
    """
    Inject a MutationObserver that records every textContent change on
    ``#phase-announcer`` into ``window.__announcerChanges``.

    Call this *after* the timer widget is visible but *before* the action
    under test (pause/resume/reset) so that every mutation is captured.
    The list accumulates both the '' clear and the actual message text,
    allowing the test to count non-empty announcements separately.
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

class TestTimerA11yBrowserInitial:
    """Tests that run against the timer in its initial (not-yet-started) state."""

    def test_initial_state_no_axe_violations(self, page, timer_html):
        """The timer widget at rest must be free of WCAG 2 AA violations."""
        _load_timer(page, timer_html)
        results = _run_axe(page)
        _assert_no_violations(results, "initial state")

    def test_initial_phase_label(self, page, timer_html):
        """Phase label must show the first phase ('Alpha') on load."""
        _load_timer(page, timer_html)
        label = page.locator(".timer-phase-label").inner_text()
        assert label == "Alpha", f"Expected 'Alpha', got '{label}'"

    def test_initial_progress_text(self, page, timer_html):
        """Phase progress text must read 'Phase 1 of 3' on load."""
        _load_timer(page, timer_html)
        text = page.locator(".timer-phase-progress").inner_text()
        assert text == "Phase 1 of 3", f"Expected 'Phase 1 of 3', got '{text}'"

    def test_initial_progress_bar_aria_state(self, page, timer_html):
        """
        On load, the JS calls renderPhase() immediately, which marks the
        first segment as 'active' and all subsequent ones as 'upcoming'.
        This verifies that the ARIA state is correct before the timer starts.
        """
        _load_timer(page, timer_html)
        segments = page.locator(".phase-segment").all()
        assert len(segments) == 3

        label_0 = segments[0].get_attribute("aria-label") or ""
        label_1 = segments[1].get_attribute("aria-label") or ""
        label_2 = segments[2].get_attribute("aria-label") or ""

        assert "active" in label_0, (
            f"Segment 0 (current phase) should be 'active' on load, got: '{label_0}'"
        )
        assert "upcoming" in label_1, (
            f"Segment 1 should be 'upcoming' on load, got: '{label_1}'"
        )
        assert "upcoming" in label_2, (
            f"Segment 2 should be 'upcoming' on load, got: '{label_2}'"
        )


class TestTimerA11yBrowserRunning:
    """Tests that run the timer for a short while before checking."""

    def test_running_state_no_axe_violations(self, page, timer_html):
        """Axe must pass immediately after the Start button is pressed."""
        _load_timer(page, timer_html)
        page.locator(".timer-start").click()
        _advance(page, 500)
        results = _run_axe(page)
        _assert_no_violations(results, "running (0.5 s into phase 1)")


class TestTimerA11yBrowserPhaseTransitions:
    """
    Tests that verify live-region updates and ARIA state at each phase
    transition.

    Each test starts the timer from scratch and advances the clock
    independently using INCREMENTAL steps — one TICK_MS per phase — so that
    `run_for` has a chance to flush the rAF callbacks for each announcement
    before the next tick batch starts.
    """

    def test_phase_1_to_2_live_region_announcement(self, page, timer_html):
        """
        After phase 1 finishes, the live-region must announce
        'Now entering Phase 2 — Beta'.
        """
        _load_timer(page, timer_html)
        page.locator(".timer-start").click()
        _advance(page, TICK_MS)
        text = _announcer_text(page)
        assert "Now entering Phase 2" in text, f"Announcer: '{text}'"
        assert "Beta" in text, f"Phase label absent from announcer: '{text}'"

    def test_phase_2_no_axe_violations(self, page, timer_html):
        """Axe must pass while phase 2 is active."""
        _load_timer(page, timer_html)
        page.locator(".timer-start").click()
        _advance(page, TICK_MS)
        results = _run_axe(page)
        _assert_no_violations(results, "phase 2 active")

    def test_phase_2_progress_bar_aria_labels(self, page, timer_html):
        """
        After the phase 1 → 2 transition the progress-bar segments must carry
        correct aria-label state ('completed', 'active', 'upcoming').
        """
        _load_timer(page, timer_html)
        page.locator(".timer-start").click()
        _advance(page, TICK_MS)

        segments = page.locator(".phase-segment").all()
        assert len(segments) == 3

        labels = [seg.get_attribute("aria-label") or "" for seg in segments]
        assert "completed" in labels[0], f"Segment 0 expected completed, got: '{labels[0]}'"
        assert "active" in labels[1], f"Segment 1 expected active, got: '{labels[1]}'"
        assert "upcoming" in labels[2], f"Segment 2 expected upcoming, got: '{labels[2]}'"

    def test_phase_2_to_3_live_region_announcement(self, page, timer_html):
        """
        After phase 2 finishes, the live-region must announce
        'Now entering Phase 3 — Gamma'.
        """
        _load_timer(page, timer_html)
        page.locator(".timer-start").click()
        _advance(page, TICK_MS)
        _advance(page, TICK_MS)
        text = _announcer_text(page)
        assert "Now entering Phase 3" in text, f"Announcer: '{text}'"
        assert "Gamma" in text, f"Phase label absent from announcer: '{text}'"

    def test_phase_3_no_axe_violations(self, page, timer_html):
        """Axe must pass while phase 3 is active."""
        _load_timer(page, timer_html)
        page.locator(".timer-start").click()
        _advance(page, TICK_MS)
        _advance(page, TICK_MS)
        results = _run_axe(page)
        _assert_no_violations(results, "phase 3 active")


class TestTimerA11yBrowserCompletion:
    """Tests for the state after all phases have elapsed."""

    def test_all_phases_complete_live_region(self, page, timer_html):
        """
        When the last phase expires the live-region must say
        'All phases complete'.
        """
        _load_timer(page, timer_html)
        page.locator(".timer-start").click()
        _advance(page, TICK_MS)
        _advance(page, TICK_MS)
        _advance(page, TICK_MS)
        text = _announcer_text(page)
        assert "All phases complete" in text, f"Announcer: '{text}'"

    def test_completion_no_axe_violations(self, page, timer_html):
        """Axe must pass when all phases have finished."""
        _load_timer(page, timer_html)
        page.locator(".timer-start").click()
        _advance(page, TICK_MS)
        _advance(page, TICK_MS)
        _advance(page, TICK_MS)
        results = _run_axe(page)
        _assert_no_violations(results, "all phases complete")

    def test_completion_segments_aria_state(self, page, timer_html):
        """
        After the final phase expires, every segment must carry '— completed'
        in its aria-label.  The last segment must be 'completed' (not 'active')
        so that screen readers do not announce it as still running.
        """
        _load_timer(page, timer_html)
        page.locator(".timer-start").click()
        _advance(page, TICK_MS)
        _advance(page, TICK_MS)
        _advance(page, TICK_MS)

        segments = page.locator(".phase-segment").all()
        assert len(segments) == 3

        for i, seg in enumerate(segments):
            label = seg.get_attribute("aria-label") or ""
            assert "completed" in label, (
                f"Segment {i} should be completed after all phases end, got: '{label}'"
            )

    def test_live_region_aria_attributes_stable_after_run(self, page, timer_html):
        """
        The live-region's aria-live and aria-atomic attributes must still be
        correct after the timer has finished — JS must not have mutated them.
        """
        _load_timer(page, timer_html)
        page.locator(".timer-start").click()
        _advance(page, TICK_MS)
        _advance(page, TICK_MS)
        _advance(page, TICK_MS)

        announcer = page.locator("#phase-announcer")
        assert announcer.get_attribute("aria-live") == "assertive"
        assert announcer.get_attribute("aria-atomic") == "true"


class TestTimerA11yBrowserKeyboard:
    """
    Tests that the timer Start / Pause / Reset buttons can be operated
    entirely by keyboard (Tab to move focus, Space or Enter to activate).

    No mouse or .click() interaction is used anywhere in this class.  Every
    button activation goes through page.keyboard.press() so that the test
    exercises the same code path a keyboard-only user would trigger.

    Note on disabled buttons
    ------------------------
    HTML disabled buttons are removed from the tab order, so the Pause button
    (initially disabled) is only reachable once the timer has been started and
    it becomes enabled.  Tests that need to reach Pause therefore start the
    timer first (via keyboard) before calling .focus() on it.
    """

    # ------------------------------------------------------------------
    # Tab-order / focus reachability
    # ------------------------------------------------------------------

    def test_start_button_reachable_by_tab(self, page, timer_html):
        """A single Tab from the document body must land on the Start button."""
        _load_timer(page, timer_html)
        page.keyboard.press("Tab")
        focused_class = page.evaluate("document.activeElement.className")
        assert "timer-start" in focused_class, (
            f"Expected Start button to receive first Tab focus, got class: '{focused_class}'"
        )

    def test_reset_button_reachable_by_tab_after_start(self, page, timer_html):
        """
        In the initial state the Pause button is disabled (not in tab order).
        Two Tabs from the document body should reach Start then Reset.
        """
        _load_timer(page, timer_html)
        page.keyboard.press("Tab")
        page.keyboard.press("Tab")
        focused_class = page.evaluate("document.activeElement.className")
        assert "timer-reset" in focused_class, (
            f"Expected Reset button after two Tabs from body, got class: '{focused_class}'"
        )

    def test_pause_button_reachable_by_tab_when_running(self, page, timer_html):
        """Once the timer is running the Pause button must be in the Tab order."""
        _load_timer(page, timer_html)
        start_btn = page.locator(".timer-start")
        start_btn.focus()
        page.keyboard.press("Space")
        _advance(page, 100)

        page.keyboard.press("Tab")
        focused_class = page.evaluate("document.activeElement.className")
        assert "timer-pause" in focused_class, (
            f"Expected Pause button to be reached by Tab while running, "
            f"got class: '{focused_class}'"
        )

    # ------------------------------------------------------------------
    # Start button — Space and Enter activation
    # ------------------------------------------------------------------

    def test_start_button_activates_with_space(self, page, timer_html):
        """Space on the focused Start button must start the timer."""
        _load_timer(page, timer_html)
        start_btn = page.locator(".timer-start")
        start_btn.focus()
        focused_class = page.evaluate("document.activeElement.className")
        assert "timer-start" in focused_class, "Start button should hold focus before activation"

        page.keyboard.press("Space")
        _advance(page, 100)
        assert start_btn.is_disabled(), "Start button should be disabled while running"
        assert start_btn.inner_text() == "Running\u2026"

    def test_start_button_activates_with_enter(self, page, timer_html):
        """Enter on the focused Start button must start the timer."""
        _load_timer(page, timer_html)
        start_btn = page.locator(".timer-start")
        start_btn.focus()
        page.keyboard.press("Enter")
        _advance(page, 100)
        assert start_btn.is_disabled(), "Start button should be disabled while running"
        assert start_btn.inner_text() == "Running\u2026"

    # ------------------------------------------------------------------
    # Pause button — Space and Enter activation
    # ------------------------------------------------------------------

    def test_pause_button_activates_with_space(self, page, timer_html):
        """Space on the Pause button must pause the running timer."""
        _load_timer(page, timer_html)
        start_btn = page.locator(".timer-start")
        start_btn.focus()
        page.keyboard.press("Space")
        _advance(page, 100)

        pause_btn = page.locator(".timer-pause")
        pause_btn.focus()
        focused_class = page.evaluate("document.activeElement.className")
        assert "timer-pause" in focused_class, "Pause button should hold focus before activation"

        page.keyboard.press("Space")
        _advance(page, 100)
        assert pause_btn.is_disabled(), "Pause button should be disabled after pausing"
        assert start_btn.inner_text() == "Resume"

    def test_pause_button_activates_with_enter(self, page, timer_html):
        """Enter on the Pause button must pause the running timer."""
        _load_timer(page, timer_html)
        start_btn = page.locator(".timer-start")
        start_btn.focus()
        page.keyboard.press("Enter")
        _advance(page, 100)

        pause_btn = page.locator(".timer-pause")
        pause_btn.focus()
        page.keyboard.press("Enter")
        _advance(page, 100)
        assert pause_btn.is_disabled(), "Pause button should be disabled after pausing"
        assert start_btn.inner_text() == "Resume"

    # ------------------------------------------------------------------
    # Resume — full start → pause → resume cycle by keyboard alone
    # ------------------------------------------------------------------

    def test_resume_by_keyboard_after_pause(self, page, timer_html):
        """After pausing via keyboard, the timer can be resumed via keyboard alone."""
        _load_timer(page, timer_html)
        start_btn = page.locator(".timer-start")
        pause_btn = page.locator(".timer-pause")

        start_btn.focus()
        page.keyboard.press("Space")
        _advance(page, 100)
        assert start_btn.is_disabled(), "Start button should be disabled while running"

        pause_btn.focus()
        page.keyboard.press("Space")
        _advance(page, 100)
        assert start_btn.inner_text() == "Resume", "Start button should show 'Resume' when paused"

        start_btn.focus()
        focused_class = page.evaluate("document.activeElement.className")
        assert "timer-start" in focused_class, "Start/Resume button should accept focus when paused"
        page.keyboard.press("Space")
        _advance(page, 100)
        assert start_btn.is_disabled(), "Start button should be disabled after keyboard resume"
        assert start_btn.inner_text() == "Running\u2026"

    # ------------------------------------------------------------------
    # Reset button — Space and Enter activation, live-region announcement
    # ------------------------------------------------------------------

    def test_reset_button_activates_with_space(self, page, timer_html):
        """Space on the Reset button must reset the timer to its initial state."""
        _load_timer(page, timer_html)
        start_btn = page.locator(".timer-start")
        start_btn.focus()
        page.keyboard.press("Space")
        _advance(page, TICK_MS)

        reset_btn = page.locator(".timer-reset")
        reset_btn.focus()
        focused_class = page.evaluate("document.activeElement.className")
        assert "timer-reset" in focused_class, "Reset button should hold focus before activation"

        page.keyboard.press("Space")
        _advance(page, 100)

        label = page.locator(".timer-phase-label").inner_text()
        assert label == "Alpha", f"Expected 'Alpha' after keyboard reset, got: '{label}'"
        assert start_btn.inner_text() == "Start"

    def test_reset_button_activates_with_enter(self, page, timer_html):
        """Enter on the Reset button must reset the timer to its initial state."""
        _load_timer(page, timer_html)
        start_btn = page.locator(".timer-start")
        start_btn.focus()
        page.keyboard.press("Space")
        _advance(page, TICK_MS)

        reset_btn = page.locator(".timer-reset")
        reset_btn.focus()
        page.keyboard.press("Enter")
        _advance(page, 100)

        label = page.locator(".timer-phase-label").inner_text()
        assert label == "Alpha", f"Expected 'Alpha' after keyboard reset, got: '{label}'"

    def test_reset_announces_via_live_region(self, page, timer_html):
        """Resetting via keyboard must trigger a 'Timer reset' live-region announcement."""
        _load_timer(page, timer_html)
        start_btn = page.locator(".timer-start")
        start_btn.focus()
        page.keyboard.press("Space")
        _advance(page, 500)

        reset_btn = page.locator(".timer-reset")
        reset_btn.focus()
        page.keyboard.press("Space")
        _advance(page, 200)

        text = _announcer_text(page)
        assert "Timer reset" in text, (
            f"Expected 'Timer reset' in live region after keyboard reset, got: '{text}'"
        )


# ---------------------------------------------------------------------------
# Announcement-count tests — exactly one SR announcement per pause / resume
# ---------------------------------------------------------------------------

class TestPauseResumeAnnouncementCount:
    """
    Verify that pausing or resuming the timer causes ``#phase-announcer`` to
    emit exactly one non-empty announcement ("Timer paused" / "Timer resumed").

    Background
    ----------
    A previous bug emitted two announcements on pause: one from the
    ``#phase-announcer`` live region and a second from the ``.timer-paused-badge``
    which also carried ``aria-live``.  The fix was to strip ``aria-live`` from
    the badge.  These tests catch any regression by:

    1. Attaching a MutationObserver to ``#phase-announcer`` before the action.
    2. Triggering pause or resume.
    3. Advancing the fake clock past ``ANNOUNCE_DELAY_MS`` (50 ms) so the
       deferred ``textContent`` update fires.
    4. Asserting that exactly one *non-empty* mutation was captured —
       i.e. the '' clear followed by the message text, giving one non-empty
       entry.

    The paused-badge test additionally confirms that the badge element itself
    carries no ``aria-live`` attribute, so screen readers never read its
    continuously-updating elapsed-time text.
    """

    # How long (ms) to advance the fake clock after triggering an action so
    # that the ANNOUNCE_DELAY_MS setTimeout (50 ms) has fired.
    _SETTLE_MS = 200

    def test_pause_fires_exactly_one_announcement(self, page, timer_html):
        """
        Clicking Pause while the timer is running must produce exactly one
        non-empty change on ``#phase-announcer`` — the text "Timer paused".
        """
        _load_timer(page, timer_html)

        page.locator(".timer-start").click()
        _advance(page, 100)

        _install_announcer_observer(page)

        page.locator(".timer-pause").click()
        _advance(page, self._SETTLE_MS)

        changes = _get_announcer_changes(page)
        non_empty = [c for c in changes if c]

        assert len(non_empty) == 1, (
            f"Expected exactly 1 non-empty announcement on pause, "
            f"got {len(non_empty)}: {non_empty}"
        )
        assert non_empty[0] == "Timer paused", (
            f"Expected announcement text 'Timer paused', got: '{non_empty[0]}'"
        )

    def test_resume_fires_exactly_one_announcement(self, page, timer_html):
        """
        Clicking Resume (after a pause) must produce exactly one non-empty
        change on ``#phase-announcer`` — the text "Timer resumed".
        """
        _load_timer(page, timer_html)

        page.locator(".timer-start").click()
        _advance(page, 100)
        page.locator(".timer-pause").click()
        _advance(page, self._SETTLE_MS)

        _install_announcer_observer(page)

        page.locator(".timer-start").click()
        _advance(page, self._SETTLE_MS)

        changes = _get_announcer_changes(page)
        non_empty = [c for c in changes if c]

        assert len(non_empty) == 1, (
            f"Expected exactly 1 non-empty announcement on resume, "
            f"got {len(non_empty)}: {non_empty}"
        )
        assert non_empty[0] == "Timer resumed", (
            f"Expected announcement text 'Timer resumed', got: '{non_empty[0]}'"
        )

    def test_paused_badge_has_no_aria_live(self, page, timer_html):
        """
        The ``.timer-paused-badge`` element must not carry an ``aria-live``
        attribute.  If it did, screen readers would continuously read out the
        updating elapsed-pause-time text ("Paused · 3s", "Paused · 4s", …).
        """
        _load_timer(page, timer_html)

        page.locator(".timer-start").click()
        _advance(page, 100)
        page.locator(".timer-pause").click()
        _advance(page, self._SETTLE_MS)

        aria_live = page.locator(".timer-paused-badge").get_attribute("aria-live")
        assert aria_live is None, (
            f"Paused badge must not have aria-live (found: '{aria_live}'). "
            "This would cause the elapsed-pause timer to be announced repeatedly."
        )

    def test_paused_badge_visible_after_pause(self, page, timer_html):
        """
        Sanity check: the ``.timer-paused-badge`` must be visible after pausing
        (not hidden), confirming the DOM state is correct before the aria-live
        check above is meaningful.
        """
        _load_timer(page, timer_html)

        page.locator(".timer-start").click()
        _advance(page, 100)
        page.locator(".timer-pause").click()
        _advance(page, self._SETTLE_MS)

        badge = page.locator(".timer-paused-badge")
        assert badge.is_visible(), "Paused badge should be visible after pausing"

    def test_paused_badge_hidden_after_resume(self, page, timer_html):
        """
        The ``.timer-paused-badge`` must disappear once the timer resumes,
        confirming the full pause → resume lifecycle is correct.
        """
        _load_timer(page, timer_html)

        page.locator(".timer-start").click()
        _advance(page, 100)
        page.locator(".timer-pause").click()
        _advance(page, self._SETTLE_MS)
        page.locator(".timer-start").click()
        _advance(page, self._SETTLE_MS)

        badge = page.locator(".timer-paused-badge")
        assert not badge.is_visible(), "Paused badge should be hidden after resuming"


# ---------------------------------------------------------------------------
# Reset-announcement accuracy tests
# ---------------------------------------------------------------------------

class TestResetAnnouncementAccuracy:
    """
    Verify that resetting the timer always announces "Timer reset" — never
    "Timer resumed" — regardless of whether the timer is paused or running
    at the time of the reset.

    Background
    ----------
    ``resetToInitial()`` calls ``setPausedIndicator(false, undefined, true)``
    (``skipAnnounce=true``) so that hiding the paused badge does not fire
    the normal "Timer resumed" live-region update.  It then calls
    ``announce('Timer reset')`` separately.  Without the ``skipAnnounce``
    flag, resetting from a paused state would silently emit "Timer resumed"
    before "Timer reset", confusing screen reader users.

    These tests use the MutationObserver helper (``_install_announcer_observer``
    / ``_get_announcer_changes``) to capture every non-empty change on
    ``#phase-announcer``.  The main guard is:

        exactly 1 non-empty change and that change == "Timer reset"

    The pause → resume path is already covered by
    ``TestPauseResumeAnnouncementCount``, so only the reset scenarios are new
    here.
    """

    _SETTLE_MS = 200

    def test_reset_from_paused_announces_timer_reset_not_resumed(
        self, page, timer_html
    ):
        """
        Resetting from a **paused** state must fire exactly one announcement
        ("Timer reset") and must *not* fire "Timer resumed" first.

        If ``skipAnnounce`` were removed from the ``setPausedIndicator(false)``
        call inside ``resetToInitial()``, this test would catch two non-empty
        announcements: first "Timer resumed" then "Timer reset".
        """
        _load_timer(page, timer_html)

        page.locator(".timer-start").click()
        _advance(page, 100)
        page.locator(".timer-pause").click()
        _advance(page, self._SETTLE_MS)

        _install_announcer_observer(page)

        page.locator(".timer-reset").click()
        _advance(page, self._SETTLE_MS)

        changes = _get_announcer_changes(page)
        non_empty = [c for c in changes if c]

        assert non_empty, "Expected at least one announcement after reset, got none"
        assert len(non_empty) == 1, (
            f"Expected exactly 1 non-empty announcement after reset from paused, "
            f"got {len(non_empty)}: {non_empty}"
        )
        assert non_empty[0] == "Timer reset", (
            f"Expected 'Timer reset', got '{non_empty[0]}'. "
            "A stray 'Timer resumed' before 'Timer reset' would indicate "
            "the skipAnnounce guard is missing from resetToInitial()."
        )

    def test_reset_from_running_announces_timer_reset(self, page, timer_html):
        """
        Resetting from a **running** state must also fire exactly one
        announcement — "Timer reset".  This confirms the running-state
        reset path is equivalent to the paused-state path.
        """
        _load_timer(page, timer_html)

        page.locator(".timer-start").click()
        _advance(page, 500)

        _install_announcer_observer(page)

        page.locator(".timer-reset").click()
        _advance(page, self._SETTLE_MS)

        changes = _get_announcer_changes(page)
        non_empty = [c for c in changes if c]

        assert non_empty, "Expected at least one announcement after reset, got none"
        assert len(non_empty) == 1, (
            f"Expected exactly 1 announcement after reset from running, "
            f"got {len(non_empty)}: {non_empty}"
        )
        assert non_empty[0] == "Timer reset", (
            f"Expected 'Timer reset', got '{non_empty[0]}'"
        )

    def test_pause_then_reset_leaves_badge_hidden(self, page, timer_html):
        """
        After a pause → reset cycle the paused badge must be hidden, confirming
        the DOM is in a clean state and setPausedIndicator ran correctly.
        """
        _load_timer(page, timer_html)

        page.locator(".timer-start").click()
        _advance(page, 100)
        page.locator(".timer-pause").click()
        _advance(page, self._SETTLE_MS)
        page.locator(".timer-reset").click()
        _advance(page, self._SETTLE_MS)

        badge = page.locator(".timer-paused-badge")
        assert not badge.is_visible(), (
            "Paused badge should be hidden after resetting from paused state"
        )

    def test_pause_then_reset_restores_start_button(self, page, timer_html):
        """
        After a pause → reset cycle the Start button must read "Start" (not
        "Resume"), confirming the full state machine reset is correct.
        """
        _load_timer(page, timer_html)

        page.locator(".timer-start").click()
        _advance(page, 100)
        page.locator(".timer-pause").click()
        _advance(page, self._SETTLE_MS)
        page.locator(".timer-reset").click()
        _advance(page, self._SETTLE_MS)

        start_btn = page.locator(".timer-start")
        assert start_btn.inner_text() == "Start", (
            f"Expected Start button to read 'Start' after reset, "
            f"got '{start_btn.inner_text()}'"
        )
        assert not start_btn.is_disabled(), (
            "Start button should be enabled after reset"
        )


# ---------------------------------------------------------------------------
# Phase-transition announcement-count tests
# ---------------------------------------------------------------------------

class TestPhaseTransitionAnnouncementCount:
    """
    Verify that each phase transition causes ``#phase-announcer`` to emit
    exactly one non-empty announcement — "Now entering Phase N — <label>" —
    and that "All phases complete" fires exactly once when the last phase ends.

    Background
    ----------
    ``announce()`` always clears the live region first (``textContent = ''``)
    and then sets the message text after ``ANNOUNCE_DELAY_MS`` (50 ms).  That
    produces two DOM mutations per call, but only *one* non-empty mutation.
    If the announce path were accidentally called twice (e.g. from both the
    ``tick()`` loop and a sync-path re-entry) the observer would capture two
    non-empty changes and the test would fail.

    Test setup
    ----------
    1. Start the timer and advance past the previous phase boundary so the
       clock is firmly *inside* the phase before the one being tested.
    2. Install the MutationObserver (``_install_announcer_observer``).
    3. Advance ``TICK_MS`` (phase duration + 500 ms) so the clock crosses the
       next boundary and the ``ANNOUNCE_DELAY_MS`` setTimeout fires within the
       same ``run_for`` call.
    4. Filter captured changes to non-empty strings and assert exactly 1,
       with the expected message text.
    """

    def test_phase_1_to_2_fires_exactly_one_announcement(self, page, timer_html):
        """
        Crossing the phase 1 → 2 boundary must produce exactly one non-empty
        announcement: "Now entering Phase 2 — Beta".
        """
        _load_timer(page, timer_html)
        page.locator(".timer-start").click()
        _advance(page, 100)

        _install_announcer_observer(page)

        _advance(page, TICK_MS)

        changes = _get_announcer_changes(page)
        non_empty = [c for c in changes if c]

        assert len(non_empty) == 1, (
            f"Expected exactly 1 non-empty announcement on phase 1 → 2 transition, "
            f"got {len(non_empty)}: {non_empty}"
        )
        assert non_empty[0] == "Now entering Phase 2 \u2014 Beta", (
            f"Expected 'Now entering Phase 2 \u2014 Beta', got: '{non_empty[0]}'"
        )

    def test_phase_2_to_3_fires_exactly_one_announcement(self, page, timer_html):
        """
        Crossing the phase 2 → 3 boundary must produce exactly one non-empty
        announcement: "Now entering Phase 3 — Gamma".
        """
        _load_timer(page, timer_html)
        page.locator(".timer-start").click()
        _advance(page, TICK_MS)
        _advance(page, 100)

        _install_announcer_observer(page)

        _advance(page, TICK_MS)

        changes = _get_announcer_changes(page)
        non_empty = [c for c in changes if c]

        assert len(non_empty) == 1, (
            f"Expected exactly 1 non-empty announcement on phase 2 → 3 transition, "
            f"got {len(non_empty)}: {non_empty}"
        )
        assert non_empty[0] == "Now entering Phase 3 \u2014 Gamma", (
            f"Expected 'Now entering Phase 3 \u2014 Gamma', got: '{non_empty[0]}'"
        )

    def test_all_phases_complete_fires_exactly_one_announcement(
        self, page, timer_html
    ):
        """
        When the last phase expires, ``#phase-announcer`` must emit exactly one
        non-empty announcement: "All phases complete".
        """
        _load_timer(page, timer_html)
        page.locator(".timer-start").click()
        _advance(page, TICK_MS)
        _advance(page, TICK_MS)
        _advance(page, 100)

        _install_announcer_observer(page)

        _advance(page, TICK_MS)

        changes = _get_announcer_changes(page)
        non_empty = [c for c in changes if c]

        assert len(non_empty) == 1, (
            f"Expected exactly 1 non-empty announcement for 'All phases complete', "
            f"got {len(non_empty)}: {non_empty}"
        )
        assert non_empty[0] == "All phases complete", (
            f"Expected 'All phases complete', got: '{non_empty[0]}'"
        )


# ---------------------------------------------------------------------------
# Long-pause host-reminder tests
# ---------------------------------------------------------------------------

class TestLongPauseHostReminder:
    """
    Verify that the long-pause host reminder triggers at the right threshold.

    Background
    ----------
    ``updatePausedText()`` runs every second while the timer is paused.
    When ``IS_HOST`` is ``true`` and ``elapsedSec >= PAUSE_REMINDER_THRESHOLD_SEC``
    (300 s), it:
      - Adds the ``long-paused`` CSS class to ``.timer-paused-badge``
      - Replaces the badge text with "▮▮ Still paused — X min"

    When ``IS_HOST`` is ``false``, the reminder never fires regardless of
    how long the pause has lasted: the badge always shows the neutral
    "▮▮ Paused · X min" text without the ``long-paused`` class.

    Test setup
    ----------
    ``host_timer_html``    — phase timer rendered with ``is_host=True``
    ``timer_html``         — phase timer rendered without ``is_host`` (defaults false)

    Both fixtures use the same fake-clock trick: pause the timer at time T,
    then advance 300 000 ms (5 minutes) so ``updatePausedText`` fires and
    ``elapsedSec`` reaches the threshold exactly.
    """

    _THRESHOLD_MS = 300_000
    _BELOW_THRESHOLD_MS = 60_000
    _SETTLE_MS = 200

    def _pause_and_advance(self, page, html: str, advance_ms: int) -> None:
        """Load html, start the timer, pause it, then advance the clock."""
        _load_timer(page, html)
        page.locator(".timer-start").click()
        _advance(page, 100)
        page.locator(".timer-pause").click()
        _advance(page, advance_ms)

    def test_host_long_paused_class_appears_at_threshold(
        self, page, host_timer_html
    ):
        """
        Host view: after 5 minutes the ``.timer-paused-badge`` must carry
        the ``long-paused`` CSS class so the amber reminder styling appears.
        """
        self._pause_and_advance(page, host_timer_html, self._THRESHOLD_MS)

        has_class = page.locator(".timer-paused-badge.long-paused").count() > 0
        assert has_class, (
            "Expected .timer-paused-badge to have 'long-paused' class after "
            f"{self._THRESHOLD_MS // 1000} s for host view"
        )

    def test_host_still_paused_text_at_threshold(
        self, page, host_timer_html
    ):
        """
        Host view: badge text must read "Still paused" (not "Paused ·") after
        the threshold, giving the host a clear nudge to resume.
        """
        self._pause_and_advance(page, host_timer_html, self._THRESHOLD_MS)

        text = page.locator(".timer-paused-badge").inner_text()
        assert "Still paused" in text, (
            f"Expected 'Still paused' in host badge text at threshold, got: '{text}'"
        )
        assert "Paused \u00b7" not in text, (
            f"Badge should not show 'Paused ·' (neutral) in host view at threshold, got: '{text}'"
        )

    def test_participant_no_long_paused_class_at_threshold(
        self, page, timer_html
    ):
        """
        Participant view (``IS_HOST = false``): after 5 minutes the badge must
        *not* gain the ``long-paused`` class — only the host gets the reminder.
        """
        self._pause_and_advance(page, timer_html, self._THRESHOLD_MS)

        has_class = page.locator(".timer-paused-badge.long-paused").count() > 0
        assert not has_class, (
            "Participant view must not show 'long-paused' class after "
            f"{self._THRESHOLD_MS // 1000} s — reminder is host-only"
        )

    def test_participant_shows_neutral_paused_text_at_threshold(
        self, page, timer_html
    ):
        """
        Participant view: badge text must stay neutral ("Paused · 5 min")
        rather than switching to the host reminder ("Still paused — 5 min").
        """
        self._pause_and_advance(page, timer_html, self._THRESHOLD_MS)

        text = page.locator(".timer-paused-badge").inner_text()
        assert "Still paused" not in text, (
            f"Participant badge must not show 'Still paused', got: '{text}'"
        )
        assert "Paused" in text, (
            f"Participant badge should still show 'Paused', got: '{text}'"
        )

    def test_host_long_paused_clears_on_resume(
        self, page, host_timer_html
    ):
        """
        Host view: after the long-pause reminder appears, resuming the timer
        must remove the ``long-paused`` class *and* hide the badge entirely.
        """
        self._pause_and_advance(page, host_timer_html, self._THRESHOLD_MS)

        has_class = page.locator(".timer-paused-badge.long-paused").count() > 0
        assert has_class, (
            "Prerequisite: .timer-paused-badge should have 'long-paused' class "
            "before resume so this test is meaningful"
        )

        page.locator(".timer-start").click()
        _advance(page, self._SETTLE_MS)

        has_long_paused = page.locator(".timer-paused-badge.long-paused").count() > 0
        assert not has_long_paused, (
            "After resume, 'long-paused' class must be removed from .timer-paused-badge"
        )

        badge_hidden = page.locator(".timer-paused-badge").get_attribute("hidden") is not None
        assert badge_hidden, (
            "After resume, the .timer-paused-badge must be hidden (hidden attribute present)"
        )

    def test_host_no_long_paused_class_before_threshold(
        self, page, host_timer_html
    ):
        """
        Host view: only 1 minute elapsed — ``long-paused`` class must *not*
        appear because the threshold (5 min) has not been reached yet.
        """
        self._pause_and_advance(page, host_timer_html, self._BELOW_THRESHOLD_MS)

        has_class = page.locator(".timer-paused-badge.long-paused").count() > 0
        assert not has_class, (
            "Host badge should not show 'long-paused' class before the "
            f"{self._THRESHOLD_MS // 1000}-s threshold "
            f"(only {self._BELOW_THRESHOLD_MS // 1000} s elapsed)"
        )

    def test_custom_threshold_120_triggers_long_paused(
        self, page, host_timer_html_threshold_120
    ):
        """
        When ``PAUSE_REMINDER_THRESHOLD_SEC`` is set to 120, the host badge
        must gain the ``long-paused`` class after exactly 120 s of pause time,
        not the default 300 s.
        """
        self._pause_and_advance(page, host_timer_html_threshold_120, 120_000)

        has_class = page.locator(".timer-paused-badge.long-paused").count() > 0
        assert has_class, (
            "Expected .timer-paused-badge to have 'long-paused' class after "
            "120 s when PAUSE_REMINDER_THRESHOLD_SEC = 120"
        )

    def test_custom_threshold_120_does_not_trigger_before_threshold(
        self, page, host_timer_html_threshold_120
    ):
        """
        With a 120 s threshold, only 60 s elapsed — ``long-paused`` must
        *not* appear yet.
        """
        self._pause_and_advance(page, host_timer_html_threshold_120, 60_000)

        has_class = page.locator(".timer-paused-badge.long-paused").count() > 0
        assert not has_class, (
            "Host badge should not show 'long-paused' class after only 60 s "
            "when PAUSE_REMINDER_THRESHOLD_SEC = 120"
        )

    def test_null_threshold_never_shows_long_paused(
        self, page, host_timer_html_threshold_null
    ):
        """
        When ``PAUSE_REMINDER_THRESHOLD_SEC`` is ``null`` (disabled), the
        host badge must *never* gain the ``long-paused`` class, even after a
        very long pause (600 s — well past the default 300 s threshold).
        """
        self._pause_and_advance(page, host_timer_html_threshold_null, 600_000)

        has_class = page.locator(".timer-paused-badge.long-paused").count() > 0
        assert not has_class, (
            "Host badge must not show 'long-paused' class when "
            "PAUSE_REMINDER_THRESHOLD_SEC = null (reminder disabled), "
            "even after 600 s of pause time"
        )


# ---------------------------------------------------------------------------
# Simple-timer reset-announcement tests
# ---------------------------------------------------------------------------

class TestTimerDisplayAriaLabelBrowser:
    """
    Browser-level verification that the timer-display element's
    role="timer" and aria-label="Time remaining" attributes are present in
    the live DOM and do not introduce WCAG 2 AA violations detected by axe-core.

    Rationale
    ---------
    The static tests in test_timer_a11y.py confirm that role="timer" and
    aria-label="Time remaining" appear in the rendered HTML, but they cannot
    catch ARIA conflicts that only surface at runtime (e.g. an unexpected
    aria-live on the same element, or a hidden parent that masks the label).
    These tests exercise the same attributes in a real Chromium browser with
    axe-core injected, closing that gap.

    Both the phase-timer (``timer_html``) and the simple countdown
    (``simple_timer_html``) are tested because ``timer-display`` is rendered
    in both modes.
    """

    def test_phase_timer_display_has_role_timer_in_browser(self, page, timer_html):
        """The timer-display element must carry role='timer' in the live DOM."""
        _load_timer(page, timer_html)
        role = page.locator(".timer-display").get_attribute("role")
        assert role == "timer", (
            f"Expected role='timer' on .timer-display, got: '{role}'"
        )

    def test_phase_timer_display_has_aria_label_in_browser(self, page, timer_html):
        """The timer-display element must carry aria-label='Time remaining' in the live DOM."""
        _load_timer(page, timer_html)
        label = page.locator(".timer-display").get_attribute("aria-label")
        assert label == "Time remaining", (
            f"Expected aria-label='Time remaining' on .timer-display, got: '{label}'"
        )

    def test_simple_timer_display_has_role_timer_in_browser(self, page, simple_timer_html):
        """Simple-timer mode: timer-display must carry role='timer' in the live DOM."""
        _load_timer(page, simple_timer_html)
        role = page.locator(".timer-display").get_attribute("role")
        assert role == "timer", (
            f"Expected role='timer' on .timer-display (simple mode), got: '{role}'"
        )

    def test_simple_timer_display_has_aria_label_in_browser(self, page, simple_timer_html):
        """Simple-timer mode: timer-display must carry aria-label='Time remaining' in the live DOM."""
        _load_timer(page, simple_timer_html)
        label = page.locator(".timer-display").get_attribute("aria-label")
        assert label == "Time remaining", (
            f"Expected aria-label='Time remaining' on .timer-display (simple mode), got: '{label}'"
        )

    def test_phase_timer_display_aria_label_no_axe_violations_initial(self, page, timer_html):
        """
        axe-core must report no WCAG 2 AA violations for the timer widget at
        rest — confirming role='timer' / aria-label='Time remaining' do not
        conflict with any other ARIA attributes on the element or its parents.
        """
        _load_timer(page, timer_html)
        results = _run_axe(page)
        _assert_no_violations(results, "phase timer — initial state (role=timer aria-label check)")

    def test_phase_timer_display_aria_label_no_axe_violations_running(self, page, timer_html):
        """
        axe-core must pass while the timer is actively counting down — the
        textContent of .timer-display changes every second, so this confirms
        that the dynamic updates do not invalidate the ARIA attributes.
        """
        _load_timer(page, timer_html)
        page.locator(".timer-start").click()
        _advance(page, 500)
        results = _run_axe(page)
        _assert_no_violations(results, "phase timer — running (role=timer aria-label check)")

    def test_simple_timer_display_aria_label_no_axe_violations_initial(self, page, simple_timer_html):
        """
        axe-core must report no violations for the simple-timer widget at rest,
        confirming role='timer' / aria-label='Time remaining' are valid in the
        no-phases rendering path as well.
        """
        _load_timer(page, simple_timer_html)
        results = _run_axe(page)
        _assert_no_violations(results, "simple timer — initial state (role=timer aria-label check)")

    def test_simple_timer_display_aria_label_no_axe_violations_running(self, page, simple_timer_html):
        """
        axe-core must pass while the simple timer is counting down, confirming
        the attributes remain valid during live textContent updates.
        """
        _load_timer(page, simple_timer_html)
        page.locator(".timer-start").click()
        _advance(page, 500)
        results = _run_axe(page)
        _assert_no_violations(results, "simple timer — running (role=timer aria-label check)")

    def test_timer_display_has_no_aria_live_in_browser(self, page, timer_html):
        """
        The timer-display element must NOT carry aria-live in the live DOM.
        Announcements are routed through #phase-announcer; an aria-live on the
        display itself would cause every second-tick textContent update to be
        announced by the screen reader, flooding the AT queue.
        """
        _load_timer(page, timer_html)
        aria_live = page.locator(".timer-display").get_attribute("aria-live")
        assert aria_live is None, (
            "timer-display must not have aria-live — every-second tick updates "
            f"would flood the screen-reader queue; got aria-live='{aria_live}'"
        )


class TestSimpleTimerResetAnnouncement:
    """
    Verify that resetting the **simple timer** (``timer_seconds`` only, no
    phases) announces "Timer reset" — and never "Timer resumed" — after a
    start → pause → reset cycle.

    Background
    ----------
    The simple timer has its own ``resetToInitial()`` function (separate from
    the phase-timer variant) that calls ``setPausedIndicator(false, undefined,
    true)`` (``skipAnnounce=true``) before calling ``announce('Timer reset')``.
    Without the ``skipAnnounce`` guard the hidden paused-badge dismissal would
    fire an extra "Timer resumed" announcement, confusing screen reader users.

    These tests use the ``simple_timer_html`` fixture (60-second countdown,
    no phases) and the same MutationObserver pattern as
    ``TestResetAnnouncementAccuracy``.
    """

    _SETTLE_MS = 200

    def test_simple_timer_reset_announces_timer_reset_not_resumed(
        self, page, simple_timer_html
    ):
        """
        After start → pause → reset the simple timer must emit exactly one
        non-empty announcement ("Timer reset") and must *not* emit "Timer
        resumed".

        If the ``skipAnnounce`` guard were removed from the simple-timer
        ``resetToInitial()``, the observer would capture two non-empty changes:
        "Timer resumed" followed by "Timer reset".
        """
        _load_timer(page, simple_timer_html)

        page.locator(".timer-start").click()
        _advance(page, 100)
        page.locator(".timer-pause").click()
        _advance(page, self._SETTLE_MS)

        _install_announcer_observer(page)

        page.locator(".timer-reset").click()
        _advance(page, self._SETTLE_MS)

        changes = _get_announcer_changes(page)
        non_empty = [c for c in changes if c]

        assert non_empty, (
            "Expected at least one announcement after simple-timer reset, got none"
        )
        assert len(non_empty) == 1, (
            f"Expected exactly 1 non-empty announcement after simple-timer reset, "
            f"got {len(non_empty)}: {non_empty}"
        )
        assert non_empty[0] == "Timer reset", (
            f"Expected 'Timer reset', got '{non_empty[0]}'. "
            "A stray 'Timer resumed' before 'Timer reset' would indicate the "
            "skipAnnounce guard is missing from the simple-timer resetToInitial()."
        )
        assert "Timer resumed" not in non_empty, (
            f"'Timer resumed' must not appear in announcements after reset; "
            f"got: {non_empty}"
        )

    def test_simple_timer_reset_leaves_badge_hidden(
        self, page, simple_timer_html
    ):
        """
        After a pause → reset cycle on the simple timer the paused badge must
        be hidden, confirming ``setPausedIndicator`` ran and the DOM is clean.
        """
        _load_timer(page, simple_timer_html)

        page.locator(".timer-start").click()
        _advance(page, 100)
        page.locator(".timer-pause").click()
        _advance(page, self._SETTLE_MS)
        page.locator(".timer-reset").click()
        _advance(page, self._SETTLE_MS)

        badge = page.locator(".timer-paused-badge")
        assert not badge.is_visible(), (
            "Paused badge should be hidden after resetting the simple timer from "
            "a paused state"
        )

    def test_simple_timer_reset_restores_start_button(
        self, page, simple_timer_html
    ):
        """
        After a pause → reset cycle on the simple timer the Start button must
        read "Start" (not "Resume") and be enabled, confirming full state reset.
        """
        _load_timer(page, simple_timer_html)

        page.locator(".timer-start").click()
        _advance(page, 100)
        page.locator(".timer-pause").click()
        _advance(page, self._SETTLE_MS)
        page.locator(".timer-reset").click()
        _advance(page, self._SETTLE_MS)

        start_btn = page.locator(".timer-start")
        assert start_btn.inner_text() == "Start", (
            f"Expected Start button to read 'Start' after simple-timer reset, "
            f"got '{start_btn.inner_text()}'"
        )
        assert not start_btn.is_disabled(), (
            "Start button should be enabled after simple-timer reset"
        )
