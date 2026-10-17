#!/usr/bin/env python3
"""Mechanical AI-slop scan for the proto-lab pipeline (layer 3).

A deterministic port of rules ``R01``-``R22`` in
``references/slop-fingerprints.md``. The scanner reads static HTML files and
records one :data:`Finding` per matching fingerprint; a page with **4 or more**
hits fails (``THRESHOLD``), three or fewer passes.

The four judge-only fingerprints (F16, F18, F21, F22) have no rule here by
design; they are decided by the judge (T16) on the rendered artifact.

Design notes
------------
* Every matcher is a regex or ``html.parser`` check over a whitespace-normalised
  copy of the document, so the scan is independent of formatting.
* Each entry of :data:`RULES` is ``(rule_id, fingerprint, confidence, matcher)``
  where ``matcher(ctx)`` returns an evidence string on a hit or ``None``.
* ``confidence`` is ``solid`` for deterministic matches and ``heuristic`` for
  patterns a direction may legitimately earn (per the spec's "Kind" column).

Python stdlib only; Python >= 3.8.
"""

import argparse
import json
import os
import re
import sys
from html.parser import HTMLParser

THRESHOLD = 4
"""Hits at or above this count fail the scan (``>= 4 hits = reprova``)."""

# --------------------------------------------------------------------------- #
# Shared vocabulary
# --------------------------------------------------------------------------- #

TELL_FONTS = frozenset({"inter", "roboto", "system-ui"})
"""F01: the "default AI stack" tell set (minus any ``--allow-font`` names)."""

INDIGO_PURPLE = ("6366f1", "8b5cf6", "7c3aed", "a855f7")
"""F02: the indigo-to-purple hex ramp."""

DARK_BODY_BACKGROUNDS = frozenset({"#000", "#000000", "#0a0a0a", "#0f172a", "#111827"})
"""F04: the flat "dark mode" body backgrounds."""

CREAM_BACKGROUNDS = ("#faf8f4", "#f5f0e8")
"""F14: the cream "warm" second-wave backgrounds."""

GREY_BODY_TEXT = ("#6b7280", "#9ca3af", "#94a3b8")
"""F15: the below-contrast grey body text colours."""

EMOJI_RE = re.compile(
    "[" 
    "\U0001F000-\U0001FAFF"  # pictographs, emoticons, symbols, flags
    "\u2190-\u21FF"          # arrows
    "\u2600-\u27BF"          # misc symbols + dingbats (incl. ✅ ✨)
    "\u2B00-\u2BFF"          # misc arrows and symbols
    "\uFE0F\u200D"           # variation selector, zero-width joiner
    "]"
)

TEXT_TAGS = frozenset(
    {"h1", "h2", "h3", "h4", "h5", "h6", "button", "li"}
)

_CONTAINER_TAGS = frozenset(
    {"div", "section", "ul", "ol", "main", "article", "nav", "header", "footer"}
)

_VOID_TAGS = frozenset(
    {
        "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr",
    }
)

FONT_FAMILY_RE = re.compile(r"font-family\s*:\s*([^;}\n]+)", re.I)
BIG_FONT_RE = re.compile(r"font-size\s*:\s*(?:5[6-9]|[6-9]\d|\d{3,})px", re.I)
CENTER_TEXT_RE = re.compile(r"text-align\s*:\s*center", re.I)
LINEAR_GRADIENT_RE = re.compile(r"linear-gradient\(([^)]*)\)", re.I)
BACKGROUND_CLIP_TEXT_RE = re.compile(r"background-clip\s*:\s*text", re.I)
BLUR_BLOB_RE = re.compile(r"blur\(\s*(?:[6-9]\d|1[01]\d|120)px\s*\)", re.I)
TRUSTED_BY_RE = re.compile(r"trusted by", re.I)
OPERATIONAL_RE = re.compile(r"operational", re.I)
DOUBLE_STYLE_RE = re.compile(r'style\s*=\s*"([^"]*)"')
SINGLE_STYLE_RE = re.compile(r"style\s*=\s*'([^']*)'")


