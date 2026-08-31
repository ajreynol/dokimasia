"""The supported fragment, per theory, and whether it is enforced.

Sources
-------
``src/theory/*/kinds.toml``   the authoritative kind inventory: every `Kind`,
                              which theory owns it, and what sort of thing it is.
``smt/illegal_checker.cpp``   two deny lists and a whole-theory sweep.
theory ``LogicException`` guards   the same statement made locally.

The three enforcement mechanisms
--------------------------------
1. **whole-theory sweep** -- for FP, FF, BAGS and SEP, `illegal_checker`
   iterates every `Kind` and blocks the ones belonging to a disabled theory.
   Complete by construction: nothing can be forgotten.
2. **per-kind deny list** -- `d_illegalKinds.insert(Kind::K)` under an option
   condition. **Hand-maintained**, one kind at a time, and the only mechanism
   covering the `*Exp` expert extensions.
3. **theory-local guards** -- a theory throws `LogicException` from `ppRewrite`
   when it sees a kind its expert option gates.

`illegal_checker.cpp` says so itself: *"nearly all illegal kinds should be
properly guarded by either the theory engine, theory solvers, or by theory
rewriters. We only require special handling for rare cases."* So mechanism 2 is
deliberately a supplement, and this tool reports coverage rather than
pronouncing a gap: a kind with no visible gate may be enforced somewhere this
does not read.
"""

from __future__ import annotations

import glob
import os
import re
from dataclasses import dataclass, field
from ..sanity import expect

_KIND_BLOCK = re.compile(r"^\[\[kinds\]\](.*?)(?=^\[\[|\Z)", re.M | re.S)
_NAME = re.compile(r'^\s*name\s*=\s*"([A-Z][A-Z0-9_]*)"', re.M)
_TYPE = re.compile(r'^\s*type\s*=\s*"(\w+)"', re.M)
_THEORY_ID = re.compile(r'^\s*id\s*=\s*"(THEORY_\w+)"', re.M)

#: Theories safe mode disables outright, and the option that does it.
THEORY_OPTIONS = {"fp": "fp", "ff": "ff", "bags": "bags", "sep": "sep"}

#: Expert extensions safe mode disables. These are gated kind-by-kind, or not
#: at all -- which is the question this tool exists to ask.
EXPERT_OPTIONS = frozenset({
    "arithExp", "arraysExp", "datatypesExp", "setsExp", "setsCardExp",
    "relsExp", "ufHoExp", "ufCardExp", "fpExp",
})

#: Options whose restriction is not on a term kind at all, verified by reading
#: the guard. Curated rather than inferred: there are two, the shapes differ,
#: and a heuristic that guessed them would be less trustworthy than a note.
NONKIND_AXIS = {
    "ufHoExp": ("logic", "theory/uf/theory_uf.cpp",
                "throws when logicInfo().isHigherOrder() and the option is off, "
                "so the restriction is on the declared logic, not on any kind"),
    "fpExp": ("type", "theory/fp/theory_fp.cpp",
              "calls checkForExperimentalFloatingPointType on each term, so the "
              "restriction is on the sort, which has kind TYPE_CONSTANT and "
              "cannot be excluded by kind"),
}

#: Kind `type` values that denote a *type constructor* rather than a term.
TYPE_LIKE = frozenset({"sort", "cardinality", "well-founded"})


@dataclass
class Fragment:
    #: theory directory -> THEORY_ID
    theory_id: dict[str, str] = field(default_factory=dict)
    #: Kind -> (theory directory, kind type)
    kinds: dict[str, tuple[str, str]] = field(default_factory=dict)
    #: Kind -> options that must be on for it to be legal
    kind_gate: dict[str, set[str]] = field(default_factory=dict)
    #: Kind -> where the gate was found
    origin: dict[str, str] = field(default_factory=dict)
    #: options named in the whole-theory sweep
    swept_theories: set[str] = field(default_factory=set)
    #: option -> (axis, file) when it gates something other than a term kind
    nonkind_gate: dict[str, tuple[str, str]] = field(default_factory=dict)

    def by_theory(self) -> dict[str, list[str]]:
        out: dict[str, list[str]] = {}
        for k, (th, _t) in sorted(self.kinds.items()):
            out.setdefault(th, []).append(k)
        return out

    def blocked_in_safe_mode(self, kind: str) -> tuple[bool, str]:
        """(blocked, mechanism) for a kind under --safe-mode=safe."""
        theory = self.kinds.get(kind, ("", ""))[0]
        if theory in THEORY_OPTIONS:
            return True, f"whole-theory sweep ({THEORY_OPTIONS[theory]} disabled)"
        gates = self.kind_gate.get(kind, set())
        expert = sorted(g for g in gates if g in EXPERT_OPTIONS)
        if expert:
            return True, f"deny list ({', '.join(expert)}) via {self.origin.get(kind, '?')}"
        return False, ""

    def expert_coverage(self) -> dict[str, list[str]]:
        """Expert option -> the kinds any mechanism gates on it."""
        out: dict[str, list[str]] = {o: [] for o in sorted(EXPERT_OPTIONS)}
        for k, gates in self.kind_gate.items():
            for g in gates:
                if g in out:
                    out[g].append(k)
        return {o: sorted(v) for o, v in out.items()}

    def uncovered_expert_options(self) -> list[tuple[str, str, str]]:
        """(option, axis, where) for expert options that gate no term kind.

        The fragment is not expressible as a kind list alone: an option may
        restrict the *logic* (higher-order) or a *type* (experimental
        floating-point sorts) instead. Those are real restrictions that no kind
        table records, which is the point worth reporting.
        """
        out = []
        for o, ks in self.expert_coverage().items():
            if ks:
                continue
            if o in NONKIND_AXIS:
                axis, where, _why = NONKIND_AXIS[o]
            else:
                axis, where = self.nonkind_gate.get(o, ("unknown", "—"))
            out.append((o, axis, where))
        return out

    def safe_fragment(self, theory: str) -> tuple[list[str], list[str]]:
        """(available, blocked) term kinds of a theory under safe mode."""
        avail, blocked = [], []
        for k in self.by_theory().get(theory, []):
            if self.kinds[k][1] in TYPE_LIKE:
                continue
            (blocked if self.blocked_in_safe_mode(k)[0] else avail).append(k)
        return avail, blocked


def _kinds(src: str, f: Fragment) -> None:
    for path in sorted(glob.glob(os.path.join(src, "theory", "*", "kinds.toml"))):
        theory = os.path.basename(os.path.dirname(path))
        with open(path, encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
        tid = _THEORY_ID.search(text)
        if tid:
            f.theory_id[theory] = tid.group(1)
        for block in _KIND_BLOCK.findall(text):
            nm = _NAME.search(block)
            ty = _TYPE.search(block)
            if nm:
                f.kinds[nm.group(1)] = (theory, ty.group(1) if ty else "?")
    expect(len(f.kinds), 300, "term kinds",
           "the `[[kinds]]` blocks in theory/*/kinds.toml")


def scan(root: str) -> Fragment:
    src = os.path.join(root, "src") if os.path.isdir(os.path.join(root, "src")) else root
    if not os.path.isdir(src):
        raise SystemExit(f"not a cvc5 checkout: {root!r}")
    f = Fragment()
    _kinds(src, f)
    # reuse the gate tables the gates subtool already recovers
    from ..gates.gates import scan as gscan
    kg = gscan(root)
    f.kind_gate = kg.kind_gate
    f.origin = kg.origin
    f.swept_theories = set(THEORY_OPTIONS)
    f.nonkind_gate = kg.nonkind_gate
    return f
