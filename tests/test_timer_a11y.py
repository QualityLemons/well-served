"""
Accessibility tests for the phase timer widget (templates/tools/_timer.html).

Covers:
- Static ARIA attributes on specific elements in the rendered HTML
- JavaScript source contains correct aria-label values and live-region patterns
- WCAG AA colour-contrast ratios parsed directly from the template CSS
"""

import re
from html.parser import HTMLParser
from types import SimpleNamespace

from django.test import TestCase
from django.template.loader import render_to_string

SAMPLE_PHASES = [
    {"label": "Introduction", "seconds": 300},
    {"label": "Discussion", "seconds": 600},
    {"label": "Wrap-up", "seconds": 120},
]

WCAG_AA_RATIO = 4.5


def _tool_meta(phases=SAMPLE_PHASES, timer_seconds=1020):
    return SimpleNamespace(phases=phases, timer_seconds=timer_seconds)


def _render(extra_context=None):
    context = {"tool_meta": _tool_meta(), "timer_session_id": None}
    if extra_context:
        context.update(extra_context)
    return render_to_string("tools/_timer.html", context)


# ---------------------------------------------------------------------------
# HTML parsing helpers
# ---------------------------------------------------------------------------

class _ElementCollector(HTMLParser):
    """Minimal HTML parser that collects every start tag and its attributes."""

    def __init__(self):
        super().__init__()
        self._elements = []

    def handle_starttag(self, tag, attrs):
        self._elements.append({"tag": tag, "attrs": dict(attrs)})

    def find_all(self, tag=None, **attr_conditions):
        results = []
        for el in self._elements:
            if tag and el["tag"] != tag:
                continue
            if all(el["attrs"].get(k) == v for k, v in attr_conditions.items()):
                results.append(el)
        return results

    def find_one(self, tag=None, **attr_conditions):
        matches = self.find_all(tag=tag, **attr_conditions)
        return matches[0] if matches else None


def _parse_html(html):
    collector = _ElementCollector()
    collector.feed(html)
    return collector


# ---------------------------------------------------------------------------
# CSS parsing helpers
# ---------------------------------------------------------------------------

def _parse_style_block(html):
    """
    Extract CSS rules from the first <style> block.
    Returns a dict: selector -> {'color': '#rrggbb', 'background': '#rrggbb'}
    Only hex colours are captured.
    """
    style_match = re.search(r"<style>(.*?)</style>", html, re.DOTALL)
    if not style_match:
        return {}
    css = style_match.group(1)
    rules = {}
    for rule_match in re.finditer(r"([^{}\n][^{]*?)\s*\{([^}]*)\}", css, re.DOTALL):
        selector = rule_match.group(1).strip()
        props = rule_match.group(2)
        entry = {}
        fg = re.search(r"(?<![a-z-])color:\s*(#[0-9a-fA-F]{6})", props)
        bg = re.search(r"background(?:-color)?:\s*(#[0-9a-fA-F]{6})", props)
        if fg:
            entry["color"] = fg.group(1).lower()
        if bg:
            entry["background"] = bg.group(1).lower()
        if entry:
            rules[selector] = entry
    return rules


# ---------------------------------------------------------------------------
# Contrast maths
# ---------------------------------------------------------------------------

def _hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i: i + 2], 16) for i in (0, 2, 4))


