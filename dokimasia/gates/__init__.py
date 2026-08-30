"""gates -- which option must be on for a term kind, and so for a rule, to occur.

Severity in this repository keeps running into one question: is this hole
reachable under `--safe-mode=safe`? Answering it needs the option gate, and the
gate is almost never at the site -- a proof step in `pow2_solver.cpp` carries no
`options()` guard at all.

The gate is on the *term kinds* instead, in two places cvc5 states plainly:
`illegal_checker.cpp`, and the `LogicException` throws in theory solvers. Both
are tables. Link them to rules through the kinds a rewriter names, and the
reachability question becomes answerable.
"""

from .gates import KindGates, gates_for, scan

__all__ = ["KindGates", "gates_for", "scan"]
