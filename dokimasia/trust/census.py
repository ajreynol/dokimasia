"""Every construction site of every TrustId, and the preprocessing correspondence.

Trust steps reach a proof through several spellings -- ``mkTrustId``,
``addTrustedStep``, ``mkTrustNode``, ``mkTrustedNode``, ``TrustProofGenerator``
-- so rather than enumerate the callers, this records every place a ``TrustId``
is *passed as a value* and reports the enclosing subsystem. Same classification
as the InferenceId scan: a ``case`` label consumes an id, it does not create one.

The preprocessing correspondence
--------------------------------
The ``TrustId`` enum carries a ``PREPROCESS_*`` family that shadows
``src/preprocessing/passes/``. A pass with no id either produces real proofs or
is an undeclared hole, and an id with no pass is dead or misnamed -- both are
worth knowing, and the mapping is checkable without a build.
"""

from __future__ import annotations

import os
import re
from collections import defaultdict
from dataclasses import dataclass, field

_USE = re.compile(r"(?:(case)\s+|(==|!=)\s*)?\bTrustId::([A-Z][A-Z0-9_]*)")
_MEMBER = re.compile(r"^\s*([A-Z][A-Z0-9_]*)\s*(?:=[^,\n]*)?,?\s*(?://.*)?$", re.M)

_DEF_FILES = (os.path.join("proof", "trust_id.h"), os.path.join("proof", "trust_id.cpp"))

#: NONE is the absence of a reason, not a reason.
SENTINELS = frozenset({"NONE"})


@dataclass(frozen=True)
class TrustSite:
    ident: str
    path: str
    line: int
    kind: str      # definition | construction | dispatch | comparison

    @property
    def subsystem(self) -> str:
        parts = self.path.split(os.sep)
        return os.sep.join(parts[:2]) if len(parts) > 2 else parts[0]

    def where(self) -> str:
        return f"{self.path}:{self.line}"


@dataclass
class Census:
    declared: list[str] = field(default_factory=list)
    sites: dict[str, list[TrustSite]] = field(default_factory=lambda: defaultdict(list))
    passes: list[str] = field(default_factory=list)

    def construction(self, ident: str) -> list[TrustSite]:
        return [s for s in self.sites.get(ident, ()) if s.kind == "construction"]

    def live(self) -> list[str]:
        return [i for i in self.declared
                if i not in SENTINELS and self.construction(i)]

    def dead(self) -> list[str]:
        return [i for i in self.declared
                if i not in SENTINELS and not self.construction(i)]

    def anonymous(self) -> list[TrustSite]:
        """Trust steps introduced with no reason at all."""
        out: list[TrustSite] = []
        for i in SENTINELS:
            out.extend(self.construction(i))
        return out

    def by_subsystem(self) -> list[tuple[str, int, int]]:
        """(subsystem, distinct ids, construction sites), heaviest first."""
        ids: dict[str, set[str]] = defaultdict(set)
        n: dict[str, int] = defaultdict(int)
        for ident in self.declared:
            for s in self.construction(ident):
                ids[s.subsystem].add(ident)
                n[s.subsystem] += 1
        return sorted(((k, len(v), n[k]) for k, v in ids.items()),
                      key=lambda r: (-r[2], r[0]))

    # --- the preprocessing correspondence ---------------------------------

    def pass_correspondence(self) -> dict[str, list]:
        """Match each `preprocessing/passes/*` against the ids it constructs.

        Established from **construction sites, not names**. Matching by name
        does not work and the reason is itself a finding: nothing enforces that
        a pass's id is derivable from its filename, and one of them
        (`PREPROCESS_BV_GUASS`, for `bv_gauss`) is a misspelling of Gauss. So
        the mapping is taken from what each file actually builds.
        """
        owner: dict[str, set[str]] = {p: set() for p in self.passes}
        for ident in self.declared:
            for s in self.construction(ident):
                parts = s.path.split(os.sep)
                if len(parts) >= 3 and parts[0] == "preprocessing" and parts[1] == "passes":
                    stem = os.path.splitext(parts[2])[0]
                    if stem in owner:
                        owner[stem].add(ident)
        declares, silent = [], []
        for p in sorted(owner):
            if owner[p]:
                declares.append((p, sorted(owner[p])))
            else:
                silent.append(p)
        claimed = {i for v in owner.values() for i in v}
        orphan = sorted(i for i in self.declared
                        if i.startswith("PREPROCESS_") and i not in claimed)
        return {"declares": declares, "silent": silent, "orphan_id": orphan}

    def misnamed_pass_ids(self) -> list[tuple[str, str, str]]:
        """(pass, id it constructs, id its filename implies) where they differ."""
        out = []
        for p, ids in self.pass_correspondence()["declares"]:
            want = "PREPROCESS_" + p.upper()
            for i in ids:
                if i not in (want, want + "_LEMMA"):
                    out.append((p, i, want))
        return out


def _declared(src: str) -> list[str]:
    path = os.path.join(src, "proof", "trust_id.h")
    with open(path, encoding="utf-8", errors="ignore") as fh:
        text = fh.read()
    start = text.find("enum class TrustId")
    end = text.find("\n};", start)
    return _MEMBER.findall(text[start:end]) if start >= 0 else []


def census(root: str) -> Census:
    src = os.path.join(root, "src") if os.path.isdir(os.path.join(root, "src")) else root
    if not os.path.isdir(src):
        raise SystemExit(f"not a cvc5 checkout: {root!r}")

    c = Census(declared=_declared(src))
    known = set(c.declared)

    pdir = os.path.join(src, "preprocessing", "passes")
    if os.path.isdir(pdir):
        c.passes = sorted(f[:-2] for f in os.listdir(pdir) if f.endswith(".h"))

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
            if "TrustId::" not in text:
                continue
            is_def = rel in _DEF_FILES
            for m in _USE.finditer(text):
                is_case, cmp_op, ident = m.group(1), m.group(2), m.group(3)
                if ident not in known:
                    continue
                kind = ("definition" if is_def else
                        "dispatch" if is_case else
                        "comparison" if cmp_op else "construction")
                line = text.count("\n", 0, m.start()) + 1
                c.sites[ident].append(TrustSite(ident, rel, line, kind))
    return c
