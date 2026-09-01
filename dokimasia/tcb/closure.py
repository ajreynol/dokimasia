"""Include-graph closure over a cvc5 source tree.

What this measures, and what it does not
----------------------------------------
This computes the transitive closure of ``#include "..."`` edges from a set of
seed files. That is an **upper bound** on the trusted computing base, not the
TCB itself: including a header does not mean the code behind it executes during
proof checking. A precise TCB needs call-graph reachability, which needs a
build; see ``docs/tooling.md``.

The over-approximation is still the right thing to measure first. It is exact,
it needs no build, it is what a reader of the code has to hold in their head,
and it moves monotonically with the thing we actually care about. A closure
that shrinks is a kernel argument that got shorter.

Modes, and a negative result worth recording
--------------------------------------------
``headers`` (default)
    Follow header edges only: the surface the checker compiles against. This is
    the meaningful measure and it discriminates -- ``proof_rule_checker.cpp``
    alone closes over 3,543 lines, the full checker set over 41,446.

``exec`` (**not recommended**, kept so the result is reproducible)
    Additionally pull in the ``.cpp`` implementing each reached header, as a
    naive proxy for "what could execute". *It does not work.* Once any ``.cpp``
    enters the closure it includes further headers, whose ``.cpp`` files follow,
    and the closure saturates at cvc5's whole link unit. Measured: seeding from
    ``printer/printer.cpp`` (unrelated to proof checking) yields 383,760 lines,
    identical to seeding from ``proof/proof_rule_checker.cpp``. A measure that
    returns the same answer for every seed measures nothing.

    The lesson is that "what could execute" is a **call-graph** question, not an
    include question, and belongs in the CodeQL tier -- see ``docs/tooling.md``.

Known under-approximation
-------------------------
Generated headers are invisible here: ``options/options.h`` is produced at build
time from the ``.toml`` files and is not in the source tree, so edges through it
are not followed. Figures are a lower bound in that respect.
"""

from __future__ import annotations
from .. import source

import os
import re
from dataclasses import dataclass, field

_INCLUDE = re.compile(r'^[ \t]*#[ \t]*include[ \t]+"([^"]+)"', re.M)

#: Named seed sets, so other kernels can be measured with the same machinery.
SEED_SETS: dict[str, tuple[str, ...]] = {
    # The internal proof checker: the dispatcher plus every registered rule
    # checker. This is the kernel candidate.
    "proof-checker": (
        "proof/proof_checker.cpp",
        "proof/proof_checker.h",
        "proof/proof_rule_checker.cpp",
        "proof/proof_rule_checker.h",
        "theory/*/proof_checker.cpp",
        "theory/*/*/proof_checker.cpp",
        "theory/*/*/*/proof_checker.cpp",
    ),
    # The Eunoia seam: what it takes to turn a cvc5 proof into an ethos proof.
    "eo-printer": (
        "proof/eo/*.cpp",
        "proof/eo/*.h",
    ),
    # Proof construction and post-processing, for contrast with the checker.
    "proof-core": (
        "proof/*.cpp",
        "proof/*.h",
    ),
}


def _expand(src: str, patterns: tuple[str, ...]) -> list[str]:
    """Expand seed glob patterns to src-relative paths that exist."""
    import glob as _glob

    out: list[str] = []
    for pat in patterns:
        for hit in sorted(_glob.glob(os.path.join(src, pat))):
            out.append(os.path.relpath(hit, src))
    return out


@dataclass
class IncludeGraph:
    """The ``#include`` graph of a cvc5 ``src/`` tree."""

    src: str
    edges: dict[str, list[str]] = field(default_factory=dict)
    lines: dict[str, int] = field(default_factory=dict)

    @classmethod
    def build(cls, src: str) -> "IncludeGraph":
        g = cls(src=src)
        for root, _dirs, files in os.walk(src):
            for fn in files:
                if not fn.endswith((".cpp", ".h", ".cc", ".hpp")):
                    continue
                path = os.path.join(root, fn)
                rel = os.path.relpath(path, src)
                try:
                    text = source.read(path)
                except OSError:
                    continue
                g.lines[rel] = text.count("\n") + 1
                g.edges[rel] = [h for h in _INCLUDE.findall(text) if h in g.lines or True]
        # Drop include targets that are not in this tree (system/third-party).
        for rel, incs in g.edges.items():
            g.edges[rel] = [h for h in incs if h in g.lines]
        return g

    def loc(self, files) -> int:
        return sum(self.lines.get(f, 0) for f in files)

    @property
    def all_files(self) -> list[str]:
        return list(self.lines)


