"""Recover each rule's arity from the C++ checker that validates it.

A rule's premise and argument counts are stated three times in cvc5: in the
`\\inferrule` doc comment, in the Eunoia signature, and — most authoritatively —
in the checker, which is the code that actually decides what is accepted.

The checker states arity in three ways, in decreasing order of confidence:

``Assert(children.size() == N)``   an exact count the author wrote down
``Assert(children.size() >= N)``   a minimum, so the rule is variadic
``children[K]``                    an index used, so the arity is at least K+1

Dispatch comes in two shapes — `if (id == ProofRule::X)` chains and
`switch`/`case` — and both appear in the tree, so both are handled.

This is *evidence*, not a specification. `Assert` compiles out in release
builds, so an assertion records what the author believed rather than what is
enforced; and a rule whose checker indexes nothing yields no bound at all.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from .. import source
from ..sanity import expect

_CHECK_FN = re.compile(r"\w+::checkInternal\s*\(")
_IF_RULE = re.compile(r"\b(?:else\s+)?if\s*\(\s*id\s*==\s*ProofRule::([A-Z][A-Z0-9_]*)\s*\)")
_CASE_RULE = re.compile(r"case\s+ProofRule::([A-Z][A-Z0-9_]*)\s*:")
_SIZE_EQ = re.compile(r"Assert\(\s*(children|args)\.size\(\)\s*==\s*(\d+)")
_SIZE_GE = re.compile(r"Assert\(\s*(children|args)\.size\(\)\s*(>=?)\s*(\d+)")
_EMPTY = re.compile(r"Assert\(\s*(children|args)\.empty\(\)")
_INDEX = re.compile(r"\b(children|args)\[(\d+)\]")


@dataclass
class Arity:
    """What the checker implies about one rule's shape."""
    rule: str
    file: str
    premises: object = None      # int | "variadic" | None (no evidence)
    arguments: object = None
    evidence: list[str] = field(default_factory=list)


def _blocks(text: str) -> list[tuple[int, int, str]]:
    out, stack, pending = [], [], ""
    for i, ch in enumerate(text):
        if ch == "{":
            stack.append((i, pending.strip())); pending = ""
        elif ch == "}":
            if stack:
                s, head = stack.pop()
                out.append((s, i, head))
            pending = ""
        elif ch == ";":
            pending = ""
        else:
            pending += ch
    return out


def _shape(body: str, which: str) -> tuple[object, list[str]]:
    ev: list[str] = []
    for m in _EMPTY.finditer(body):
        if m.group(1) == which:
            ev.append(f"Assert({which}.empty())")
            return 0, ev
    for m in _SIZE_EQ.finditer(body):
        if m.group(1) == which:
            ev.append(f"Assert({which}.size() == {m.group(2)})")
            return int(m.group(2)), ev
    for m in _SIZE_GE.finditer(body):
        if m.group(1) == which:
            # `size() > N` is a bound of N+1, not N. Keep the bound: `>= 3` is
            # compatible with a documented 4, and discarding N would turn
            # agreement into a false disagreement.
            n = int(m.group(3)) + (1 if m.group(2) == ">" else 0)
            ev.append(f"Assert({which}.size() {m.group(2)} {m.group(3)})")
            return f">={n}", ev
    idx = [int(m.group(2)) for m in _INDEX.finditer(body) if m.group(1) == which]
    if idx:
        ev.append(f"{which}[{max(idx)}] indexed")
        return f">={max(idx) + 1}", ev
    return None, ev


def scan_checkers(root: str) -> dict[str, Arity]:
    """ProofRule -> what its checker implies. First checker found wins."""
    src = os.path.join(root, "src")
    out: dict[str, Arity] = {}
    for dirpath, _d, files in os.walk(src):
        for fn in files:
            if not fn.endswith(".cpp"):
                continue
            path = os.path.join(dirpath, fn)
            text = source.read(path)
            if "checkInternal" not in text or "ProofRule::" not in text:
                continue
            rel = os.path.relpath(path, src)
            m = _CHECK_FN.search(text)
            if not m:
                continue
            body = text[m.start():]
            blocks = _blocks(body)
            # `if (id == ProofRule::X) { ... }`: the rule is named in the header
            for start, end, head in blocks:
                names = _IF_RULE.findall(head)
                if len(names) != 1:
                    continue
                inner = body[start:end]
                p, pe = _shape(inner, "children")
                a, ae = _shape(inner, "args")
                out.setdefault(names[0], Arity(names[0], rel, p, a, pe + ae))
            # `case ProofRule::X:` runs, bounded by the next case label
            marks = [(mm.group(1), mm.start(), mm.end())
                     for mm in _CASE_RULE.finditer(body)]
            for i, (name, _s, e) in enumerate(marks):
                nxt = marks[i + 1][1] if i + 1 < len(marks) else len(body)
                inner = body[e:nxt]
                if not inner.strip():
                    continue
                p, pe = _shape(inner, "children")
                a, ae = _shape(inner, "args")
                out.setdefault(name, Arity(name, rel, p, a, pe + ae))
    expect(len(out), 100, "rules with checker arity evidence",
           "`checkInternal` in the theory proof_checker.cpp files")
    return out


def agrees(doc, chk) -> bool | None:
    """Is a documented arity consistent with what the checker implies?

    ``None`` when the checker gives no evidence. Lower bounds (`>=N`) are
    treated as bounds, not as "must be variadic" — a documented count of 4 is
    perfectly consistent with `Assert(args.size() >= 3)`.
    """
    if chk is None:
        return None
    lo = hi = None
    if isinstance(doc, tuple):          # optional arguments: a range
        lo, hi = min(doc), max(doc)
    elif isinstance(doc, int) and doc >= 0:
        lo = hi = doc
    if isinstance(chk, str) and chk.startswith(">="):
        n = int(chk[2:])
        if doc == "variadic" or doc == -1:
            return True
        return None if hi is None else hi >= n
    if chk == "variadic":
        return doc in ("variadic", -1)
    if doc in ("variadic", -1):
        return False
    return None if lo is None else lo <= chk <= hi