def _normalize(html):
    """Collapse every run of whitespace to a single space."""
    return re.sub(r"\s+", " ", html)


def _css_blocks(text):
    """Return declaration bodies: ``{...}`` rules plus inline ``style`` attrs."""
    blocks = re.findall(r"\{([^{}]*)\}", text)
    blocks += DOUBLE_STYLE_RE.findall(text)
    blocks += SINGLE_STYLE_RE.findall(text)
    return blocks


def _split_families(value):
    """Split a ``font-family`` value into its declared (unquoted) names."""
    names = set()
    for part in value.split(","):
        name = part.strip().strip("\"'").strip()
        if name:
            names.add(name)
    return names


class _Structure(HTMLParser):
    """Collects the small structural facts the matchers need."""

    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.stack = []            # open nodes: {"tag": str, "children": int}
        self.nodes = []            # closed nodes: (tag, child_count)
        self.tag_counts = {}
        self.svgs = []             # attr dicts, in document order
        self.cta_count = 0
        self.text_by_tag = {}      # target tag -> concatenated text

    def handle_starttag(self, tag, attrs):
        self.tag_counts[tag] = self.tag_counts.get(tag, 0) + 1
        if tag in ("a", "button"):
            self.cta_count += 1
        if tag == "svg":
            self.svgs.append(dict(attrs))
        if tag in _VOID_TAGS:
            return
        if self.stack:
            self.stack[-1]["children"] += 1
        self.stack.append({"tag": tag, "children": 0})

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in _VOID_TAGS:
            return
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index]["tag"] == tag:
                closed = self.stack[index:]
                for node in reversed(closed):
                    self.nodes.append((node["tag"], node["children"]))
                del self.stack[index:]
                break

    def handle_data(self, data):
        for node in self.stack:
            if node["tag"] in TEXT_TAGS:
                key = node["tag"]
                self.text_by_tag[key] = self.text_by_tag.get(key, "") + data

    def close(self):
        HTMLParser.close(self)
        for node in reversed(self.stack):
            self.nodes.append((node["tag"], node["children"]))
        self.stack = []


class _Context:
    """Everything a matcher may consult, computed once per document."""

    def __init__(self, html, allow_fonts=None):
        self.raw = html
        self.norm = _normalize(html)
        self.low = self.norm.lower()
        self.allow = set()
        for name in allow_fonts or []:
            self.allow.add(name.strip().strip("\"'").lower())
        parser = _Structure()
        parser.feed(html)
        parser.close()
        self.nodes = parser.nodes
        self.tag_counts = parser.tag_counts
        self.svgs = parser.svgs
        self.cta_count = parser.cta_count
        self.text_by_tag = parser.text_by_tag


# --------------------------------------------------------------------------- #
# R01-R22 matchers. Each returns an evidence string on a hit, else None.
# --------------------------------------------------------------------------- #


def _r01_font_family(ctx):
    """F01: every declared family belongs to the Inter/Roboto/system-ui tell."""
    families = set()
    for match in FONT_FAMILY_RE.finditer(ctx.norm):
        families |= _split_families(match.group(1))
    if not families:
        return None
    effective = TELL_FONTS - ctx.allow
    if all(name.lower() in effective for name in families):
        return "only families declared: %s" % ", ".join(sorted(families))
    return None


def _r02_indigo_gradient(ctx):
    """F02: an indigo-to-purple gradient (or the matching utility)."""
    for match in LINEAR_GRADIENT_RE.finditer(ctx.low):
        inner = match.group(1)
        for hex_value in INDIGO_PURPLE:
            if hex_value in inner:
                return "linear-gradient with #%s" % hex_value
    utility = re.search(r"\bfrom-(?:indigo|violet)-\d{3}", ctx.low)
    if utility:
        return "utility %s" % utility.group(0)
    return None