@dataclass
class Closure:
    """A reachable set over an :class:`IncludeGraph`."""

    graph: IncludeGraph
    seeds: list[str]
    files: set[str]
    mode: str

    @classmethod
    def compute(
        cls,
        graph: IncludeGraph,
        seeds: list[str],
        mode: str = "exec",
        skip_edge: tuple[str, str] | None = None,
        skip_prefix: str | None = None,
    ) -> "Closure":
        seen: set[str] = set()
        stack = list(seeds)
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            for nxt in graph.edges.get(cur, ()):
                if skip_edge is not None and (cur, nxt) == skip_edge:
                    continue
                if skip_prefix is not None and nxt.startswith(skip_prefix):
                    continue
                if nxt not in seen:
                    stack.append(nxt)
                if mode == "exec" and nxt.endswith(".h"):
                    impl = nxt[:-2] + ".cpp"
                    if impl in graph.lines and impl not in seen:
                        stack.append(impl)
        return cls(graph=graph, seeds=list(seeds), files=seen, mode=mode)

    @property
    def loc(self) -> int:
        return self.graph.loc(self.files)

    def by_subsystem(self, depth: int = 1) -> list[tuple[str, int, int]]:
        """(subsystem, file count, line count), heaviest first."""
        agg: dict[str, list[int]] = {}
        for f in self.files:
            parts = f.split("/")
            key = "/".join(parts[:depth]) if len(parts) > depth else parts[0]
            slot = agg.setdefault(key, [0, 0])
            slot[0] += 1
            slot[1] += self.graph.lines.get(f, 0)
        return sorted(
            ((k, v[0], v[1]) for k, v in agg.items()), key=lambda r: -r[2]
        )

    def cuts(self, limit: int = 15) -> list[tuple[str, str, int, int]]:
        """Weigh each seed include edge by what leaves the closure without it.

        Returns ``(from, include, files_dropped, lines_dropped)`` heaviest
        first. These are the edges to argue about: the ones whose removal buys
        the most.
        """
        base_files = len(self.files)
        base_loc = self.loc
        out: list[tuple[str, str, int, int]] = []
        seen_edges: set[tuple[str, str]] = set()
        for seed in self.seeds:
            for inc in self.graph.edges.get(seed, ()):
                edge = (seed, inc)
                if edge in seen_edges:
                    continue
                seen_edges.add(edge)
                trimmed = Closure.compute(
                    self.graph, self.seeds, self.mode, skip_edge=edge
                )
                d_files = base_files - len(trimmed.files)
                d_loc = base_loc - trimmed.loc
                if d_files > 0:
                    out.append((seed, inc, d_files, d_loc))
        return sorted(out, key=lambda r: -r[3])[:limit]

    def subsystem_cuts(self, depth: int = 2) -> list[tuple[str, int, int]]:
        """Weigh each subsystem as a *cut set*.

        Single-edge cuts are near-useless on a dense include graph: almost
        everything is reachable by several paths, so removing one edge changes
        nothing. The question worth asking is the one a maintainer would
        actually argue: *if the checker did not reach into this subsystem at
        all, how much smaller would the TCB be?*

        Returns ``(subsystem, files_dropped, lines_dropped)``, heaviest first.
        """
        base_files = len(self.files)
        base_loc = self.loc
        subs = {r[0] for r in self.by_subsystem(depth)}
        out: list[tuple[str, int, int]] = []
        for s in subs:
            if any(seed.startswith(s + "/") for seed in self.seeds):
                continue  # the seeds live here; cutting it is meaningless
            trimmed = Closure.compute(
                self.graph, self.seeds, self.mode, skip_prefix=s + "/"
            )
            d_files = base_files - len(trimmed.files)
            d_loc = base_loc - trimmed.loc
            if d_files > 0:
                out.append((s, d_files, d_loc))
        return sorted(out, key=lambda r: -r[2])

    def path_to(self, target: str) -> list[str] | None:
        """Shortest include path from any seed to *target*, or None.

        This is the answer to "why is this in the TCB at all?" -- the thing
        you need in hand before you can argue for cutting it.
        """
        from collections import deque

        prev: dict[str, str | None] = {s: None for s in self.seeds}
        dq = deque(self.seeds)
        while dq:
            cur = dq.popleft()
            if cur == target:
                path = []
                node: str | None = cur
                while node is not None:
                    path.append(node)
                    node = prev[node]
                return list(reversed(path))
            for nxt in self.graph.edges.get(cur, ()):
                if nxt not in prev:
                    prev[nxt] = cur
                    dq.append(nxt)
                if self.mode == "exec" and nxt.endswith(".h"):
                    impl = nxt[:-2] + ".cpp"
                    if impl in self.graph.lines and impl not in prev:
                        prev[impl] = nxt
                        dq.append(impl)
        return None


def resolve_src(root: str) -> str:
    """Accept either a cvc5 checkout or its ``src/`` directory."""
    cand = os.path.join(root, "src")
    if os.path.isdir(cand):
        return cand
    if os.path.basename(os.path.normpath(root)) == "src":
        return root
    raise SystemExit(f"not a cvc5 checkout (no src/ under {root!r})")
