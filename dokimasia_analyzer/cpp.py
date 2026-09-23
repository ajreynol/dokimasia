"""Small, deliberately partial C++ source helpers for syntactic checks.

Offsets and newlines survive masking. These helpers do not expand macros,
resolve types, or parse templates; callers must count unsupported forms as
unknown rather than interpreting an extraction failure as a clean check.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


_NONCODE = re.compile(
    r'//(?:\\\r?\n|[^\n])*|/\*[\s\S]*?\*/'
    r'|(?:u8|u|U|L)?R"([^ ()\\\t\r\n]{0,16})\([\s\S]*?\)\1"'
    r'|"(?:\\[\s\S]|[^"\\])*"|\'(?:\\[\s\S]|[^\'\\])*\'')


def mask(text: str) -> str:
    def replace(m):
        # A literal is still an expression, so keep a non-whitespace marker.
        value = ''.join('\n' if c == '\n' else ' ' for c in m.group())
        return value if m.group().startswith('/') else '0' + value[1:]
    return _NONCODE.sub(replace, text)


def closing(text: str, start: int) -> int | None:
    pairs = {'(': ')', '[': ']', '{': '}'}
    if start >= len(text) or text[start] not in pairs:
        return None
    stack = []
    for pos in range(start, len(text)):
        c = text[pos]
        if c in pairs:
            stack.append(pairs[c])
        elif c in ')]}':
            if not stack or stack.pop() != c:
                return None
            if not stack:
                return pos
    return None


def split(text: str) -> list[str] | None:
    """Split comma-separated expressions; ambiguous templates are unknown."""
    parts, start, pos = [], 0, 0
    while pos < len(text):
        c = text[pos]
        if c in '([{':
            end = closing(text, pos)
            if end is None:
                return None
            pos = end
        elif c in ')]}':
            return None
        elif c == '<' or (c == '>' and (pos == 0 or text[pos - 1] != '-')):
            return None
        elif c == ',':
            parts.append(text[start:pos].strip())
            start = pos + 1
        pos += 1
    parts.append(text[start:].strip())
    if not parts[-1]:  # empty list or a trailing initializer comma
        parts.pop()
    return None if any(not p for p in parts) else parts


def list_size(text: str) -> int | None:
    text = text.strip()
    if not text.startswith('{') or closing(text, 0) != len(text) - 1:
        return None
    parts = split(text[1:-1])
    return len(parts) if parts is not None else None


@dataclass(frozen=True)
class Function:
    name: str
    params: str
    start: int
    end: int


def functions(text: str) -> list[Function]:
    """Out-of-line qualified method definitions with an ordinary body."""
    out = []
    for m in re.finditer(r'\b(\w+(?:::\w+)+)\s*\(', text):
        end = closing(text, m.end() - 1)
        if end is None:
            continue
        tail = re.match(r'\s*(?:const\s*)?\{', text[end + 1:])
        if tail is None:
            continue
        start = end + tail.end()
        stop = closing(text, start)
        if stop is not None:
            out.append(Function(m[1], text[m.end():end], start, stop))
    return out


def calls(text: str, pattern: str):
    """Yield (match, end offset, arguments) for calls in already masked text."""
    for m in re.finditer(pattern + r'\s*\(', text):
        end = closing(text, m.end() - 1)
        if end is not None:
            yield m, end, split(text[m.end():end])
