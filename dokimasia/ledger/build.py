"""Assemble the proof-rule ledger from cvc5's own tables.

Every column is read out of source text -- no build required:

``declared``    ``EVALUE(...)`` entries in ``include/cvc5/cvc5_proof_rule.h``,
                which holds two enums: ``ProofRule`` and ``ProofRewriteRule``.
``produced``    ``ProofRule::X`` passed as a value somewhere in ``src/``.
``checked``     ``registerChecker`` / ``registerTrustedChecker`` call sites. The
                latter carries a *pedantic level*: cvc5's own statement of how
                much its checker really verifies.
``elaborated``  a ``ProofRule::MACRO_*`` named in ``smt/proof_post_processor*``.
``printed``     the ``EoPrinter::isHandled`` switch, three-valued.

Why printed is three-valued
---------------------------
``isHandled`` is not a list. Some arms return ``true`` outright; others inspect
the step's arguments and return a computed answer. So handledness is a property
of a rule *applied to particular arguments*, and the honest states are
``always``, ``never`` and ``conditional`` -- never a bare yes/no.

Fallthrough is handled the way C means it: a ``case`` label with no body shares
the outcome of the next label that has one.
"""

from __future__ import annotations

import os
import re
from collections import defaultdict
from dataclasses import dataclass, field

_EVALUE = re.compile(r"EVALUE\(([A-Z][A-Z0-9_]*)\)")
_REGISTER = re.compile(
    r"register(Trusted)?Checker\(\s*ProofRule::([A-Z][A-Z0-9_]*)\s*,([^;]*?)\)\s*;", re.S)
_USE = re.compile(r"(?:(case)\s+|(==|!=)\s*)?\bProofRule::([A-Z][A-Z0-9_]*)")
_CASE = re.compile(r"case\s+ProofRule::([A-Z][A-Z0-9_]*)\s*:")

SENTINELS = frozenset({"UNKNOWN", "LAST"})

#: Rules the Eunoia printer is *supposed* to reject, and why. Reporting these
#: as gaps would be noise: a macro is meant to be elaborated away before the
#: proof is printed, a trust step *is* the hole rather than a failure to print
#: one, and the other formats' rules are not Eunoia's business.
BY_DESIGN = {
    "TRUST": "a trust step is the hole itself, not a printing failure",
    "TRUST_THEORY_REWRITE": "as TRUST",
    "ALETHE_RULE": "belongs to the Alethe format",
    "LFSC_RULE": "belongs to the LFSC format",
}


@dataclass
class Row:
    """One proof rule, and what the pipeline does with it."""

    name: str
    produced: list[str] = field(default_factory=list)      # "file:line"
    checker: str | None = None                              # file:line
    pedantic: int | None = None                             # None = fully checked
    elaborated: list[str] = field(default_factory=list)
    printed: str = "never"                                  # always|conditional|never

    @property
    def is_macro(self) -> bool:
        return self.name.startswith("MACRO_")

    @property
    def unprintable_kind(self) -> str | None:
        """Why this rule is not printable, or None if it is.

        ``by-design``  a macro, a trust step, or another format's rule
        ``unreachable`` nothing produces it, so the gap cannot bite
        ``gap``        a rule the solver emits and the Eunoia seam cannot take
        """
        if self.printed != "never":
            return None
        # A rule the post-processor expands is gone before the proof is
        # printed, so the seam rejecting it is correct. SUBS is the case that
        # makes the MACRO_ prefix an insufficient test on its own.
        if self.name in BY_DESIGN or self.is_macro or self.elaborated:
            return "by-design"
        if not self.produced:
            return "unreachable"
        return "gap"

    @property
    def holes(self) -> list[str]:
        """The columns that are empty, as check codes."""
        out = []
        if not self.produced:
            out.append("RULE0003")           # declared, nothing produces it
        if self.checker is None:
            out.append("RULE0001")           # no registered checker
        if self.pedantic:
            out.append("RULE0002")           # checker does not fully check
        if self.is_macro and not self.elaborated:
            out.append("ELAB0001")           # macro nothing expands
        if self.unprintable_kind == "gap":
            out.append("SEAM0001")           # emitted, and the seam cannot take it
        return out


@dataclass
class Ledger:
    rules: dict[str, Row] = field(default_factory=dict)
    rewrite_rules: list[str] = field(default_factory=list)

    def rows(self) -> list[Row]:
        return [self.rules[n] for n in self.rules]

    def with_hole(self, code: str) -> list[Row]:
        return [r for r in self.rows() if code in r.holes]

    def unprintable(self) -> dict[str, list[Row]]:
        out: dict[str, list[Row]] = {"gap": [], "by-design": [], "unreachable": []}
        for r in self.rows():
            k = r.unprintable_kind
            if k:
                out[k].append(r)
        return out

    def producible(self) -> list[Row]:
        """Rules something actually emits -- the ones whose holes can bite."""
        return [r for r in self.rows() if r.produced]


