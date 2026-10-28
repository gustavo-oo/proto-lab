#!/usr/bin/env python3
"""Mechanical copy-contract scan for proto-lab (C01 and C04).

``references/copy-contract.md`` defines four zero-tolerance copy rules. This
script implements the deterministic subset:

* ``C01`` — item-count labels such as ``10 registros`` or ``6 filmes`` in a
  heading, legend, caption, summary or label-like element.
* ``C04`` — separator glyphs (``·``, ``|``, ``•``, ``—``, ``–``) joining
  visible product copy.

``C02`` (one fact, one place) and ``C03`` (no filler copy) are judge-only: a
regex cannot reliably decide whether two facts have distinct roles or whether a
line carries information.

The copy gate is **zero-tolerance**: any finding fails the page. The scan is a
single-page verdict; the pipeline calls this once per product page. Session
chrome inside a product page is marked ``data-session-chrome`` and skipped, as
are ``head``, ``script``, ``style``, ``title``, ``template`` and ``noscript``.

Python stdlib only; Python >= 3.8.
"""

import argparse
import json
import os
import re
import sys
from html.parser import HTMLParser

# --------------------------------------------------------------------------- #
# Vocabulary
# --------------------------------------------------------------------------- #

RULES = ("C01", "C04")
"""The rules this scanner implements. C02/C03 are judge-only."""

IGNORED_TAGS = frozenset(
    {"head", "script", "style", "title", "template", "noscript"}
)

VOID_TAGS = frozenset(
    {
        "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr",
    }
)

C01_TAGS = frozenset(
    {"h1", "h2", "h3", "h4", "h5", "h6", "legend", "figcaption", "summary", "caption"}
)
"""Elements that read as labels or headings rather than data fields."""

C01_DATA_TAGS = frozenset({"dt", "dd", "td", "th"})
"""Data fields: a number here is the value, not a count of a list."""

LABEL_CLASS_RE = re.compile(
    r"(?:^|[\s_-])(label|eyebrow|kicker|meta|count|legend|subtitle|caption)(?:$|[\s_-])",
    re.I,
)

COUNT_FRAGMENT_RE = re.compile(
    r"^\s*(\d{1,4})\s+([^\W\d_][\w-]{2,})(?:\s+([^\W\d_][\w-]{2,}))?\s*$",
    re.UNICODE,
)

UNIT_WORDS = frozenset(
    {
        "g", "kg", "mg", "ml", "l", "cl", "dl", "px", "rem", "em", "pt",
        "mm", "cm", "m", "km", "h", "min", "s", "ms", "gb", "mb", "kb",
        "anos", "ano", "meses", "mes", "dias", "dia", "horas", "hora",
        "minutos", "minuto", "segundos", "segundo",
    }
)

SOLID_SEPARATOR_RE = re.compile(r"[·•]")
PIPE_SEPARATOR_RE = re.compile(r"\s\|\s")
DASH_SEPARATOR_RE = re.compile(r"\s[—–]\s")
SEPARATOR_SPLIT_RE = re.compile(r"\s*[·|•—–,;]\s*")
ALONE_SEPARATORS = frozenset({"·", "|", "•", "—", "–"})

_NORMALIZE_RE = re.compile(r"\s+")


def _normalize(text):
    """Collapse whitespace and trim."""
    return _NORMALIZE_RE.sub(" ", text).strip()


# --------------------------------------------------------------------------- #
# A small DOM, enough to preserve element context
# --------------------------------------------------------------------------- #


class _Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag=None, attrs=None, parent=None):
        self.tag = tag
        self.attrs = dict(attrs or [])
        self.children = []
        self.parent = parent