def _r03_clipped_headline(ctx):
    """F03: background-clip:text next to a linear-gradient on the same rule."""
    for block in _css_blocks(ctx.low):
        if BACKGROUND_CLIP_TEXT_RE.search(block) and "linear-gradient(" in block:
            return "gradient-clipped headline text"
    return None


def _r04_dark_flat(ctx):
    """F04: flat dark body background with a single neon accent."""
    body = re.search(r"body\s*\{[^}]*\}", ctx.low)
    if not body:
        return None
    background = re.search(
        r"background(?:-color)?\s*:\s*([^;}]+)", body.group(0)
    )
    if not background:
        return None
    hex_value = re.search(r"#[0-9a-f]{3,6}", background.group(1))
    if hex_value and hex_value.group(0) in DARK_BODY_BACKGROUNDS:
        return "flat dark body background %s" % hex_value.group(0)
    return None


def _r05_soft_shadows(ctx):
    """F05: five or more soft, identical-looking shadows (blur 8-24, alpha<=.15)."""
    count = 0
    for match in re.finditer(r"box-shadow\s*:\s*([^;}]+)", ctx.low):
        if _is_soft_shadow(match.group(1)):
            count += 1
    if count >= 5:
        return "%d soft box-shadows (blur 8-24px, alpha <= .15)" % count
    return None


def _is_soft_shadow(value):
    alpha_match = re.search(r"rgba?\(([^)]*)\)", value)
    if not alpha_match:
        return False
    parts = [part.strip() for part in alpha_match.group(1).split(",")]
    if len(parts) != 4:
        return False
    try:
        alpha = float(parts[3])
    except ValueError:
        return False
    if alpha > 0.15:
        return False
    cleaned = re.sub(r"rgba?\([^)]*\)", " ", value)
    cleaned = re.sub(r"hsla?\([^)]*\)", " ", cleaned)
    cleaned = re.sub(r"#[0-9a-f]{3,8}", " ", cleaned)
    lengths = re.findall(r"[+-]?(?:\d+\.?\d*|\.\d+)(?:px)?", cleaned)
    if len(lengths) < 3:
        return False
    blur = float(lengths[2].replace("px", ""))
    return 8.0 <= blur <= 24.0


def _r06_uniform_radius(ctx):
    """F06: at most two distinct radii, six or more uses, all in 12-16px."""
    values = [
        match.group(1).strip()
        for match in re.finditer(r"border-radius\s*:\s*([^;}]+)", ctx.low)
    ]
    if len(values) < 6:
        return None
    distinct = set(values)
    if len(distinct) > 2:
        return None
    for value in distinct:
        numbers = re.findall(r"(\d+(?:\.\d+)?)px", value)
        if not numbers or not all(12 <= float(n) <= 16 for n in numbers):
            return None
    return "uniform border-radius (%s) x%d" % (", ".join(sorted(distinct)), len(values))


def _r07_three_cards(ctx):
    """F07: a three-equal-columns grid holding exactly three children."""
    has_grid = re.search(r"repeat\(\s*3\s*,\s*1fr\s*\)", ctx.low) or re.search(
        r"1fr\s+1fr\s+1fr", ctx.low
    )
    if not has_grid:
        return None
    for tag, children in ctx.nodes:
        if tag in _CONTAINER_TAGS and children == 3:
            return "three equal columns with exactly 3 children"
    return None


def _r08_icon_in_square(ctx):
    """F08: three or more 24px currentColor icons in padded/rounded boxes."""
    count = 0
    for attrs in ctx.svgs:
        if "24" in str(attrs.get("width", "")) and "currentColor" in str(
            attrs.get("stroke", "")
        ):
            count += 1
    if count >= 3:
        return "%d 24px currentColor icons" % count
    return None


def _r09_emoji_icons(ctx):
    """F09: a unicode emoji inside a heading, button or list item."""
    for tag in sorted(ctx.text_by_tag):
        if tag in TEXT_TAGS:
            match = EMOJI_RE.search(ctx.text_by_tag[tag])
            if match:
                return "emoji %r inside <%s>" % (match.group(0), tag)
    return None


