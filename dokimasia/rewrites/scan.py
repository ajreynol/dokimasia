"""Classify every ProofRewriteRule, and measure the seam's coverage of them.

Sources, all read as text:

``include/cvc5/cvc5_proof_rule.h``   the ``ProofRewriteRule`` enum.
``src/theory/*/rewrites``            RARE definitions, named in kebab-case;
                                     the enum entry is the UPPER_SNAKE form.
``proof/eo/eo_printer.cpp``          ``isHandledTheoryRewrite``, which decides
                                     whether a hand-written theory rewrite can
                                     be printed.

A RARE-defined rule is *declarative*: the same definition drives cvc5 and the
Eunoia signature, so it is handled generically and is not the interesting case.
A hand-written rule is C++ the seam must be taught about one at a time, so the
ones it has not been taught are where a proof can fail to print.
"""

from __future__ import annotations

import glob
import os
import re
from dataclasses import dataclass, field

_EVALUE = re.compile(r"EVALUE\(([A-Z][A-Z0-9_]*)\)")
_RARE = re.compile(r"^\(define-(?:cond-)?rule\*?\s+([A-Za-z0-9_.\-]+)", re.M)
_CASE = re.compile(r"case\s+ProofRewriteRule::([A-Z][A-Z0-9_]*)\s*:")

SENTINELS = frozenset({"NONE"})


def rare_to_enum(name: str) -> str:
    """`bool-double-not-elim` -> `BOOL_DOUBLE_NOT_ELIM`."""
    return name.replace("-", "_").replace(".", "_").upper()


@dataclass
class RewriteRules:
    declared: list[str] = field(default_factory=list)
    rare: dict[str, str] = field(default_factory=dict)      # enum name -> file
    handled: dict[str, str] = field(default_factory=dict)   # enum name -> always|conditional
    unrestricted_only: set[str] = field(default_factory=set)
    implemented: dict[str, str] = field(default_factory=dict)  # enum name -> file

    @property
    def handwritten(self) -> list[str]:
        """Rules with no RARE definition: C++ the seam must be taught about."""
        return [r for r in self.declared
                if r not in SENTINELS and r not in self.rare]

    def rare_without_enum(self) -> list[str]:
        """RARE names that match no enum entry -- a naming drift check."""
        known = set(self.declared)
        return sorted(n for n in self.rare if n not in known)

    def unhandled_handwritten(self) -> list[str]:
        return [r for r in self.handwritten if r not in self.handled]

    def macro_gaps(self) -> list[str]:
        """Gaps that are MACRO_* rewrites.

        Like the MACRO ProofRules, these are meant to be elaborated into finer
        steps before the proof is printed, so the seam refusing them is
        expected -- *provided the elaboration succeeds*. That proviso is not
        free: reconstruction runs under a search budget
        (`--proof-rewrite-rcons-rec-limit`), and when it fails the macro step
        stays and the proof is incomplete. So these are conditional, not benign.
        """
        return [r for r in self.gaps() if r.startswith("MACRO_")]

    def hard_gaps(self) -> list[str]:
        """Gaps that are not macros: applied, unprintable, nothing to expand."""
        return [r for r in self.gaps() if not r.startswith("MACRO_")]

    def safe_mode_gaps(self) -> list[str]:
        """Applied rules the seam accepts *only* in an unrestricted build.

        Some `isHandledTheoryRewrite` arms are guarded by
        `opts.base.safeMode == options::SafeMode::UNRESTRICTED`, so safe mode --
        the one configuration that promises complete proofs -- is *stricter*
        at the seam than the default. If a rewriter applies one of these under
        `--safe-mode=safe`, the step cannot be printed.
        """
        return sorted(r for r in self.unrestricted_only if r in self.implemented)

    def gaps(self) -> list[str]:
        """Hand-written, implemented in a rewriter, and the seam refuses it.

        A hand-written rule that no `rewriteViaRule` implements cannot be
        applied through that path, so the seam not handling it costs nothing
        today. The rules that are both applicable and unprintable are the ones
        where a proof can fail to print.
        """
        return [r for r in self.unhandled_handwritten() if r in self.implemented]

    def declared_only(self) -> list[str]:
        """Hand-written, no RARE definition, and no rewriter implements them."""
        return [r for r in self.handwritten if r not in self.implemented]

    def by_theory(self, names: list[str]) -> dict[str, int]:
        """Group rule names by their leading theory-ish token."""
        out: dict[str, int] = {}
        for n in names:
            key = n.split("_")[0]
            if key == "MACRO":
                parts = n.split("_")
                key = "MACRO_" + (parts[1] if len(parts) > 1 else "")
            out[key] = out.get(key, 0) + 1
        return dict(sorted(out.items(), key=lambda kv: -kv[1]))


