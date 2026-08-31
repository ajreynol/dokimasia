"""Per-theory coverage: inferences produced, against inferences reconstructed.

Two sides, both read from source:

**produced** -- every `InferenceId` passed as a value, attributed to the theory
directory of the site that passes it. Reuses `dokimasia.inferid`, so the same
production/dispatch/comparison classification applies.

**reconstructed** -- the `case InferenceId::` labels in a theory's
`infer_proof_cons.cpp`. Its default case sets `ps.d_rule = ProofRule::TRUST`
with a `THEORY_INFERENCE_*` id, so an unnamed inference becomes a trust step.

An honest reading
-----------------
A theory with no `InferProofCons` is **not** thereby proofless. Several attach a
`ProofGenerator` at the inference site instead, which this does not see. So the
verdict for such a theory is *unknown by this mechanism*, never "no proofs", and
the tool says which of the two it is looking at.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

_CASE = re.compile(r"case\s+InferenceId::([A-Z][A-Z0-9_]*)\s*:")
_TRUST_FALLBACK = re.compile(r"ProofRule::TRUST\b")


@dataclass
class TheoryCoverage:
    theory: str
    produced: set[str] = field(default_factory=set)
    reconstructed: set[str] = field(default_factory=set)
    has_ipc: bool = False
    ipc_file: str = ""
    trust_fallback: bool = False

    @property
    def unhandled(self) -> list[str]:
        """Produced here, and this theory's reconstructor does not name it."""
        return sorted(self.produced - self.reconstructed)

    @property
    def reconstructed_not_produced(self) -> list[str]:
        """A case for an inference this theory never emits -- dead reconstruction."""
        return sorted(self.reconstructed - self.produced)

    @property
    def rate(self) -> float | None:
        if not self.has_ipc or not self.produced:
            return None
        return len(self.produced & self.reconstructed) / len(self.produced)


@dataclass
class Coverage:
    theories: dict[str, TheoryCoverage] = field(default_factory=dict)

    def with_reconstructor(self) -> list[TheoryCoverage]:
        return [t for t in self.theories.values() if t.has_ipc]

    def without_reconstructor(self) -> list[TheoryCoverage]:
        return [t for t in self.theories.values() if not t.has_ipc and t.produced]

    def total_unhandled(self) -> int:
        return sum(len(t.unhandled) for t in self.with_reconstructor())


#: Inference sites that belong to the theory framework rather than a theory.
CORE = "theory (core)"


def _theory_of(path: str) -> str | None:
    """Owning theory directory, or CORE for files sitting in `theory/` itself.

    `theory/theory_engine.cpp` has no owning theory; taking `parts[1]` blindly
    turns the filename into one, which is how this first reported a theory
    called `theory_engine.cpp`.
    """
    parts = path.split(os.sep)
    if not parts or parts[0] != "theory":
        return None
    if len(parts) == 2:
        return CORE
    return parts[1]


def scan(root: str) -> Coverage:
    src = os.path.join(root, "src") if os.path.isdir(os.path.join(root, "src")) else root
    if not os.path.isdir(src):
        raise SystemExit(f"not a cvc5 checkout: {root!r}")

    from ..inferid.scan import scan as iscan
    model = iscan(src)

    cov = Coverage()
    for ident in model.declared:
        for use in model.production(ident):
            th = _theory_of(use.path)
            if th is None:
                continue
            cov.theories.setdefault(th, TheoryCoverage(th)).produced.add(ident)

    # reconstructors
    for dirpath, _d, files in os.walk(os.path.join(src, "theory")):
        if "infer_proof_cons.cpp" not in files:
            continue
        path = os.path.join(dirpath, "infer_proof_cons.cpp")
        rel = os.path.relpath(path, src)
        th = _theory_of(rel)
        if th is None:
            continue
        with open(path, encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
        t = cov.theories.setdefault(th, TheoryCoverage(th))
        t.has_ipc = True
        t.ipc_file = rel
        t.reconstructed = set(_CASE.findall(text))
        t.trust_fallback = bool(_TRUST_FALLBACK.search(text))
    return cov