def _r10_beta_pill(ctx):
    """F10: a fully rounded pill and a beta micro-label before the headline."""
    if "9999px" not in ctx.low:
        return None
    beta = ctx.low.find("beta")
    headline = ctx.low.find("<h1")
    if beta != -1 and headline != -1 and beta < headline:
        return "beta pill before the h1"
    return None


def _r11_centred_hero(ctx):
    """F11: centred stack, headline >= 56px, two or more CTAs."""
    if not CENTER_TEXT_RE.search(ctx.low):
        return None
    if not BIG_FONT_RE.search(ctx.low):
        return None
    if ctx.cta_count >= 2:
        return "centred hero, big h1, %d CTAs" % ctx.cta_count
    return None


def _r12_glass(ctx):
    """F12: backdrop-filter over a translucent white panel."""
    if "backdrop-filter" in ctx.low and re.search(
        r"rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*0?\.1\s*\)", ctx.low
    ):
        return "glassmorphism panel (backdrop-filter + rgba white .1)"
    return None


def _r13_blobs(ctx):
    """F13: large blurred blobs or a repeating radial dot field."""
    if BLUR_BLOB_RE.search(ctx.low):
        return "large blurred background blob"
    if "repeating-radial-gradient" in ctx.low:
        return "repeating radial-gradient dot field"
    return None


def _r14_cream_amber(ctx):
    """F14: cream background plus an amber/stone accent."""
    if not any(hex_value in ctx.low for hex_value in CREAM_BACKGROUNDS):
        return None
    if re.search(r"#(?:f59e0b|fbbf24|d97706|b45309)|amber|stone", ctx.low):
        return "cream background with an amber/stone accent"
    return None


def _r15_grey_text(ctx):
    """F15: below-contrast grey body text colour."""
    for hex_value in GREY_BODY_TEXT:
        if re.search(r"color\s*:\s*" + re.escape(hex_value), ctx.low):
            return "grey body text %s" % hex_value
    return None


def _r16_left_border_callout(ctx):
    """F17: two or more tinted callouts with a 2-4px coloured left border."""
    count = len(re.findall(r"border-left\s*:\s*[234]px", ctx.low))
    if count >= 2:
        return "%d left-border callout boxes" % count
    return None


def _r17_shadcn_defaults(ctx):
    """F19: shadcn's stock tokens shipped as-is."""
    has_token = re.search(r"--radius\s*:\s*0\.5rem", ctx.low) or re.search(
        r"221\.2\s+83\.2%\s+53\.3%", ctx.low
    )
    if has_token and re.search(r"\b(?:slate|zinc)\b", ctx.low):
        return "shadcn default tokens (--radius / --primary hsl)"
    return None


def _r18_trusted_by(ctx):
    """F20: a "trusted by" line above four or more grey wordmarks."""
    if not TRUSTED_BY_RE.search(ctx.low):
        return None
    svg_count = ctx.tag_counts.get("svg", 0)
    faint = len(re.findall(r"opacity\s*:\s*0?\.5\b", ctx.low))
    if svg_count >= 4 or faint >= 4:
        return "trusted-by logo bar (%d svg, %d at opacity .5)" % (svg_count, faint)
    return None


def _r19_fade_up(ctx):
    """F23: IntersectionObserver-driven translateY fade-up on 4+ sections."""
    if "intersectionobserver" in ctx.low and "translatey" in ctx.low:
        sections = ctx.tag_counts.get("section", 0)
        if sections >= 4:
            return "fade-up on %d sections" % sections
    return None


def _r20_theme_toggle(ctx):
    """F24: a persisted theme toggle on a page that has a hero."""
    if (
        "localstorage" in ctx.low
        and "theme" in ctx.low
        and ctx.tag_counts.get("h1", 0) >= 1
    ):
        return "persisted theme toggle on a hero page"
    return None


