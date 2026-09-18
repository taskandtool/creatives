"""Shared helpers for the creatives scripts: the app root, the status
folders, reading and writing creative.md (frontmatter + body), the tiny
template language render.py uses, and the copy gate. Standard library only
(PyYAML is not assumed: the frontmatter subset here is what the scripts
write, and a full YAML file the AI writes by hand still parses as long as
it stays within that subset: scalars, lists, and one level of nested maps).
"""

import json
import os
import re
import sys
from datetime import datetime, timezone

STATUSES = ["generated", "approved", "scheduled", "posted", "rejected"]
PLATFORMS = ["meta", "linkedin", "tiktok", "google", "pinterest", "youtube", "gbp"]
KINDS = ["static", "carousel", "video", "post"]
ANGLES = ["outcome", "problem", "social-proof", "mechanism", "comparison"]
AWARENESS = ["cold", "warm", "hot"]

RATIOS = {
    "4:5": (1080, 1350),
    "1:1": (1080, 1080),
    "9:16": (1080, 1920),
    "1.91:1": (1200, 628),
    "2:3": (1000, 1500),
    "16:9": (1280, 720),
}


def root():
    """The app root: the folder holding creatives/ and CREATIVES.md, found
    upward from the working directory (so the scripts run from anywhere
    inside the app)."""
    d = os.path.abspath(os.getcwd())
    while True:
        if os.path.isfile(os.path.join(d, "CREATIVES.md")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return os.path.abspath(os.getcwd())
        d = parent


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def die(msg, code=1):
    print(msg, file=sys.stderr)
    sys.exit(code)


# ── frontmatter ─────────────────────────────────────────────────────────

def split_frontmatter(text):
    """(frontmatter_text, body) or ("", text) when there is none."""
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            return text[4:end], text[end + 4:].lstrip("\n")
    return "", text


def _parse_scalar(s):
    s = s.strip()
    if s == "" or s == "null" or s == "~":
        return None
    if s in ("true", "false"):
        return s == "true"
    if s.startswith('"') and s.endswith('"') and len(s) >= 2:
        try:
            return json.loads(s)
        except ValueError:
            return s[1:-1]
    if s.startswith("'") and s.endswith("'") and len(s) >= 2:
        return s[1:-1].replace("''", "'")
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        return [_parse_scalar(x) for x in _split_top(inner)] if inner else []
    if s.startswith("{") and s.endswith("}"):
        inner = s[1:-1].strip()
        out = {}
        for part in _split_top(inner):
            if ":" in part:
                k, v = part.split(":", 1)
                out[k.strip().strip('"')] = _parse_scalar(v)
        return out
    try:
        if re.fullmatch(r"-?\d+", s):
            return int(s)
        if re.fullmatch(r"-?\d+\.\d+", s):
            return float(s)
    except ValueError:
        pass
    return s


def _split_top(s):
    """Split on commas outside quotes, brackets and braces."""
    parts, depth, quote, cur = [], 0, None, ""
    escaped = False
    for ch in s:
        if quote:
            cur += ch
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            cur += ch
        elif ch in "[{":
            depth += 1
            cur += ch
        elif ch in "]}":
            depth -= 1
            cur += ch
        elif ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur)
    return parts


def parse_frontmatter(text):
    """A small YAML subset: `key: scalar`, `key: [a, b]`, `key: {a: 1}`,
    block lists of scalars or flow maps (`- { ... }`), and one level of
    nested maps (`copy:` followed by indented `key: value` lines).
    Comments after `#` outside quotes are dropped."""
    data = {}
    lines = [_strip_comment(l) for l in text.split("\n")]
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, rest = m.group(1), m.group(2)
        if rest.strip() != "":
            data[key] = _parse_scalar(rest)
            i += 1
            continue
        # block: list or map follows
        block = []
        i += 1
        while i < len(lines) and (lines[i].startswith("  ") or lines[i].startswith("\t") or not lines[i].strip()):
            if lines[i].strip():
                block.append(lines[i])
            i += 1
        if not block:
            data[key] = None
        elif block[0].lstrip().startswith("- "):
            items = []
            for b in block:
                b = b.strip()
                if b.startswith("- "):
                    items.append(_parse_scalar(b[2:]))
            data[key] = items
        else:
            sub = {}
            for b in block:
                mm = re.match(r"^\s+([A-Za-z_][\w-]*):\s*(.*)$", b)
                if mm:
                    sub[mm.group(1)] = _parse_scalar(mm.group(2))
            data[key] = sub
    return data


def _strip_comment(line):
    out, quote, escaped = "", None, False
    for ch in line:
        if quote:
            out += ch
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
            out += ch
        elif ch == "#":
            break
        else:
            out += ch
    return out.rstrip()


