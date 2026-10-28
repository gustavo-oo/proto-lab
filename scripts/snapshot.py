#!/usr/bin/env python3
"""Capture an existing visual system as a fit-mode snapshot (proto-lab).

``scripts/snapshot.py`` is the reference implementation of
``references/fit-mode.md``. It reads the smallest set of visual sources around
a repository path (or accepts a browser-captured ``--extra`` for a URL), turns
them into a ``style-snapshot.json`` plus a fit ``direction.json``, and keeps the
two deterministic:

* the snapshot is canonical JSON (sorted keys, compact separators, no
  timestamp, relative paths only);
* its ``hash`` is ``sha256`` over that canonical form with the hash removed;
* the fit card records the snapshot hash and nothing that changes on a rerun.

The script never fetches the network. A URL source is captured by the executor
through a browser tool and supplied as ``--extra``; the script normalises,
validates and hashes it.

Python stdlib only, Python >= 3.8.

Usage:
    python3 scripts/snapshot.py --from PATH [--extra EXTRA.json]
                                [--out SNAPSHOT.json] [--card CARD.json]
                                [--seed SEED] [--name NAME]
                                [--existing-html PAGE.html]
    python3 scripts/snapshot.py --check SNAPSHOT.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

# ``roll`` owns the canonical card encoding; ``check_slop`` owns the inherited
# fingerprint baseline.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_slop  # noqa: E402
import roll  # noqa: E402

SCHEMA = "style-snapshot:v1"
SNAPSHOT_NAME = "style-snapshot.json"
ALGORITHM = "snapshot:v1"
HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
RULE_RE = re.compile(r"^R\d{2}$")
FINGERPRINT_RE = re.compile(r"^F\d{2}$")
ABSOLUTE_REF_RE = re.compile(r"^(?:/|~|[A-Za-z]:[\\/])")
URL_RE = re.compile(r"^https?://", re.I)
LINE_SUFFIX_RE = re.compile(r":\d+(?:-\d+)?$")

TOKEN_GROUPS = (
    "color",
    "font",
    "space",
    "radius",
    "shadow",
    "motion",
    "breakpoint",
    "other",
)
EVIDENCE_ORDER = {"inferred": 0, "declared": 1, "observed": 2}
EVIDENCE_LEVELS = tuple(EVIDENCE_ORDER)
SOURCE_KINDS = ("repo", "url", "files")
TOP_LEVEL_KEYS = {
    "schema",
    "evidence",
    "source",
    "tokens",
    "type",
    "components",
    "layout",
    "voice",
    "constraints",
    "extensions",
    "inherited_slop",
    "gaps",
    "hash",
}
SOURCE_KEYS = {"kind", "root", "files", "url", "notes"}
TOKEN_KEYS = {"role", "name", "value", "source", "evidence"}
SCALE_KEYS = {
    "role",
    "size",
    "weight",
    "line_height",
    "letter_spacing",
    "source",
    "evidence",
}
COMPONENT_KEYS = {"name", "selector", "states", "facts", "source", "evidence"}
VOICE_KEYS = {"samples", "terminology", "casing"}
EXTENSION_KEYS = {"role", "name", "value", "reason", "approved_at_gate"}
INHERITED_KEYS = {"rule", "fingerprint", "evidence", "source"}
EXTRA_KEYS = {
    "source",
    "tokens",
    "type",
    "components",
    "layout",
    "voice",
    "constraints",
    "extensions",
    "inherited_slop",
    "gaps",
    "evidence",
}
GENERIC_FAMILIES = {
    "serif",
    "sans-serif",
    "monospace",
    "cursive",
    "fantasy",
    "system-ui",
    "ui-serif",
    "ui-sans-serif",
    "ui-monospace",
    "ui-rounded",
    "emoji",
    "math",
    "fangsong",
}

MAX_SOURCE_FILES = 8
MAX_COMPONENTS = 12
MAX_VOICE_SAMPLES = 5
MAX_WALK_FILES = 2000

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "bower_components",
    "vendor",
    "dist",
    "build",
    "out",
    "coverage",
    ".next",
    ".nuxt",
    ".svelte-kit",
    ".cache",
    ".turbo",
    "__pycache__",
    "public",
    "assets",
    "static",
}

# Named sources come first; any other CSS is a fallback. A Tailwind config is
# recorded as a gap rather than parsed (v1 scope).
PRIORITY_NAMES = {
    "tokens.css": 0,
    "tokens.json": 0,
    "design-tokens.json": 0,
    "theme.css": 1,
    "variables.css": 1,
    "globals.css": 1,
    "global.css": 1,
    "app.css": 2,
    "index.css": 2,
    "styles.css": 2,
    "design.md": 3,
    "tailwind.config.js": 4,
    "tailwind.config.cjs": 4,
    "tailwind.config.mjs": 4,
    "tailwind.config.ts": 4,
}

COLOR_HINTS = (
    "color",
    "colour",
    "bg",
    "background",
    "ink",
    "surface",
    "accent",
    "fg",
    "text",
    "muted",
    "border",
    "success",
    "warn",
    "danger",
    "error",
    "primary",
    "secondary",
    "focus",
    "ring",
    "brand",
    "fill",
    "stroke",
)
FONT_HINTS = ("font", "family", "typeface")
SPACE_HINTS = ("space", "spacing", "gap", "gutter", "padding", "margin")
RADIUS_HINTS = ("radius", "rounded")
SHADOW_HINTS = ("shadow", "elevation")
MOTION_HINTS = ("motion", "duration", "ease", "easing", "transition", "animation")
BREAKPOINT_HINTS = ("breakpoint", "breakpoints", "screen", "viewport")

COLOR_VALUE_RE = re.compile(
    r"^(?:#[0-9a-fA-F]{3,8}|(?:rgb|rgba|hsl|hsla|oklch|oklab|lab|lch|color|color-mix)\()",
    re.I,
)
FONT_VALUE_RE = re.compile(r"[A-Za-z][^,;]*,\s*(?:serif|sans-serif|monospace|system-ui)")
BLOCK_RE = re.compile(r"([^{}]+)\{([^{}]*)\}", re.S)
CUSTOM_PROP_RE = re.compile(r"(--[A-Za-z0-9_-]+)\s*:\s*([^;{}]+)")
FONT_FAMILY_RE = re.compile(r"(?<![\w-])font-family\s*:\s*([^;{}]+)", re.I)
COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)


class SnapshotError(ValueError):
    """A snapshot that violates ``references/fit-mode.md``."""


# --------------------------------------------------------------------------- #
# Small helpers
# --------------------------------------------------------------------------- #


def _blank_snapshot():
    return {
        "schema": SCHEMA,
        "evidence": "declared",
        "source": {"kind": "repo", "root": ".", "files": [], "url": None, "notes": ""},
        "tokens": {group: [] for group in TOKEN_GROUPS},
        "type": {"families": [], "scale": []},
        "components": [],
        "layout": {},
        "voice": {"samples": [], "terminology": [], "casing": ""},
        "constraints": [],
        "extensions": [],
        "inherited_slop": [],
        "gaps": [],
        "hash": "",
    }


def _strip_css_comments(text):
    """Blank out CSS comments while preserving every newline and offset."""

    def replace(match):
        return "".join("\n" if char == "\n" else " " for char in match.group(0))

    return COMMENT_RE.sub(replace, text)


def _line_of(text, index):
    return text.count("\n", 0, index) + 1


def _relative(path, root):
    """A POSIX path relative to ``root``; the basename when outside it."""
    path = Path(path).resolve()
    root = Path(root).resolve()
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.name


def _is_url(value):
    return isinstance(value, str) and bool(URL_RE.match(value))


def _is_absolute_ref(value):
    """True for a filesystem-absolute source; URLs are allowed."""
    if not isinstance(value, str) or _is_url(value):
        return False
    stripped = LINE_SUFFIX_RE.sub("", value)
    return bool(ABSOLUTE_REF_RE.match(stripped))


def _dedupe(items, key):
    seen = set()
    result = []
    for item in items:
        marker = key(item)
        if marker in seen:
            continue
        seen.add(marker)
        result.append(item)
    return result


def _as_list(value, label):
    if not isinstance(value, list):
        raise SnapshotError("%s must be an array" % label)
    return value


def _as_str(value, label):
    if not isinstance(value, str):
        raise SnapshotError("%s must be a string" % label)
    return value


def _check_evidence(value, label):
    if value not in EVIDENCE_ORDER:
        raise SnapshotError(
            "%s must be one of %s" % (label, ", ".join(EVIDENCE_LEVELS))
        )
    return value


# --------------------------------------------------------------------------- #
# CSS extraction
# --------------------------------------------------------------------------- #


def _classify(name, value):
    lowered = name.lower()
    if (
        lowered.startswith("--bp-")
        or "breakpoint" in lowered
        or "screen" in lowered
        or "viewport" in lowered
    ):
        return "breakpoint"
    if any(hint in lowered for hint in RADIUS_HINTS):
        return "radius"
    if any(hint in lowered for hint in SHADOW_HINTS):
        return "shadow"
    if any(hint in lowered for hint in MOTION_HINTS):
        return "motion"
    if any(hint in lowered for hint in BREAKPOINT_HINTS):
        return "breakpoint"
    if any(hint in lowered for hint in SPACE_HINTS):
        return "space"
    if any(hint in lowered for hint in FONT_HINTS):
        return "font"
    if any(hint in lowered for hint in COLOR_HINTS):
        return "color"
    if COLOR_VALUE_RE.search(value.strip()):
        return "color"
    if FONT_VALUE_RE.search(value):
        return "font"
    return "other"


def _role(name, group):
    role = name[2:] if name.startswith("--") else name
    for prefix in ("%s-" % group, "color-", "font-", "space-", "radius-", "shadow-"):
        if role.startswith(prefix) and len(role) > len(prefix):
            return role[len(prefix) :]
    return role or name


def _first_family(value):
    first = value.split(",", 1)[0].strip().strip("\"'").strip()
    if not first or first.lower() in GENERIC_FAMILIES:
        return None
    return first


def _families_from_tokens(snapshot):
    """Keep ``type.families`` in sync with the captured font tokens."""
    for item in snapshot["tokens"]["font"]:
        family = _first_family(item["value"])
        if family:
            snapshot["type"]["families"].append(family)


def _scan_css(path, root):
    """Return ``(tokens, families, gaps)`` for one CSS file."""
    text = _strip_css_comments(Path(path).read_text(encoding="utf-8"))
    relative = _relative(path, root)
    tokens = []
    families = []
    gaps = []
    seen = {}

    for block in BLOCK_RE.finditer(text):
        body = block.group(2)
        body_start = block.start(2)
        for declaration in CUSTOM_PROP_RE.finditer(body):
            name = declaration.group(1)
            value = declaration.group(2).strip()
            line = _line_of(text, body_start + declaration.start())
            source = "%s:%d" % (relative, line)
            group = _classify(name, value)
            item = {
                "role": _role(name, group),
                "name": name,
                "value": value,
                "source": source,
                "evidence": "declared",
            }
            marker = (group, name)
            if marker in seen:
                gaps.append(
                    "duplicate token %s at %s; kept the first at %s"
                    % (name, source, seen[marker])
                )
                continue
            seen[marker] = source
            tokens.append((group, item))

    font_values = set(
        item["value"] for group, item in tokens if group == "font"
    )
    for match in FONT_FAMILY_RE.finditer(text):
        value = match.group(1).strip()
        if value in font_values:
            continue
        font_values.add(value)
        line = _line_of(text, match.start())
        source = "%s:%d" % (relative, line)
        tokens.append(
            (
                "font",
                {
                    "role": "family",
                    "name": "font-family",
                    "value": value,
                    "source": source,
                    "evidence": "declared",
                },
            )
        )
        family = _first_family(value)
        if family:
            families.append(family)

    for group, item in tokens:
        if group == "font":
            family = _first_family(item["value"])
            if family:
                families.append(family)

    return [item for group, item in tokens], families, gaps


def _walk_candidates(root):
    """Bounded, deterministic scan for visual sources under ``root``."""
    root = Path(root)
    candidates = []
    walked = 0
    truncated = False
    for directory, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(
            name
            for name in dirnames
            if name not in SKIP_DIRS and not name.startswith(".")
        )
        for filename in sorted(filenames):
            walked += 1
            if walked > MAX_WALK_FILES:
                truncated = True
                break
            lower = filename.lower()
            suffix = Path(filename).suffix.lower()
            if lower not in PRIORITY_NAMES and suffix != ".css":
                continue
            path = Path(directory) / filename
            priority = PRIORITY_NAMES.get(lower, 5)
            candidates.append((priority, path.as_posix(), path))
        if truncated:
            break
    candidates.sort(key=lambda item: (item[0], item[1]))
    return [item[2] for item in candidates], truncated


def _scan_source_path(source, root):
    """Capture CSS/JSON/Markdown sources and return tokens/families/gaps."""
    tokens = []
    families = []
    gaps = []
    files = []
    candidates, truncated = _walk_candidates(source)
    if truncated:
        gaps.append(
            "source walk stopped after %d files; pass a narrower --from path"
            % MAX_WALK_FILES
        )
    for path in candidates:
        if len(files) >= MAX_SOURCE_FILES:
            gaps.append(
                "source cap reached (≤ %d files); later candidates were not read"
                % MAX_SOURCE_FILES
            )
            break
        suffix = path.suffix.lower()
        lower = path.name.lower()
        if lower.startswith("tailwind.config"):
            files.append(_relative(path, root))
            gaps.append(
                "Tailwind config %s found; v1 needs its generated CSS or --extra tokens"
                % _relative(path, root)
            )
            continue
        if suffix == ".css":
            files.append(_relative(path, root))
            file_tokens, file_families, file_gaps = _scan_css(path, root)
            tokens.extend(file_tokens)
            families.extend(file_families)
            gaps.extend(file_gaps)
        elif suffix == ".json":
            files.append(_relative(path, root))
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                gaps.append(
                    "JSON source %s is not an object" % _relative(path, root)
                )
            elif data.get("schema") == SCHEMA:
                gaps.append(
                    "snapshot input %s found; pass it directly with --from"
                    % _relative(path, root)
                )
            else:
                tokens.extend(_flat_tokens(data, root, _relative(path, root)))
                gaps.append(
                    "flat token JSON %s read; add components/layout/voice with --extra"
                    % _relative(path, root)
                )
        elif suffix == ".md":
            files.append(_relative(path, root))
            gaps.append(
                "prose source %s found; tokens from it must be authored via --extra"
                % _relative(path, root)
            )
    return tokens, families, gaps, files


# --------------------------------------------------------------------------- #
# Authoring and merging
# --------------------------------------------------------------------------- #


def _token_item(item, group, root):
    if not isinstance(item, dict):
        raise SnapshotError("tokens.%s entries must be objects" % group)
    unknown = set(item) - TOKEN_KEYS
    if unknown:
        raise SnapshotError(
            "tokens.%s entry has unknown keys: %s" % (group, ", ".join(sorted(unknown)))
        )
    name = _as_str(item.get("name"), "tokens.%s.name" % group)
    value = _as_str(item.get("value"), "tokens.%s.value" % group)
    source = _as_str(item.get("source"), "tokens.%s.source" % group)
    if not source:
        raise SnapshotError("tokens.%s.source must not be empty" % group)
    evidence = _check_evidence(
        item.get("evidence", "declared"), "tokens.%s.evidence" % group
    )
    role = _as_str(item.get("role") or _role(name, group), "tokens.%s.role" % group)
    return {
        "role": role,
        "name": name,
        "value": value,
        "source": source,
        "evidence": evidence,
    }


def _flat_tokens(data, root, source_name):
    """Convert a flat ``{group: {name: value}}`` or ``{--name: value}`` map."""
    tokens = []
    for group, entries in data.items():
        if group in TOKEN_GROUPS and isinstance(entries, dict):
            for name, value in entries.items():
                if isinstance(value, dict):
                    raise SnapshotError(
                        "nested token values are not supported: %s.%s" % (group, name)
                    )
                token_name = name if str(name).startswith("--") else "--%s-%s" % (group, name)
                tokens.append(
                    {
                        "role": _role(str(token_name), group),
                        "name": str(token_name),
                        "value": str(value),
                        "source": source_name,
                        "evidence": "declared",
                    }
                )
        elif str(group).startswith("--"):
            token_name = str(group)
            token_group = _classify(token_name, str(entries))
            tokens.append(
                {
                    "role": _role(token_name, token_group),
                    "name": token_name,
                    "value": str(entries),
                    "source": source_name,
                    "evidence": "declared",
                }
            )
    return tokens


def _merge_extra(snapshot, extra, root):
    if not isinstance(extra, dict):
        raise SnapshotError("--extra must contain a JSON object")
    unknown = set(extra) - EXTRA_KEYS
    if unknown:
        raise SnapshotError("--extra has unknown keys: %s" % ", ".join(sorted(unknown)))

    if "evidence" in extra:
        snapshot["evidence"] = _check_evidence(extra["evidence"], "--extra.evidence")

    if "source" in extra:
        source = extra["source"]
        if not isinstance(source, dict):
            raise SnapshotError("--extra.source must be an object")
        unknown_source = set(source) - SOURCE_KEYS
        if unknown_source:
            raise SnapshotError(
                "--extra.source has unknown keys: %s"
                % ", ".join(sorted(unknown_source))
            )
        for key, value in source.items():
            if key == "files":
                files = _as_list(value, "--extra.source.files")
                snapshot["source"]["files"].extend(
                    _as_str(item, "--extra.source.files[]") for item in files
                )
            elif key == "kind":
                if value not in SOURCE_KINDS:
                    raise SnapshotError(
                        "--extra.source.kind must be one of %s"
                        % ", ".join(SOURCE_KINDS)
                    )
                snapshot["source"]["kind"] = value
            else:
                snapshot["source"][key] = value

    if "tokens" in extra:
        grouped = extra["tokens"]
        if not isinstance(grouped, dict):
            raise SnapshotError("--extra.tokens must be an object")
        for group, items in grouped.items():
            if group not in TOKEN_GROUPS:
                raise SnapshotError(
                    "--extra.tokens.%s is not a token group (%s)"
                    % (group, ", ".join(TOKEN_GROUPS))
                )
            for item in _as_list(items, "--extra.tokens.%s" % group):
                snapshot["tokens"][group].append(_token_item(item, group, root))
        snapshot["tokens"] = {
            group: _sort_tokens(snapshot["tokens"][group]) for group in TOKEN_GROUPS
        }

    if "type" in extra:
        value = extra["type"]
        if not isinstance(value, dict):
            raise SnapshotError("--extra.type must be an object")
        unknown_type = set(value) - {"families", "scale"}
        if unknown_type:
            raise SnapshotError(
                "--extra.type has unknown keys: %s" % ", ".join(sorted(unknown_type))
            )
        if "families" in value:
            families = _as_list(value["families"], "--extra.type.families")
            snapshot["type"]["families"].extend(
                _as_str(item, "--extra.type.families[]") for item in families
            )
        if "scale" in value:
            for item in _as_list(value["scale"], "--extra.type.scale"):
                if not isinstance(item, dict):
                    raise SnapshotError("--extra.type.scale entries must be objects")
                unknown_scale = set(item) - SCALE_KEYS
                if unknown_scale:
                    raise SnapshotError(
                        "--extra.type.scale has unknown keys: %s"
                        % ", ".join(sorted(unknown_scale))
                    )
                entry = dict(item)
                entry.setdefault("evidence", "declared")
                snapshot["type"]["scale"].append(entry)

    if "components" in extra:
        for item in _as_list(extra["components"], "--extra.components"):
            if not isinstance(item, dict):
                raise SnapshotError("--extra.components entries must be objects")
            unknown_component = set(item) - COMPONENT_KEYS
            if unknown_component:
                raise SnapshotError(
                    "--extra.components has unknown keys: %s"
                    % ", ".join(sorted(unknown_component))
                )
            entry = dict(item)
            entry.setdefault("evidence", "declared")
            snapshot["components"].append(entry)

    if "layout" in extra:
        value = extra["layout"]
        if not isinstance(value, dict):
            raise SnapshotError("--extra.layout must be an object")
        snapshot["layout"].update(value)

    if "voice" in extra:
        value = extra["voice"]
        if not isinstance(value, dict):
            raise SnapshotError("--extra.voice must be an object")
        unknown_voice = set(value) - VOICE_KEYS
        if unknown_voice:
            raise SnapshotError(
                "--extra.voice has unknown keys: %s" % ", ".join(sorted(unknown_voice))
            )
        if "samples" in value:
            snapshot["voice"]["samples"].extend(
                _as_str(item, "--extra.voice.samples[]")
                for item in _as_list(value["samples"], "--extra.voice.samples")
            )
        if "terminology" in value:
            snapshot["voice"]["terminology"].extend(
                _as_str(item, "--extra.voice.terminology[]")
                for item in _as_list(value["terminology"], "--extra.voice.terminology")
            )
        if "casing" in value:
            snapshot["voice"]["casing"] = _as_str(
                value["casing"], "--extra.voice.casing"
            )

    for key in ("constraints", "gaps"):
        if key in extra:
            snapshot[key].extend(
                _as_str(item, "--extra.%s[]" % key)
                for item in _as_list(extra[key], "--extra.%s" % key)
            )

    if "extensions" in extra:
        for item in _as_list(extra["extensions"], "--extra.extensions"):
            if not isinstance(item, dict):
                raise SnapshotError("--extra.extensions entries must be objects")
            unknown_extension = set(item) - EXTENSION_KEYS
            if unknown_extension:
                raise SnapshotError(
                    "--extra.extensions has unknown keys: %s"
                    % ", ".join(sorted(unknown_extension))
                )
            snapshot["extensions"].append(dict(item))

    if "inherited_slop" in extra:
        for item in _as_list(extra["inherited_slop"], "--extra.inherited_slop"):
            if not isinstance(item, dict):
                raise SnapshotError("--extra.inherited_slop entries must be objects")
            unknown_inherited = set(item) - INHERITED_KEYS
            if unknown_inherited:
                raise SnapshotError(
                    "--extra.inherited_slop has unknown keys: %s"
                    % ", ".join(sorted(unknown_inherited))
                )
            snapshot["inherited_slop"].append(dict(item))

    return snapshot


def _load_snapshot_input(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SnapshotError("%s must contain a JSON object" % path)
    if data.get("schema") == SCHEMA:
        snapshot = _blank_snapshot()
        for key, value in data.items():
            if key == "hash":
                continue
            if key not in TOP_LEVEL_KEYS:
                raise SnapshotError("snapshot has unknown key %r" % key)
            snapshot[key] = value
        return snapshot
    return None


# --------------------------------------------------------------------------- #
# Sorting, hashing, validation
# --------------------------------------------------------------------------- #


def _sort_tokens(items):
    return sorted(
        items,
        key=lambda item: (
            item.get("role", ""),
            item.get("name", ""),
            item.get("value", ""),
            item.get("source", ""),
        ),
    )


def _sort_snapshot(snapshot):
    snapshot["source"]["files"] = sorted(set(snapshot["source"]["files"]))
    snapshot["tokens"] = {
        group: _sort_tokens(snapshot["tokens"].get(group, [])) for group in TOKEN_GROUPS
    }
    snapshot["type"]["families"] = sorted(set(snapshot["type"]["families"]))
    snapshot["type"]["scale"] = sorted(
        snapshot["type"]["scale"],
        key=lambda item: (
            str(item.get("role", "")),
            str(item.get("size", "")),
            str(item.get("weight", "")),
        ),
    )
    snapshot["components"] = sorted(
        _dedupe(
            snapshot["components"],
            key=lambda item: (
                item.get("name", ""),
                item.get("selector", ""),
                item.get("source", ""),
            ),
        ),
        key=lambda item: (str(item.get("name", "")), str(item.get("selector", ""))),
    )
    snapshot["voice"]["samples"] = _dedupe(
        snapshot["voice"]["samples"], key=lambda item: item
    )[:MAX_VOICE_SAMPLES]
    snapshot["voice"]["terminology"] = sorted(set(snapshot["voice"]["terminology"]))
    for key in ("constraints", "gaps"):
        snapshot[key] = sorted(set(snapshot[key]))
    snapshot["extensions"] = sorted(
        _dedupe(
            snapshot["extensions"],
            key=lambda item: (
                item.get("role", ""),
                item.get("name", ""),
                item.get("value", ""),
            ),
        ),
        key=lambda item: (str(item.get("role", "")), str(item.get("name", ""))),
    )
    snapshot["inherited_slop"] = sorted(
        _dedupe(
            snapshot["inherited_slop"],
            key=lambda item: (
                item.get("rule", ""),
                item.get("fingerprint", ""),
                item.get("evidence", ""),
            ),
        ),
        key=lambda item: (
            str(item.get("rule", "")),
            str(item.get("fingerprint", "")),
            str(item.get("evidence", "")),
        ),
    )
    return snapshot


def _compute_hash(snapshot):
    payload = {key: value for key, value in snapshot.items() if key != "hash"}
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _canonical(snapshot):
    snapshot = dict(snapshot)
    snapshot["hash"] = _compute_hash(snapshot)
    return json.dumps(
        snapshot, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )


def _check_ref(value, label):
    value = _as_str(value, label)
    if not value:
        raise SnapshotError("%s must not be empty" % label)
    if _is_absolute_ref(value):
        raise SnapshotError("%s must be relative to source.root: %s" % (label, value))
    return value


def _validate(snapshot, check_hash=False):
    if not isinstance(snapshot, dict):
        raise SnapshotError("snapshot must be a JSON object")
    missing = sorted(TOP_LEVEL_KEYS - set(snapshot))
    unknown = sorted(set(snapshot) - TOP_LEVEL_KEYS)
    if missing or unknown:
        raise SnapshotError(
            "snapshot top-level keys must be exactly %s (missing: %s; unknown: %s)"
            % (
                ", ".join(sorted(TOP_LEVEL_KEYS)),
                ", ".join(missing) or "none",
                ", ".join(unknown) or "none",
            )
        )
    if snapshot["schema"] != SCHEMA:
        raise SnapshotError("snapshot.schema must be %r" % SCHEMA)
    _check_evidence(snapshot["evidence"], "snapshot.evidence")

    source = snapshot["source"]
    if not isinstance(source, dict) or set(source) != SOURCE_KEYS:
        raise SnapshotError(
            "snapshot.source must have exactly the keys %s"
            % ", ".join(sorted(SOURCE_KEYS))
        )
    if source["kind"] not in SOURCE_KINDS:
        raise SnapshotError(
            "snapshot.source.kind must be one of %s" % ", ".join(SOURCE_KINDS)
        )
    if source["root"] != ".":
        raise SnapshotError("snapshot.source.root must be '.' in the canonical form")
    files = _as_list(source["files"], "snapshot.source.files")
    if len(files) > MAX_SOURCE_FILES:
        raise SnapshotError(
            "snapshot.source.files has %d entries; the cap is %d"
            % (len(files), MAX_SOURCE_FILES)
        )
    for index, item in enumerate(files):
        _check_ref(item, "snapshot.source.files[%d]" % index)
    if source["url"] is not None and not _is_url(source["url"]):
        raise SnapshotError("snapshot.source.url must be an http(s) URL or null")
    _as_str(source["notes"], "snapshot.source.notes")

    tokens = snapshot["tokens"]
    if not isinstance(tokens, dict) or set(tokens) != set(TOKEN_GROUPS):
        raise SnapshotError(
            "snapshot.tokens must have exactly the groups %s"
            % ", ".join(TOKEN_GROUPS)
        )
    for group in TOKEN_GROUPS:
        for index, item in enumerate(_as_list(tokens[group], "snapshot.tokens.%s" % group)):
            if not isinstance(item, dict) or set(item) != TOKEN_KEYS:
                raise SnapshotError(
                    "snapshot.tokens.%s[%d] must have exactly the keys %s"
                    % (group, index, ", ".join(sorted(TOKEN_KEYS)))
                )
            _as_str(item["role"], "snapshot.tokens.%s[%d].role" % (group, index))
            _as_str(item["name"], "snapshot.tokens.%s[%d].name" % (group, index))
            _as_str(item["value"], "snapshot.tokens.%s[%d].value" % (group, index))
            _check_ref(
                item["source"], "snapshot.tokens.%s[%d].source" % (group, index)
            )
            _check_evidence(
                item["evidence"], "snapshot.tokens.%s[%d].evidence" % (group, index)
            )
            if EVIDENCE_ORDER[item["evidence"]] > EVIDENCE_ORDER[snapshot["evidence"]]:
                raise SnapshotError(
                    "token evidence %r is stronger than the snapshot header %r"
                    % (item["evidence"], snapshot["evidence"])
                )

    type_value = snapshot["type"]
    if not isinstance(type_value, dict) or set(type_value) != {"families", "scale"}:
        raise SnapshotError("snapshot.type must have exactly families and scale")
    for index, item in enumerate(
        _as_list(type_value["families"], "snapshot.type.families")
    ):
        _as_str(item, "snapshot.type.families[%d]" % index)
    for index, item in enumerate(_as_list(type_value["scale"], "snapshot.type.scale")):
        if not isinstance(item, dict) or set(item) - SCALE_KEYS:
            raise SnapshotError(
                "snapshot.type.scale[%d] has unknown keys" % index
            )
        for key in ("role", "size", "source"):
            _as_str(item.get(key), "snapshot.type.scale[%d].%s" % (index, key))
        _check_ref(item["source"], "snapshot.type.scale[%d].source" % index)
        _check_evidence(
            item.get("evidence", "declared"), "snapshot.type.scale[%d].evidence" % index
        )

    components = _as_list(snapshot["components"], "snapshot.components")
    if len(components) > MAX_COMPONENTS:
        raise SnapshotError(
            "snapshot.components has %d entries; the cap is %d"
            % (len(components), MAX_COMPONENTS)
        )
    for index, item in enumerate(components):
        if not isinstance(item, dict) or set(item) != COMPONENT_KEYS:
            raise SnapshotError(
                "snapshot.components[%d] must have exactly the keys %s"
                % (index, ", ".join(sorted(COMPONENT_KEYS)))
            )
        for key in ("name", "selector", "source"):
            _as_str(item[key], "snapshot.components[%d].%s" % (index, key))
        _check_ref(item["source"], "snapshot.components[%d].source" % index)
        for state in _as_list(
            item["states"], "snapshot.components[%d].states" % index
        ):
            _as_str(state, "snapshot.components[%d].states[]" % index)
        if not isinstance(item["facts"], dict):
            raise SnapshotError("snapshot.components[%d].facts must be an object" % index)
        _check_evidence(
            item["evidence"], "snapshot.components[%d].evidence" % index
        )

    if not isinstance(snapshot["layout"], dict):
        raise SnapshotError("snapshot.layout must be an object")

    voice = snapshot["voice"]
    if not isinstance(voice, dict) or set(voice) != VOICE_KEYS:
        raise SnapshotError(
            "snapshot.voice must have exactly the keys %s" % ", ".join(sorted(VOICE_KEYS))
        )
    samples = _as_list(voice["samples"], "snapshot.voice.samples")
    if len(samples) > MAX_VOICE_SAMPLES:
        raise SnapshotError(
            "snapshot.voice.samples has %d entries; the cap is %d"
            % (len(samples), MAX_VOICE_SAMPLES)
        )
    for index, item in enumerate(samples):
        _as_str(item, "snapshot.voice.samples[%d]" % index)
    for index, item in enumerate(
        _as_list(voice["terminology"], "snapshot.voice.terminology")
    ):
        _as_str(item, "snapshot.voice.terminology[%d]" % index)
    _as_str(voice["casing"], "snapshot.voice.casing")

    for key in ("constraints", "gaps"):
        for index, item in enumerate(_as_list(snapshot[key], "snapshot.%s" % key)):
            _as_str(item, "snapshot.%s[%d]" % (key, index))

    for index, item in enumerate(
        _as_list(snapshot["extensions"], "snapshot.extensions")
    ):
        if not isinstance(item, dict) or set(item) != EXTENSION_KEYS:
            raise SnapshotError(
                "snapshot.extensions[%d] must have exactly the keys %s"
                % (index, ", ".join(sorted(EXTENSION_KEYS)))
            )
        for key in ("role", "name", "value", "reason"):
            _as_str(item[key], "snapshot.extensions[%d].%s" % (index, key))
        if item["approved_at_gate"] is not True:
            raise SnapshotError(
                "snapshot.extensions[%d].approved_at_gate must be true" % index
            )

    for index, item in enumerate(
        _as_list(snapshot["inherited_slop"], "snapshot.inherited_slop")
    ):
        if not isinstance(item, dict) or set(item) != INHERITED_KEYS:
            raise SnapshotError(
                "snapshot.inherited_slop[%d] must have exactly the keys %s"
                % (index, ", ".join(sorted(INHERITED_KEYS)))
            )
        if not RULE_RE.match(str(item["rule"])):
            raise SnapshotError(
                "snapshot.inherited_slop[%d].rule must look like R01" % index
            )
        if not FINGERPRINT_RE.match(str(item["fingerprint"])):
            raise SnapshotError(
                "snapshot.inherited_slop[%d].fingerprint must look like F01" % index
            )
        _as_str(item["evidence"], "snapshot.inherited_slop[%d].evidence" % index)
        _check_ref(item["source"], "snapshot.inherited_slop[%d].source" % index)

    if not HASH_RE.match(str(snapshot["hash"])):
        raise SnapshotError("snapshot.hash must be sha256:<64 hex>")
    if check_hash and snapshot["hash"] != _compute_hash(snapshot):
        raise SnapshotError(
            "snapshot hash mismatch: recorded %s, computed %s"
            % (snapshot["hash"], _compute_hash(snapshot))
        )

    _reject_timestamps(snapshot)
    return snapshot


def _reject_timestamps(value, path="snapshot"):
    if isinstance(value, dict):
        for key, item in value.items():
            if key in ("timestamp", "captured_at", "created_at"):
                raise SnapshotError(
                    "%s.%s is a timestamp; snapshots must be deterministic"
                    % (path, key)
                )
            _reject_timestamps(item, "%s.%s" % (path, key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_timestamps(item, "%s[%d]" % (path, index))


# --------------------------------------------------------------------------- #
# Capture and the fit card
# --------------------------------------------------------------------------- #


def _capture_from_path(source, snapshot):
    root = Path(source)
    loaded_snapshot = False
    if root.is_dir():
        tokens, families, gaps, files = _scan_source_path(root, root)
        snapshot["source"].update(
            {"kind": "repo", "root": ".", "files": files, "url": None}
        )
        snapshot["gaps"].extend(gaps)
    elif root.is_file():
        parent = root.parent
        relative = _relative(root, parent)
        snapshot["source"].update(
            {"kind": "repo", "root": ".", "files": [relative], "url": None}
        )
        suffix = root.suffix.lower()
        if suffix == ".css":
            tokens, families, gaps = _scan_css(root, parent)
            snapshot["gaps"].extend(gaps)
        elif suffix == ".json":
            data = json.loads(root.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise SnapshotError("%s must contain a JSON object" % root)
            if data.get("schema") == SCHEMA:
                loaded = _load_snapshot_input(root)
                for key in TOP_LEVEL_KEYS - {"hash"}:
                    snapshot[key] = loaded[key]
                tokens, families = [], []
                loaded_snapshot = True
            else:
                tokens = _flat_tokens(data, parent, relative)
                families = []
                snapshot["gaps"].append(
                    "flat token JSON %s read; add components/layout/voice with --extra"
                    % relative
                )
        elif suffix == ".md":
            tokens, families = [], []
            snapshot["gaps"].append(
                "prose source %s read; tokens from it must be authored via --extra"
                % relative
            )
        else:
            raise SnapshotError(
                "%s is not a CSS, JSON or Markdown visual source" % root
            )
    else:
        raise SnapshotError("source does not exist: %s" % source)

    return tokens, families, loaded_snapshot


def capture(source=None, extra_path=None, existing_html=None):
    """Build, merge, sort and validate a snapshot; return the dict."""
    snapshot = _blank_snapshot()
    tokens = []
    families = []
    loaded_snapshot = False

    if source and _is_url(source):
        snapshot["source"].update(
            {"kind": "url", "root": ".", "files": [], "url": source}
        )
        snapshot["evidence"] = "inferred"
    elif source:
        tokens, families, loaded_snapshot = _capture_from_path(source, snapshot)

    for item in tokens:
        group = _classify(item["name"], item["value"])
        snapshot["tokens"][group].append(item)
    snapshot["type"]["families"].extend(families)

    if extra_path:
        extra = json.loads(Path(extra_path).read_text(encoding="utf-8"))
        snapshot = _merge_extra(snapshot, extra, Path.cwd())

    _families_from_tokens(snapshot)

    if (
        snapshot["source"]["kind"] == "url"
        and not any(snapshot["tokens"][group] for group in TOKEN_GROUPS)
        and not snapshot["components"]
    ):
        raise SnapshotError(
            "a URL source needs browser-captured tokens/components in --extra"
        )

    if existing_html:
        html_path = Path(existing_html)
        if not html_path.is_file():
            raise SnapshotError("--existing-html does not exist: %s" % existing_html)
        findings = check_slop.check_html(html_path.read_text(encoding="utf-8"))
        if source and not _is_url(source):
            source_root = Path(source)
            if not source_root.is_dir():
                source_root = source_root.parent
        else:
            source_root = Path.cwd()
        source_ref = _relative(html_path, source_root)
        for finding in findings:
            snapshot["inherited_slop"].append(
                {
                    "rule": finding["rule"],
                    "fingerprint": finding["fingerprint"],
                    "evidence": finding["evidence"],
                    "source": source_ref,
                }
            )
        if not findings:
            snapshot["gaps"].append(
                "existing page %s produced no inherited fingerprints" % source_ref
            )
    else:
        if not loaded_snapshot:
            snapshot["gaps"].append(
                "existing page HTML not scanned; inherited slop baseline unknown"
            )

    if not loaded_snapshot:
        if not any(snapshot["tokens"][group] for group in TOKEN_GROUPS):
            snapshot["evidence"] = "inferred"
            snapshot["gaps"].append(
                "no tokens captured; supply the visual system via --extra and confirm at the gate"
            )
        if not snapshot["components"]:
            snapshot["gaps"].append(
                "no component recipes captured; supply them via --extra before generation"
            )
        if not snapshot["layout"]:
            snapshot["gaps"].append(
                "layout shell not captured; supply max width, gutters, nav model and density"
            )

    snapshot = _sort_snapshot(snapshot)
    snapshot["hash"] = _compute_hash(snapshot)
    _validate(snapshot)
    return snapshot


def make_card(snapshot, seed=None, name=None):
    """Return the FIT CARD for a validated snapshot."""
    digest = snapshot["hash"].split(":", 1)[1]
    if not seed:
        seed = "fit-" + digest[:8]
    direction_name = "Existing system"
    if name:
        direction_name += " — " + name
    return {
        "mode": "fit",
        "seed": seed,
        "algorithm": ALGORITHM,
        "direction_id": "FIT",
        "direction_name": direction_name,
        "family": "existing",
        "knobs": {},
        "filters": {"domain": None, "excluded": []},
        "wild": False,
        "snapshot": {"path": SNAPSHOT_NAME, "hash": snapshot["hash"]},
    }


def _write(path, text):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Capture an existing visual system as a fit-mode snapshot.",
    )
    parser.add_argument("--from", dest="source", help="repo path, CSS/token file or URL")
    parser.add_argument("--extra", help="authored JSON sections (components, layout, ...)")
    parser.add_argument("--out", help="write style-snapshot.json to this path")
    parser.add_argument("--card", help="write the fit direction.json to this path")
    parser.add_argument("--seed", help="session seed (default fit-<hash8>)")
    parser.add_argument("--name", help="product name used in direction_name")
    parser.add_argument("--existing-html", help="existing page HTML for the slop baseline")
    parser.add_argument("--check", help="validate a snapshot and verify its hash")
    args = parser.parse_args(argv)

    if args.check:
        if args.source or args.extra or args.card or args.out:
            parser.error("--check is exclusive with capture flags")
        try:
            snapshot = json.loads(Path(args.check).read_text(encoding="utf-8"))
            _validate(snapshot, check_hash=True)
        except (SnapshotError, ValueError, OSError) as error:
            print("snapshot check failed: %s" % error, file=sys.stderr)
            return 1
        print(json.dumps({"ok": True, "hash": snapshot["hash"]}, sort_keys=True))
        return 0

    if not args.source and not args.extra:
        parser.error("--from or --extra is required (or use --check)")

    try:
        snapshot = capture(args.source, args.extra, args.existing_html)
    except (SnapshotError, ValueError, OSError, json.JSONDecodeError) as error:
        parser.error(str(error))

    text = _canonical(snapshot)
    if args.out:
        _write(args.out, text + "\n")
    elif args.card:
        # The card points at style-snapshot.json; keep the pair together.
        snapshot_path = Path(args.card).parent / SNAPSHOT_NAME
        _write(snapshot_path, text + "\n")
        print("snapshot: %s" % snapshot_path, file=sys.stderr)

    print(text)

    if args.card:
        card = make_card(snapshot, args.seed, args.name)
        _write(args.card, roll.dumps(card) + "\n")
        print("card: %s" % args.card, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