def _r21_status_dot(ctx):
    """F25: green glow dot with an "all systems operational" line."""
    if (
        "#22c55e" in ctx.low
        and OPERATIONAL_RE.search(ctx.low)
        and "box-shadow" in ctx.low
    ):
        return "glowing green status dot + operational text"
    return None


def _r22_gradient_border(ctx):
    """F26: padding-box/border-box gradient border over a transparent border."""
    if re.search(
        r"background-clip\s*:\s*padding-box\s*,\s*border-box", ctx.low
    ) and "transparent" in ctx.low:
        return "gradient-border AI card glow"
    return None


# (rule_id, fingerprint, confidence, matcher)
RULES = [
    ("R01", "F01", "solid", _r01_font_family),
    ("R02", "F02", "solid", _r02_indigo_gradient),
    ("R03", "F03", "solid", _r03_clipped_headline),
    ("R04", "F04", "heuristic", _r04_dark_flat),
    ("R05", "F05", "heuristic", _r05_soft_shadows),
    ("R06", "F06", "heuristic", _r06_uniform_radius),
    ("R07", "F07", "heuristic", _r07_three_cards),
    ("R08", "F08", "heuristic", _r08_icon_in_square),
    ("R09", "F09", "solid", _r09_emoji_icons),
    ("R10", "F10", "heuristic", _r10_beta_pill),
    ("R11", "F11", "heuristic", _r11_centred_hero),
    ("R12", "F12", "heuristic", _r12_glass),
    ("R13", "F13", "heuristic", _r13_blobs),
    ("R14", "F14", "heuristic", _r14_cream_amber),
    ("R15", "F15", "solid", _r15_grey_text),
    ("R16", "F17", "heuristic", _r16_left_border_callout),
    ("R17", "F19", "solid", _r17_shadcn_defaults),
    ("R18", "F20", "heuristic", _r18_trusted_by),
    ("R19", "F23", "heuristic", _r19_fade_up),
    ("R20", "F24", "solid", _r20_theme_toggle),
    ("R21", "F25", "solid", _r21_status_dot),
    ("R22", "F26", "solid", _r22_gradient_border),
]
"""The 22 mechanical rules, in spec order."""


# --------------------------------------------------------------------------- #
# Public interface
# --------------------------------------------------------------------------- #


def check_html(html, allow_fonts=None):
    """Scan one HTML document and return its :data:`Finding` list.

    ``allow_fonts`` names families a direction legitimately earns; they are
    removed from the F01 tell set (so ``["Inter"]`` silences an all-Inter page).
    """
    ctx = _Context(html, allow_fonts=allow_fonts)
    findings = []
    for rule_id, fingerprint, confidence, matcher in RULES:
        evidence = matcher(ctx)
        if evidence:
            findings.append(
                {
                    "fingerprint": fingerprint,
                    "rule": rule_id,
                    "confidence": confidence,
                    "evidence": evidence,
                }
            )
    return findings


def check_paths(paths, allow_fonts=None):
    """Scan one or more files; return hits, count and the ``pass``/``fail`` verdict."""
    if isinstance(paths, (str, bytes, os.PathLike)):
        paths = [paths]
    hits = []
    for path in paths:
        with open(os.fspath(path), "r", encoding="utf-8") as handle:
            hits.extend(check_html(handle.read(), allow_fonts=allow_fonts))
    count = len(hits)
    return {
        "hits": hits,
        "count": count,
        "verdict": "fail" if count >= THRESHOLD else "pass",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Mechanical slop scan (R01-R22); exit 1 at >=4 hits."
    )
    parser.add_argument("paths", nargs="+", help="HTML files to scan")
    parser.add_argument(
        "--allow-font",
        action="append",
        default=[],
        metavar="NAME",
        dest="allow_fonts",
        help="family the direction earns; removed from the F01 tell set (repeatable)",
    )
    args = parser.parse_args(argv)
    result = check_paths(args.paths, allow_fonts=args.allow_fonts)
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 1 if result["count"] >= THRESHOLD else 0


if __name__ == "__main__":
    sys.exit(main())
