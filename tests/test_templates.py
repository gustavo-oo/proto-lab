"""Static-template checks for the proto-lab assets (Task 12).

The three templates in ``assets/`` are copied by the scaffolder (Task 14) and
filled by the variant generator (SKILL.md). They must open straight from
``file://`` with no build step and no cross-frame scripting, so this suite pins
the constraints that make that true:

- each file exists and carries its own ``{{PLACEHOLDER}}`` tokens;
- no external ``<script src=``; at most one inline ``<script>`` block of at
  most 30 lines, and the cap is evaluated **per file** (ruling R9);
- every ``<iframe`` is ``loading="lazy"`` with a relative ``src`` (no leading
  ``/`` and no scheme);
- no ``http`` URL outside the two allow-listed font hosts;
- no cross-frame scripting (``contentWindow`` / ``postMessage`` /
  ``contentDocument``);
- ``canvas.html`` shows three frames labelled ``A`` / ``B`` / ``C``;
- ``variant-shell.html`` carries a ``<nav>`` of relative links plus the
  ``<!-- screens -->`` marker.

Python stdlib only.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

GALLERY = ASSETS / "gallery.html"
CANVAS = ASSETS / "canvas.html"
VARIANT_SHELL = ASSETS / "variant-shell.html"

TEMPLATES = (GALLERY, CANVAS, VARIANT_SHELL)

# The placeholders each template must expose, and the closed set of every
# placeholder the templates may use (the interface Task 14/T16 bind to).
REQUIRED_PLACEHOLDERS = {
    "gallery.html": (
        "{{SEED}}",
        "{{DIRECTION_NAME}}",
        "{{FAMILY}}",
        "{{POINTS_TABLE_ROWS}}",
    ),
    "canvas.html": ("{{CANVAS_TITLE}}", "{{CANVAS_FRAMES}}"),
    "variant-shell.html": ("{{VARIANT_LABEL}}",),
}

ALL_PLACEHOLDERS = frozenset(
    placeholder
    for placeholders in REQUIRED_PLACEHOLDERS.values()
    for placeholder in placeholders
)

ALLOWED_URL_PREFIXES = (
    "https://fonts.googleapis.com",
    "https://fonts.gstatic.com",
)

INLINE_SCRIPT_LINE_CAP = 30
INLINE_SCRIPT_BLOCK_CAP = 1

# Cross-frame access tokens: a display-only, ``file://``-safe page never uses
# any of these.
FORBIDDEN_CROSS_FRAME_TOKENS = ("contentWindow", "postMessage", "contentDocument")

PLACEHOLDER_RE = re.compile(r"\{\{([A-Z_]+)\}\}")
EXTERNAL_SCRIPT_RE = re.compile(r"<script\b[^>]*\bsrc\s*=", re.IGNORECASE)
INLINE_SCRIPT_RE = re.compile(
    r"<script\b(?![^>]*\bsrc\s*=)[^>]*>(.*?)</script\s*>",
    re.IGNORECASE | re.DOTALL,
)
IFRAME_RE = re.compile(r"<iframe\b[^>]*>", re.IGNORECASE)
SRC_RE = re.compile(r'\bsrc\s*=\s*"([^"]*)"', re.IGNORECASE)
LAZY_RE = re.compile(r'\bloading\s*=\s*"lazy"', re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s\"'<>()]+", re.IGNORECASE)
FRAME_LETTER_RE = re.compile(r'class="frame__letter">([A-Z])<')
FRAME_VARIANT_RE = re.compile(r'data-variant="([a-z])"')
NAV_RE = re.compile(r"<nav\b[^>]*>(.*?)</nav>", re.IGNORECASE | re.DOTALL)
HREF_RE = re.compile(r'href\s*=\s*"([^"]+)"', re.IGNORECASE)


class TemplateTest(unittest.TestCase):
    """Shared helpers."""

    def read(self, path):
        self.assertTrue(path.is_file(), "missing template: %s" % path)
        return path.read_text(encoding="utf-8")

    def each_template(self):
        for path in TEMPLATES:
            yield path, self.read(path)


class TemplateExistenceTest(TemplateTest):
    def test_every_template_exists(self):
        missing = sorted(path.name for path in TEMPLATES if not path.is_file())
        self.assertEqual(missing, [], "missing templates: %s" % ", ".join(missing))

    def test_every_template_is_html(self):
        for path, html in self.each_template():
            self.assertIn("<!DOCTYPE html>", html, path.name)
            self.assertIn("</html>", html, path.name)


class PlaceholderContractTest(TemplateTest):
    def test_templates_carry_their_required_placeholders(self):
        for name, required in REQUIRED_PLACEHOLDERS.items():
            html = self.read(ASSETS / name)
            for placeholder in required:
                self.assertIn(placeholder, html, "%s misses %s" % (name, placeholder))

    def test_no_placeholder_outside_the_closed_set(self):
        for path, html in self.each_template():
            found = {"{{%s}}" % token for token in PLACEHOLDER_RE.findall(html)}
            unknown = sorted(found - ALL_PLACEHOLDERS)
            self.assertEqual(unknown, [], "%s has unknown placeholders" % path.name)

    def test_every_placeholder_appears_somewhere(self):
        seen = set()
        for _, html in self.each_template():
            seen |= {"{{%s}}" % token for token in PLACEHOLDER_RE.findall(html)}
        self.assertEqual(sorted(ALL_PLACEHOLDERS - seen), [])


class ScriptBudgetTest(TemplateTest):
    def test_no_external_script_src(self):
        for path, html in self.each_template():
            self.assertNotRegex(
                html, EXTERNAL_SCRIPT_RE, "%s loads an external script" % path.name
            )

    def test_inline_script_budget_is_per_file(self):
        for path, html in self.each_template():
            blocks = INLINE_SCRIPT_RE.findall(html)
            self.assertLessEqual(
                len(blocks),
                INLINE_SCRIPT_BLOCK_CAP,
                "%s has %d inline <script> blocks" % (path.name, len(blocks)),
            )
            lines = sum(len(block.strip("\n").splitlines()) for block in blocks)
            self.assertLessEqual(
                lines,
                INLINE_SCRIPT_LINE_CAP,
                "%s has %d inline <script> lines" % (path.name, lines),
            )


class FileUrlSafetyTest(TemplateTest):
    def test_iframes_are_lazy_and_relative(self):
        for path, html in self.each_template():
            frames = IFRAME_RE.findall(html)
            for tag in frames:
                self.assertRegex(
                    tag, LAZY_RE, "%s has an <iframe> without loading=\"lazy\"" % path.name
                )
                src_match = SRC_RE.search(tag)
                self.assertIsNotNone(src_match, "%s has an <iframe> with no src" % path.name)
                src = src_match.group(1)
                self.assertNotIn("://", src, "%s iframe src is absolute: %r" % (path.name, src))
                self.assertFalse(
                    src.startswith("/"),
                    "%s iframe src is root-absolute: %r" % (path.name, src),
                )
                self.assertTrue(src, "%s has an empty iframe src" % path.name)

    def test_canvas_has_iframes(self):
        self.assertTrue(
            IFRAME_RE.findall(self.read(CANVAS)),
            "canvas.html must embed its variant frames",
        )

    def test_only_allowlisted_http_urls(self):
        for path, html in self.each_template():
            for url in URL_RE.findall(html):
                self.assertTrue(
                    url.startswith(ALLOWED_URL_PREFIXES),
                    "%s references a non-allowlisted URL: %s" % (path.name, url),
                )

    def test_no_cross_frame_scripting(self):
        for path, html in self.each_template():
            for token in FORBIDDEN_CROSS_FRAME_TOKENS:
                self.assertNotIn(
                    token, html, "%s uses cross-frame token %r" % (path.name, token)
                )


class CanvasFramesTest(TemplateTest):
    def test_canvas_shows_three_frames_labelled_a_b_c(self):
        html = self.read(CANVAS)
        self.assertEqual(
            len(IFRAME_RE.findall(html)), 3, "canvas.html must show exactly 3 frames"
        )
        self.assertEqual(
            sorted(FRAME_LETTER_RE.findall(html)), ["A", "B", "C"]
        )
        self.assertEqual(
            sorted(FRAME_VARIANT_RE.findall(html)), ["a", "b", "c"]
        )

    def test_canvas_exposes_the_frames_placeholder(self):
        self.assertIn("{{CANVAS_FRAMES}}", self.read(CANVAS))


class VariantShellTest(TemplateTest):
    def test_variant_shell_has_relative_nav_and_screens_marker(self):
        html = self.read(VARIANT_SHELL)
        nav_match = NAV_RE.search(html)
        self.assertIsNotNone(nav_match, "variant-shell.html must carry a <nav>")
        hrefs = HREF_RE.findall(nav_match.group(1))
        self.assertGreaterEqual(len(hrefs), 2, "the nav must link its screens")
        for href in hrefs:
            self.assertNotIn("://", href, "nav href is absolute: %r" % href)
            self.assertFalse(href.startswith("/"), "nav href is root-absolute: %r" % href)
            self.assertFalse(href.startswith("#"), "nav href is a bare fragment: %r" % href)
        self.assertTrue(
            any(href.endswith(".html") for href in hrefs),
            "the nav must link sibling screens",
        )
        self.assertIn("<!-- screens -->", html)

    def test_variant_shell_exposes_the_label_placeholder(self):
        self.assertIn("{{VARIANT_LABEL}}", self.read(VARIANT_SHELL))


if __name__ == "__main__":
    unittest.main()
