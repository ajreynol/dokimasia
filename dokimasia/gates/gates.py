"""Recover the option gate on each term kind, and hence on each rewrite rule.

Two sources, both hand-maintained tables that happen to be written in C++:

``smt/illegal_checker.cpp``
    ``if (... && !options().dom.opt) { d_illegalKinds.insert(Kind::K); ... }``
    -- K may not appear in an assertion unless ``dom.opt`` is on.

theory ``ppRewrite`` / ``preRewrite`` guards
    ``if (!options().dom.opt) { if (k == Kind::K) throw LogicException(...); }``
    -- the same statement, made locally by a theory.

Linking kinds to rules
----------------------
A rewrite rule's ``rewriteViaRule`` arm names the kinds it applies to
(``if (n.getKind() == Kind::MATCH)``). If every kind an arm names is gated by
an option that safe mode turns off, the rule cannot fire in safe mode, and a
seam that refuses it costs nothing there.

This is evidence, not proof: an arm that names no kind gets no verdict, and a
kind can be introduced internally rather than parsed from input. Verdicts are
``blocked``, ``open`` or ``unknown``, and ``unknown`` is the honest common case.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

_INSERT = re.compile(r"d_illegalKinds\.insert\(Kind::([A-Z][A-Z0-9_]*)\)")
_OPT = re.compile(r"!\s*options\(\)\.([a-zA-Z]+)\.([a-zA-Z][a-zA-Z0-9_]*)")
_KIND = re.compile(r"\bKind::([A-Z][A-Z0-9_]*)")
_CASE_RW = re.compile(r"case\s+ProofRewriteRule::([A-Z][A-Z0-9_]*)\s*:")

#: Options safe mode turns off, from SetDefaults::setDefaultsPre. Kept here as
#: a small literal rather than importing the modes tool, so the two agree by
#: review instead of by coupling; `dokimasia.modes delta` prints the live list.
SAFE_MODE_DISABLES = frozenset({
    "sep", "bags", "ff", "fp", "ufHoExp", "ufCardExp", "datatypesExp",
    "arithExp", "relsExp", "setsCardExp", "fpExp", "arraysExp", "setsExp",
    "nlCov", "ufSymmetryBreaker", "cegqiBv", "varEntEqElimQuant",
})


@dataclass
class KindGates:
    #: Kind -> options that must be enabled for it to be legal
    kind_gate: dict[str, set[str]] = field(default_factory=dict)
    #: where each gate was found
    origin: dict[str, str] = field(default_factory=dict)
    #: ProofRewriteRule -> kinds its rewriteViaRule arm names
    rule_kinds: dict[str, set[str]] = field(default_factory=dict)

    def gated_in_safe_mode(self, kind: str) -> str | None:
        """The safe-mode-disabled option gating this kind, if any."""
        for opt in self.kind_gate.get(kind, ()):
            if opt in SAFE_MODE_DISABLES:
                return opt
        return None

    def verdict(self, rule: str) -> tuple[str, str]:
        """(blocked | partial | open | unknown, why) for a rule in safe mode.

        The three-way split exists because an arm's kinds may be *alternatives*
        (`k == A || k == B`) or *conjoined requirements*
        (`k == SELECT && n[0].getKind() == STORE_ALL`), and telling those apart
        syntactically is more than this is worth.

        ``blocked``  every kind named is gated -- blocked either way.
        ``partial``  some are. If the arm is conjunctive it is blocked; if
                     disjunctive it is not. Read the arm.
        ``open``     none is gated: nothing here stops the rule firing in safe
                     mode.
        """
        kinds = self.rule_kinds.get(rule) or set()
        if not kinds:
            return "unknown", "its rewriteViaRule arm names no term kind"
        gated = {k: self.gated_in_safe_mode(k) for k in sorted(kinds)}
        blocked = {k: v for k, v in gated.items() if v}
        free = [k for k, v in gated.items() if not v]
        if not free:
            return "blocked", ", ".join(f"{k} needs --{v}" for k, v in blocked.items())
        if blocked:
            return "partial", (
                ", ".join(f"{k} needs --{v}" for k, v in blocked.items())
                + "; ungated: " + ", ".join(free))
        return "open", "no safe-mode gate on " + ", ".join(free)


def _blocks(text: str) -> list[tuple[int, int, str]]:
    """(start, end, header) for each braced block, with the text preceding it."""
    out, stack, pending = [], [], ""
    for i, ch in enumerate(text):
        if ch == "{":
            stack.append((i, pending.strip()))
            pending = ""
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


def _from_illegal_checker(src: str, kg: KindGates) -> None:
    path = os.path.join(src, "smt", "illegal_checker.cpp")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8", errors="ignore") as fh:
        text = fh.read()
    for start, end, head in _blocks(text):
        body = text[start:end]
        if "d_illegalKinds.insert" not in body:
            continue
        opts = {m.group(2) for m in _OPT.finditer(head)}
        if not opts:
            continue
        for m in _INSERT.finditer(body):
            # only kinds inserted directly in this block, not a nested one
            kg.kind_gate.setdefault(m.group(1), set()).update(opts)
            kg.origin.setdefault(m.group(1), "smt/illegal_checker.cpp")


def _from_logic_exceptions(src: str, kg: KindGates) -> None:
    """Theory-local `if (!options().x) { if (k == Kind::K) throw LogicException }`."""
    for dirpath, _dirs, files in os.walk(os.path.join(src, "theory")):
        for fn in files:
            if not fn.endswith(".cpp"):
                continue
            full = os.path.join(dirpath, fn)
            with open(full, encoding="utf-8", errors="ignore") as fh:
                text = fh.read()
            if "LogicException" not in text or "options()." not in text:
                continue
            rel = os.path.relpath(full, src)
            for start, end, head in _blocks(text):
                body = text[start:end]
                if "LogicException" not in body:
                    continue
                opts = {m.group(2) for m in _OPT.finditer(head)}
                if not opts:
                    continue
                for m in _KIND.finditer(body):
                    kg.kind_gate.setdefault(m.group(1), set()).update(opts)
                    kg.origin.setdefault(m.group(1), rel)


def _rule_kinds(src: str, kg: KindGates) -> None:
    for dirpath, _dirs, files in os.walk(src):
        for fn in files:
            if not fn.endswith(".cpp"):
                continue
            full = os.path.join(dirpath, fn)
            with open(full, encoding="utf-8", errors="ignore") as fh:
                text = fh.read()
            if "rewriteViaRule" not in text:
                continue
            for m in re.finditer(r"::rewriteViaRule\b", text):
                end = text.find("\n}\n", m.start())
                body = text[m.start(): end if end > 0 else len(text)]
                marks = [(mm.group(1), mm.start(), mm.end())
                         for mm in _CASE_RW.finditer(body)]
                for i, (name, _s, e) in enumerate(marks):
                    nxt = marks[i + 1][1] if i + 1 < len(marks) else len(body)
                    kinds = set(_KIND.findall(body[e:nxt]))
                    if kinds:
                        kg.rule_kinds.setdefault(name, set()).update(kinds)


def scan(root: str) -> KindGates:
    src = os.path.join(root, "src") if os.path.isdir(os.path.join(root, "src")) else root
    if not os.path.isdir(src):
        raise SystemExit(f"not a cvc5 checkout: {root!r}")
    kg = KindGates()
    _from_illegal_checker(src, kg)
    _from_logic_exceptions(src, kg)
    _rule_kinds(src, kg)
    return kg


def gates_for(kg: KindGates, kind: str) -> set[str]:
    return kg.kind_gate.get(kind, set())
