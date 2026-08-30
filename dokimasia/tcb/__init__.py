"""tcb — measure the trusted computing base of cvc5's internal proof checker.

The internal proof checker is the natural kernel candidate: it is the code that
decides whether a cvc5 proof is valid. Its value is inversely proportional to
how much of cvc5 it depends on -- a checker that transitively depends on the
rewriter and the theory solvers is checking cvc5 with cvc5.

This subtool measures that dependency closure, breaks it down by subsystem, and
identifies which single edges carry the most weight, so the closure can be
argued about and shrunk.
"""

from .closure import IncludeGraph, Closure, SEED_SETS

__all__ = ["IncludeGraph", "Closure", "SEED_SETS"]