def _dump_scalar(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        return "[" + ", ".join(_dump_scalar(x) for x in v) + "]"
    if isinstance(v, dict):
        return "{ " + ", ".join(f"{k}: {_dump_scalar(x)}" for k, x in v.items()) + " }"
    s = str(v)
    return json.dumps(s, ensure_ascii=False)


def dump_frontmatter(data):
    """The inverse of parse_frontmatter for the shapes the scripts write."""
    out = []
    for key, v in data.items():
        if isinstance(v, dict) and v and not any(isinstance(x, (dict, list)) for x in v.values()):
            out.append(f"{key}:")
            for k, x in v.items():
                out.append(f"  {k}: {_dump_scalar(x)}")
        elif isinstance(v, list) and v and all(isinstance(x, dict) for x in v):
            out.append(f"{key}:")
            for x in v:
                out.append(f"  - {_dump_scalar(x)}")
        else:
            out.append(f"{key}: {_dump_scalar(v)}")
    return "\n".join(out) + "\n"


def read_record(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    fm, body = split_frontmatter(text)
    return parse_frontmatter(fm), body


def write_record(path, data, body):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("---\n" + dump_frontmatter(data) + "---\n\n" + body.rstrip("\n") + "\n")


# ── creatives on disk ───────────────────────────────────────────────────

def creative_dirs(app_root, statuses=None):
    """[(status, id, dir)] for every creative folder."""
    out = []
    for status in statuses or STATUSES:
        base = os.path.join(app_root, "creatives", status)
        if not os.path.isdir(base):
            continue
        for name in sorted(os.listdir(base)):
            d = os.path.join(base, name)
            if os.path.isdir(d) and os.path.isfile(os.path.join(d, "creative.md")):
                out.append((status, name, d))
    return out


def find_creative(app_root, cid):
    for status, name, d in creative_dirs(app_root):
        if name == cid:
            return status, d
    return None, None


# ── the template language (a mustache subset) ───────────────────────────

def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def render_template(tpl, ctx):
    """`{{name}}` escaped, `{{{name}}}` raw, `{{#name}}…{{/name}}` for a
    truthy value (iterating a list; a dict or scalar renders once with the
    value as context), `{{^name}}…{{/name}}` when falsy, `{{.}}` the
    current scalar in a list."""
    section = re.compile(r"{{([#^])([\w.-]+)}}(.*?){{/\2}}", re.S)

    def resolve(name, scopes):
        if name == ".":
            return scopes[-1]
        for scope in reversed(scopes):
            if isinstance(scope, dict) and name in scope:
                return scope[name]
        return None

    def expand(text, scopes):
        def sec(m):
            kind, name, inner = m.group(1), m.group(2), m.group(3)
            val = resolve(name, scopes)
            if kind == "^":
                return expand(inner, scopes) if not val else ""
            if not val:
                return ""
            if isinstance(val, list):
                return "".join(expand(inner, scopes + [v]) for v in val)
            if isinstance(val, dict):
                return expand(inner, scopes + [val])
            return expand(inner, scopes)

        text = section.sub(sec, text)
        text = re.sub(r"{{{([\w.-]+)}}}", lambda m: str(resolve(m.group(1), scopes) or ""), text)
        text = re.sub(r"{{([\w.-]+)}}", lambda m: _esc(resolve(m.group(1), scopes) if resolve(m.group(1), scopes) is not None else ""), text)
        return text

    return expand(tpl, [ctx])


# ── the copy gate (the writing rules, greppable) ────────────────────────

COPY_TELLS = [
    r"\bin today'?s (fast-paced|digital|competitive|ever-changing) world\b",
    r"\bin a world where\b", r"\bimagine a world\b", r"\bwelcome to (our|my|the)\b",
    r"\bhere'?s the thing\b", r"\band honestly\?", r"\byou know what'?s wild\b", r"\bthat changes everything\b",
    r"\bwhether you'?re\b", r"\blook no further\b", r"\blet'?s dive in\b",
    r"\bsay goodbye to\b", r"\bto the next level\b", r"\bdon'?t just \w+, \w+",
    r"\bgame-?changer\b", r"\ball-in-one\b", r"\bseamless(ly)?\b", r"\bcutting-edge\b",
    r"\b(unlock|unleash|elevate|revolutioni[sz]e|supercharge) your\b", r"\bleverage\b",
    r"\bwe'?re passionate about\b", r"\bwe pride ourselves\b", r"\bwe do things differently\b",
    r"\bstands? as a testament\b", r"\bevolving landscape\b", r"\bnestled in\b", r"\bin the heart of\b",
    r"\bit'?s not (just )?(about )?\w+[,.;] it'?s\b", r"\bnot just \w+(?: \w+)?, but\b",
    r"\blearn more\b",
]
PERSONAL_ATTRIBUTES = [
    r"\b(struggling|suffering) with\b", r"\bdo you have (diabetes|anxiety|depression|debt|acne)\b",
    r"\byour (weight|debt|depression|anxiety|diabetes|condition|diagnosis|credit score)\b",
    r"\bare you (overweight|bankrupt|depressed|in debt|pregnant)\b",
    r"\bother (christians|muslims|jews|gay|lesbian|black|asian|latino|hispanic) (people|men|women)\b",
]


def copy_findings(text, ad=True):
    """[(rule, match)] for the phrases the writing skill refuses and, for
    an ad, the phrasings Meta's personal-attributes rule refuses."""
    out = []
    if not text:
        return out
    if "—" in text:
        out.append(("em dash", "—"))
    for rx in COPY_TELLS:
        m = re.search(rx, text, re.I)
        if m:
            out.append(("refused phrase", m.group(0)))
    if ad:
        for rx in PERSONAL_ATTRIBUTES:
            m = re.search(rx, text, re.I)
            if m:
                out.append(("personal attribute (Meta policy)", m.group(0)))
    return out
