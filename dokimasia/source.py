"""One read of the cvc5 tree, shared by every scanner in the process.

Each subtool used to open and regex the same ~17 MB of `src/` for itself, so a
run of the eight ratchets read it eight times in eight processes. The scanners
are unchanged in what they compute; they just stop doing the I/O twice.

The cache is per-process and keyed by absolute path. That is deliberate: a
long-lived cache would have to answer "has the checkout changed underneath
me?", and an analysis whose answer depends on when it ran is not a measurement.
One process, one snapshot.
"""
from __future__ import annotations

import os

_TEXT: dict[str, str] = {}
_LIST: dict[tuple[str, tuple[str, ...]], list[str]] = {}

#: Directories no analysis here looks at, skipped during a walk. Kept small:
#: excluding something a scanner needs would silently narrow its answer.
SKIP = frozenset({".git", "build", "deps", "__pycache__"})


def read(path: str) -> str:
    """The file's text, decoded permissively, read at most once per process."""
    key = os.path.abspath(path)
    text = _TEXT.get(key)
    if text is None:
        with open(key, encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
        _TEXT[key] = text
    return text


def walk(root: str, exts: tuple[str, ...]) -> list[str]:
    """Every file under `root` with one of these extensions, sorted.

    Sorted because an analysis that reports sites in filesystem order produces
    a different diff on every machine, and the baselines are diffed.
    """
    key = (os.path.abspath(root), tuple(sorted(exts)))
    hit = _LIST.get(key)
    if hit is not None:
        return hit
    out: list[str] = []
    for dirpath, dirnames, filenames in os.walk(key[0]):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        for fn in filenames:
            if fn.endswith(exts):
                out.append(os.path.join(dirpath, fn))
    out.sort()
    _LIST[key] = out
    return out


def stats() -> tuple[int, int]:
    """(files cached, bytes cached) — for `dokimasia all` to report the saving."""
    return len(_TEXT), sum(len(v) for v in _TEXT.values())


def clear() -> None:
    _TEXT.clear()
    _LIST.clear()