class _Tree(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.root = _Node()
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = _Node(tag, attrs, self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        node = _Node(tag, attrs, self.stack[-1])
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


# --------------------------------------------------------------------------- #
# Traversal helpers
# --------------------------------------------------------------------------- #


def _has_session_chrome(node):
    current = node
    while current is not None:
        if "data-session-chrome" in current.attrs:
            return True
        current = current.parent
    return False


def _visible_text(node):
    if node.tag in IGNORED_TAGS or _has_session_chrome(node):
        return ""
    parts = []
    for child in node.children:
        if isinstance(child, str):
            parts.append(child)
        else:
            parts.append(_visible_text(child))
    return _normalize("".join(parts))


def _iter_elements(node):
    for child in node.children:
        if isinstance(child, _Node):
            yield child
            yield from _iter_elements(child)


def _iter_text_nodes(node):
    """Yield ``(parent, text)`` for visible text nodes outside chrome."""
    if node.tag in IGNORED_TAGS or _has_session_chrome(node):
        return
    for child in node.children:
        if isinstance(child, str):
            text = _normalize(child)
            if text:
                yield node, text
        else:
            yield from _iter_text_nodes(child)


def _class_name(node):
    return node.attrs.get("class", "")


def _is_label_element(node):
    if node.tag in C01_DATA_TAGS:
        return False
    if node.tag in C01_TAGS:
        return True
    return bool(LABEL_CLASS_RE.search(_class_name(node)))


# --------------------------------------------------------------------------- #
# C01: item-count labels
# --------------------------------------------------------------------------- #


def _count_fragment(fragment):
    """Return the count fragment if it reads as an item-count label."""
    fragment = fragment.strip()
    if not fragment:
        return None
    # Dates, ratios and times are values, not counts of a list.
    if re.search(r"[/:]", fragment):
        return None
    # Selection/process counts are state, not a description of the list.
    if re.match(r"^\d+\s+de\s+\d+", fragment):
        return None
    match = COUNT_FRAGMENT_RE.match(fragment)
    if not match:
        return None
    noun = match.group(2).lower()
    if noun in UNIT_WORDS:
        return None
    return fragment


def _c01_findings(root):
    findings = []
    for node in _iter_elements(root):
        if not _is_label_element(node):
            continue
        if _has_session_chrome(node):
            continue
        text = _visible_text(node)
        if not text or len(text) > 160:
            continue
        for fragment in SEPARATOR_SPLIT_RE.split(text):
            label = _count_fragment(fragment)
            if label:
                findings.append(
                    {
                        "rule": "C01",
                        "confidence": "heuristic",
                        "evidence": label,
                        "tag": node.tag,
                        "class": _class_name(node),
                    }
                )
    return findings


# --------------------------------------------------------------------------- #
# C04: separator glyphs
# --------------------------------------------------------------------------- #


def _separator_confidence(text):
    if text in ALONE_SEPARATORS:
        return "solid" if text in {"·", "|", "•"} else "heuristic"
    if SOLID_SEPARATOR_RE.search(text) or PIPE_SEPARATOR_RE.search(text):
        return "solid"
    if DASH_SEPARATOR_RE.search(text):
        return "heuristic"
    return None


def _c04_findings(root):
    findings = []
    for node, text in _iter_text_nodes(root):
        confidence = _separator_confidence(text)
        if not confidence:
            continue
        findings.append(
            {
                "rule": "C04",
                "confidence": confidence,
                "evidence": text,
                "tag": node.tag,
                "class": _class_name(node),
            }
        )
    return findings


# --------------------------------------------------------------------------- #
# Public interface
# --------------------------------------------------------------------------- #


def check_html(html):
    """Scan one HTML document and return its copy-contract findings."""
    tree = _Tree()
    tree.feed(html)
    tree.close()
    return _c01_findings(tree.root) + _c04_findings(tree.root)


def check_paths(paths):
    """Scan file(s) and return ``{"findings", "count", "verdict"}``.

    The copy gate is a per-page verdict, and the pipeline calls this once per
    product page. Passing several paths sums their findings into one count,
    matching the scanner's single-page contract.
    """
    if isinstance(paths, (str, bytes, os.PathLike)):
        paths = [paths]
    findings = []
    for path in paths:
        with open(os.fspath(path), "r", encoding="utf-8") as handle:
            findings.extend(check_html(handle.read()))
    return {
        "findings": findings,
        "count": len(findings),
        "verdict": "fail" if findings else "pass",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Mechanical copy-contract scan (C01/C04); exit 1 on any finding."
    )
    parser.add_argument("paths", nargs="+", help="HTML files to scan")
    args = parser.parse_args(argv)
    result = check_paths(args.paths)
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 1 if result["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
