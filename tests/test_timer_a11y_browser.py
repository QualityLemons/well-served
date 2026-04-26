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
`announce()` function defers textContent updates via `requestAnimationFrame`.
`run_for` fires both timer callbacks *and* rAF callbacks, so the live region
is always up to date when the assertion runs.
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
        After the final phase expires:
          - All but the last segment must carry '— completed' in their aria-label.
          - The last segment is 'active' (the JS marks it active because
            phaseIdx == lastPhaseIndex, even though remaining == 0).

        This test documents the current rendering behaviour and will catch any
        unintended regression that leaves earlier segments in an incorrect state.
        """
        _load_timer(page, timer_html)
        page.locator(".timer-start").click()
        _advance(page, TICK_MS)
        _advance(page, TICK_MS)
        _advance(page, TICK_MS)

        segments = page.locator(".phase-segment").all()
        assert len(segments) == 3

        for i in range(len(segments) - 1):
            label = segments[i].get_attribute("aria-label") or ""
            assert "completed" in label, (
                f"Segment {i} should be completed after all phases end, got: '{label}'"
            )

        last_label = segments[-1].get_attribute("aria-label") or ""
        assert "active" in last_label or "completed" in last_label, (
            f"Last segment should be active or completed after timer ends, got: '{last_label}'"
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