def _relative_luminance(r, g, b):
    def channel(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def _contrast_ratio(fg_hex, bg_hex):
    l1 = _relative_luminance(*_hex_to_rgb(fg_hex))
    l2 = _relative_luminance(*_hex_to_rgb(bg_hex))
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


# ---------------------------------------------------------------------------
# Static HTML / ARIA attribute tests
# ---------------------------------------------------------------------------

class TimerWidgetStaticHTMLTests(TestCase):
    """Rendered HTML must carry required ARIA attributes on the correct elements."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.html = _render()
        cls.dom = _parse_html(cls.html)

    def test_phase_progress_bar_has_group_role(self):
        bar = self.dom.find_one(tag="div", **{"class": "phase-progress-bar", "role": "group"})
        self.assertIsNotNone(bar, "phase-progress-bar div must have role='group'")

    def test_phase_progress_bar_has_aria_label(self):
        bar = self.dom.find_one(tag="div", **{"class": "phase-progress-bar", "role": "group"})
        self.assertIsNotNone(bar)
        self.assertEqual(
            bar["attrs"].get("aria-label"),
            "Session phase progress",
            "phase-progress-bar must have aria-label='Session phase progress'",
        )

    def test_live_announcer_element_present(self):
        announcer = self.dom.find_one(tag="div", id="phase-announcer")
        self.assertIsNotNone(announcer, "div#phase-announcer must exist")

    def test_live_announcer_is_assertive(self):
        announcer = self.dom.find_one(tag="div", id="phase-announcer")
        self.assertIsNotNone(announcer)
        self.assertEqual(
            announcer["attrs"].get("aria-live"),
            "assertive",
            "phase-announcer must have aria-live='assertive'",
        )

    def test_live_announcer_is_atomic(self):
        announcer = self.dom.find_one(tag="div", id="phase-announcer")
        self.assertIsNotNone(announcer)
        self.assertEqual(
            announcer["attrs"].get("aria-atomic"),
            "true",
            "phase-announcer must have aria-atomic='true'",
        )

    def test_live_announcer_uses_sr_only_class(self):
        announcer = self.dom.find_one(tag="div", id="phase-announcer")
        self.assertIsNotNone(announcer)
        classes = (announcer["attrs"].get("class") or "").split()
        self.assertIn("sr-only", classes, "phase-announcer must have class 'sr-only'")

    def test_paused_badge_has_aria_live_polite(self):
        badge = self.dom.find_one(tag="div", **{"class": "timer-paused-badge"})
        self.assertIsNotNone(badge, "timer-paused-badge div must exist")
        self.assertEqual(
            badge["attrs"].get("aria-live"),
            "polite",
            "timer-paused-badge must have aria-live='polite'",
        )

    def test_sr_only_css_rule_hides_visually(self):
        css = self.html
        self.assertIn(".sr-only", css)
        self.assertIn("position: absolute", css)
        self.assertIn("clip: rect(0,0,0,0)", css)

    def test_timer_renders_when_no_phases(self):
        context = {
            "tool_meta": SimpleNamespace(phases=None, timer_seconds=300),
            "timer_session_id": None,
        }
        html = render_to_string("tools/_timer.html", context)
        dom = _parse_html(html)
        self.assertIsNotNone(
            dom.find_one(tag="div", **{"class": "timer-display"}),
            "timer-display must render in the no-phases (simple countdown) mode",
        )


# ---------------------------------------------------------------------------
# JavaScript source pattern tests
# ---------------------------------------------------------------------------

class TimerWidgetJavaScriptTests(TestCase):
    """
    The JS embedded in the template must contain the strings that drive
    dynamic aria-label updates and live-region announcements.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.html = _render()

    def test_js_sets_aria_label_upcoming_on_segments(self):
        self.assertIn("\u2014 upcoming", self.html)

    def test_js_sets_aria_label_active_on_segments(self):
        self.assertIn("\u2014 active", self.html)

    def test_js_sets_aria_label_completed_on_segments(self):
        self.assertIn("\u2014 completed", self.html)

    def test_js_assigns_role_img_to_segments(self):
        self.assertIn("'img'", self.html)

    def test_js_announces_phase_transitions(self):
        self.assertIn("Now entering Phase", self.html)

    def test_js_announces_all_phases_complete(self):
        self.assertIn("All phases complete", self.html)

    def test_js_references_phase_announcer_element(self):
        self.assertIn("phase-announcer", self.html)

    def test_js_clears_announcer_before_updating(self):
        self.assertIn("announcer.textContent = ''", self.html)

    def test_js_uses_requestAnimationFrame_for_announcement(self):
        self.assertIn("requestAnimationFrame", self.html)

    def test_js_sets_aria_label_in_renderProgressBar(self):
        self.assertIn("setAttribute('aria-label'", self.html)


# ---------------------------------------------------------------------------
# CSS colour-contrast tests (WCAG AA >= 4.5:1) — sourced from the template
# ---------------------------------------------------------------------------

class TimerCSSContrastTests(TestCase):
    """
    Parse colour values directly from the rendered template CSS and verify
    WCAG AA contrast.  Tests fail if the template CSS is changed to a
    low-contrast colour, catching regressions automatically.

    Effective backgrounds:
      Most text lives on the widget surface: .timer-widget background
      The paused badge has its own background: .timer-paused-badge background
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.rules = _parse_style_block(_render())
        cls.widget_bg = cls.rules.get(".timer-widget", {}).get("background")
        cls.badge_bg = cls.rules.get(".timer-paused-badge", {}).get("background")

    def _assert_contrast(self, fg, bg, label):
        self.assertIsNotNone(fg, f"Could not parse foreground color for {label} from template CSS")
        self.assertIsNotNone(bg, f"Could not parse background color for {label} from template CSS")
        ratio = _contrast_ratio(fg, bg)
        self.assertGreaterEqual(
            ratio,
            WCAG_AA_RATIO,
            f"WCAG AA failure — {label}: {fg} on {bg} gives {ratio:.2f}:1 "
            f"(need >= {WCAG_AA_RATIO}:1)",
        )

    def test_timer_display_normal_state_contrast(self):
        fg = self.rules.get(".timer-display", {}).get("color")
        self._assert_contrast(fg, self.widget_bg, "timer-display (normal state)")

    def test_timer_display_warning_state_contrast(self):
        fg = self.rules.get(".timer-display.warning", {}).get("color")
        self._assert_contrast(fg, self.widget_bg, "timer-display.warning")

    def test_timer_display_expired_state_contrast(self):
        fg = self.rules.get(".timer-display.expired", {}).get("color")
        self._assert_contrast(fg, self.widget_bg, "timer-display.expired")

    def test_phase_label_contrast(self):
        fg = self.rules.get(".timer-phase-label", {}).get("color")
        self._assert_contrast(fg, self.widget_bg, "timer-phase-label")

    def test_phase_progress_text_contrast(self):
        fg = self.rules.get(".timer-phase-progress", {}).get("color")
        self._assert_contrast(fg, self.widget_bg, "timer-phase-progress")

    def test_paused_badge_text_contrast(self):
        fg = self.rules.get(".timer-paused-badge", {}).get("color")
        self._assert_contrast(fg, self.badge_bg, "timer-paused-badge text")