def _strip_comments(text: str) -> str:
    """Remove C++ comments.

    Block comments need DOTALL; line comments must *not* have it, or `//.*`
    eats the rest of the string. Doing both in one alternation under re.S was a
    real bug here: any switch arm whose body opened with a `//` comment looked
    empty, so it was read as a fallthrough and its labels were silently lost.
    """
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"//[^\n]*", "", text)


def _declared(include_dir: str) -> list[str]:
    path = os.path.join(include_dir, "cvc5", "cvc5_proof_rule.h")
    with open(path, encoding="utf-8", errors="ignore") as fh:
        text = fh.read()
    b = text.find("enum ENUM(ProofRewriteRule)")
    end = text.find("\n};", b)
    return [r for r in _EVALUE.findall(text[b:end]) if r not in SENTINELS]


def _rare(src: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for path in sorted(glob.glob(os.path.join(src, "theory", "*", "rewrites"))):
        rel = os.path.relpath(path, src)
        with open(path, encoding="utf-8", errors="ignore") as fh:
            for name in _RARE.findall(fh.read()):
                out[rare_to_enum(name)] = rel
    return out


def _handled(src: str) -> tuple[dict[str, str], set[str]]:
    """(rule -> always|conditional, rules the seam takes only when unrestricted)."""
    path = os.path.join(src, "proof", "eo", "eo_printer.cpp")
    with open(path, encoding="utf-8", errors="ignore") as fh:
        text = fh.read()
    # match the *definition*, not the call site 100 lines above it
    m = re.search(r"^bool EoPrinter::isHandledTheoryRewrite\b", text, re.M)
    if m is None:
        return {}, set()
    start = m.start()
    end = text.find("\n}\n", start)
    body = text[start: end if end > 0 else len(text)]
    # (name, label start, label end) -- the *start* of the next label bounds
    # this one's body. Using its end instead makes every fallthrough label look
    # like it has a body, which silently mis-groups the switch.
    marks = [(m.group(1), m.start(), m.end()) for m in _CASE.finditer(body)]
    out: dict[str, str] = {}
    unrestricted: set[str] = set()
    pending: list[str] = []
    for i, (name, _s, e) in enumerate(marks):
        nxt = marks[i + 1][1] if i + 1 < len(marks) else len(body)
        between = _strip_comments(body[e:nxt]).strip()
        pending.append(name)
        if not between:
            continue                       # falls through
        verdict = "always" if re.match(r"^return\s+true\s*;", between) else "conditional"
        restricted = "SafeMode::UNRESTRICTED" in between
        for p in pending:
            out[p] = verdict
            if restricted:
                unrestricted.add(p)
        pending = []
    return out, unrestricted


def _implemented(src: str) -> dict[str, str]:
    """ProofRewriteRule -> file, from every `rewriteViaRule` implementation.

    Each theory rewriter dispatches applicable rules through
    ``rewriteViaRule(ProofRewriteRule id, const Node& n)``. A rule with a case
    there can be applied; one without cannot reach a proof by that route.
    """
    out: dict[str, str] = {}
    for dirpath, _dirs, files in os.walk(src):
        for fn in files:
            if not fn.endswith(".cpp"):
                continue
            full = os.path.join(dirpath, fn)
            with open(full, encoding="utf-8", errors="ignore") as fh:
                text = fh.read()
            if "rewriteViaRule" not in text:
                continue
            rel = os.path.relpath(full, src)
            for m in re.finditer(r"::rewriteViaRule\b", text):
                end = text.find("\n}\n", m.start())
                body = text[m.start(): end if end > 0 else len(text)]
                for name in _CASE.findall(body):
                    out.setdefault(name, rel)
    return out


def scan(root: str) -> RewriteRules:
    src = os.path.join(root, "src")
    inc = os.path.join(root, "include")
    if not (os.path.isdir(src) and os.path.isdir(inc)):
        raise SystemExit(f"not a cvc5 checkout: {root!r}")
    handled, unrestricted = _handled(src)
    return RewriteRules(declared=_declared(inc), rare=_rare(src),
                        handled=handled, unrestricted_only=unrestricted,
                        implemented=_implemented(src))
