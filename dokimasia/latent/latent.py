"""Cross the static hole inventory against what a corpus actually reached."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field

from ..fragment.fragment import THEORY_OPTIONS
from ..fragment.fragment import scan as fscan
from ..infer.coverage import scan as iscan
from ..ledger.build import build as lbuild
from ..rewrites.scan import scan as rscan
from ..trust.census import census

#: Where a corpus census is recorded. Produced by `scripts/sweep_corpus`.
CENSUS = "reach-corpus.json"


class State:
    """How much we know about one declared hole.

    The three are not degrees of confidence in the same claim; they are
    different claims, and only the first is a defect.
    """
    #: reached under --safe-mode=safe. A contract violation: safe mode promises
    #: full proof support, and this hole was taken with an input in hand.
    SAFE = "reachable-in-safe-mode"
    #: reached, but only outside safe mode. Real, and nobody relying on safe
    #: mode is exposed to it.
    OPEN = "reached-unrestricted-only"
    #: declared, and no input we have run has ever reached it. **Not** a claim
    #: that it is unreachable -- it is the absence of evidence either way, and
    #: it is the population this repository exists to name.
    LATENT = "latent"


@dataclass
class Hole:
    kind: str          # trust-id | seam-rule | rewrite | inference
    name: str
    state: str
    detail: str = ""
    hits: int = 0

    @property
    def rank(self) -> int:
        return {State.SAFE: 1, State.LATENT: 2, State.OPEN: 3}[self.state]


@dataclass
class Latent:
    holes: list[Hole] = field(default_factory=list)
    corpus: str = ""
    have_census: bool = False

    def by_state(self, state: str) -> list[Hole]:
        return sorted((h for h in self.holes if h.state == state),
                      key=lambda h: (h.kind, h.name))

    def by_kind(self) -> dict[str, dict[str, int]]:
        out: dict[str, dict[str, int]] = {}
        for h in self.holes:
            out.setdefault(h.kind, {}).setdefault(h.state, 0)
            out[h.kind][h.state] += 1
        return out


def _census(root: str) -> tuple[dict, dict, bool]:
    """(safe counters, unrestricted counters, found) from the recorded sweep."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", CENSUS)
    if not os.path.exists(path):
        return {}, {}, False
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    return (d.get("safe", {}).get("counters", {}),
            d.get("unrestricted", {}).get("counters", {}), True)


def provenance(root: str = "") -> dict:
    """What build and corpus produced the recorded census, if it says."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", CENSUS)
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return json.load(fh).get("_provenance", {})


def _state(name: str, safe: dict, unres: dict, keys: tuple[str, ...]) -> tuple[str, int]:
    for k in keys:
        if name in safe.get(k, {}):
            return State.SAFE, safe[k][name]
    for k in keys:
        if name in unres.get(k, {}):
            return State.OPEN, unres[k][name]
    return State.LATENT, 0


def scan(root: str) -> Latent:
    safe, unres, have = _census(root)
    out = Latent(corpus="regress0", have_census=have)

    # 1. every TrustId that is constructed somewhere
    c = census(root)
    swept = set(THEORY_OPTIONS)
    for tid in c.live():
        st, n = _state(tid, safe, unres, ("trustCount",))
        ths = {s.subsystem.split(os.sep)[1] for s in c.construction(tid)
               if s.subsystem.startswith("theory" + os.sep)}
        why = ""
        if st == State.LATENT and ths and ths <= swept:
            why = f"every site is in a theory safe mode sweeps ({', '.join(sorted(ths))})"
        out.holes.append(Hole("trust-id", tid, st, why, n))

    # 2. every ProofRule the solver emits that the seam refuses
    led = lbuild(root)
    for row in led.unprintable()["gap"]:
        rule = row.name
        st, n = _state(rule, safe, unres, ("ruleUnhandledEoCount",))
        out.holes.append(Hole("seam-rule", rule, st, "", n))

    # 3. every rewrite applied and unprintable
    r = rscan(root)
    for rw in sorted(set(r.hard_gaps()) | set(r.macro_gaps())):
        st, n = _state(rw.lower().replace("_", "-"), safe, unres,
                       ("theoryRewriteRuleUnhandledEoCount",))
        out.holes.append(Hole("rewrite", rw, st, "", n))

    # 4. every inference falling through to a trust step by construction.
    # The counters key trust steps by TrustId, never by InferenceId, so the
    # corpus cannot confirm or deny an individual one: they are all latent by
    # the measurement's construction, and saying so is the honest report.
    f = fscan(root)
    for t in iscan(root).with_reconstructor():
        for i in t.unhandled:
            why = ("no counter keys trust steps by InferenceId, so the corpus "
                   "cannot see this one either way")
            if t.theory in swept:
                why = f"theory {t.theory} is swept in safe mode"
            out.holes.append(Hole("inference", f"{t.theory}:{i}", State.LATENT, why))
    return out