def _declared(include_dir: str) -> tuple[list[str], list[str]]:
    """(ProofRule names, ProofRewriteRule names) from the public header."""
    path = os.path.join(include_dir, "cvc5", "cvc5_proof_rule.h")
    with open(path, encoding="utf-8", errors="ignore") as fh:
        text = fh.read()
    a = text.find("enum ENUM(ProofRule)")
    b = text.find("enum ENUM(ProofRewriteRule)")
    rules = _EVALUE.findall(text[a:b]) if a >= 0 else []
    end = text.find("\n};", b)
    rw = _EVALUE.findall(text[b:end]) if b >= 0 else []
    return ([r for r in rules if r not in SENTINELS],
            [r for r in rw if r not in SENTINELS])


def _parse_is_handled(src: str) -> dict[str, str]:
    """Rule -> always | conditional, from EoPrinter::isHandled.

    Rules absent from the result are ``never``.
    """
    path = os.path.join(src, "proof", "eo", "eo_printer.cpp")
    with open(path, encoding="utf-8", errors="ignore") as fh:
        text = fh.read()
    start = text.find("bool EoPrinter::isHandled")
    if start < 0:
        return {}
    # the function ends at the first line-start '}' after it
    end = text.find("\n}\n", start)
    body = text[start:end if end > 0 else len(text)]

    # split into (label, following-text) pairs, in order
    marks = [(m.group(1), m.start(), m.end()) for m in _CASE.finditer(body)]
    out: dict[str, str] = {}
    pending: list[str] = []
    for i, (name, _s, e) in enumerate(marks):
        nxt = marks[i + 1][1] if i + 1 < len(marks) else len(body)
        between = body[e:nxt]
        pending.append(name)
        stripped = re.sub(r"//.*|/\*.*?\*/", "", between, flags=re.S).strip()
        if not stripped:
            continue                      # empty: falls through to the next label
        verdict = "always" if re.match(r"^return\s+true\s*;", stripped) else "conditional"
        for p in pending:
            out[p] = verdict
        pending = []
    return out


def build(root: str) -> Ledger:
    """Build the ledger from a cvc5 checkout."""
    src = os.path.join(root, "src")
    inc = os.path.join(root, "include")
    if not (os.path.isdir(src) and os.path.isdir(inc)):
        raise SystemExit(f"not a cvc5 checkout: {root!r}")

    names, rw = _declared(inc)
    led = Ledger(rules={n: Row(name=n) for n in names}, rewrite_rules=rw)
    known = set(names)

    printed = _parse_is_handled(src)
    for n, verdict in printed.items():
        if n in led.rules:
            led.rules[n].printed = verdict

    uses: dict[str, list[str]] = defaultdict(list)
    for dirpath, _dirs, files in os.walk(src):
        for fn in files:
            if not fn.endswith((".cpp", ".h")):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, src)
            try:
                with open(full, encoding="utf-8", errors="ignore") as fh:
                    text = fh.read()
            except OSError:
                continue
            if "ProofRule::" not in text:
                continue

            for m in _REGISTER.finditer(text):
                trusted, name, rest = m.group(1), m.group(2), m.group(3)
                if name not in known:
                    continue
                row = led.rules[name]
                row.checker = f"{rel}:{text.count(chr(10), 0, m.start()) + 1}"
                if trusted:
                    lvl = re.findall(r",\s*(\d+)\s*$", rest.strip())
                    row.pedantic = int(lvl[0]) if lvl else 1

            is_printer = rel == os.path.join("proof", "eo", "eo_printer.cpp")
            is_post = rel.startswith(os.path.join("smt", "proof_post_processor"))
            for m in _USE.finditer(text):
                is_case, cmp_op, name = m.group(1), m.group(2), m.group(3)
                if name not in known:
                    continue
                line = text.count("\n", 0, m.start()) + 1
                where = f"{rel}:{line}"
                if is_post:
                    led.rules[name].elaborated.append(where)
                    continue
                if is_case or cmp_op or is_printer:
                    continue
                # a registration call is not a production site
                if re.search(r"register(Trusted)?Checker\(\s*$",
                             text[max(0, m.start() - 40): m.start()]):
                    continue
                uses[name].append(where)

    for name, sites in uses.items():
        led.rules[name].produced = sites
    return led
