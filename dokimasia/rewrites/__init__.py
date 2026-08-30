"""rewrites -- coverage of cvc5's rewrite vocabulary.

`ProofRewriteRule` is the largest vocabulary in the proof calculus and it has
two halves. Most entries are generated from RARE files -- the declarative
`src/theory/*/rewrites` -- and reach a proof as DSL_REWRITE steps that the
Eunoia seam handles generically. The rest are hand-written theory rewrites that
reach a proof as THEORY_REWRITE, and the seam takes them only if
`isHandledTheoryRewrite` says so.

The coverage question is about that second half.
"""

from .scan import RewriteRules, scan

__all__ = ["RewriteRules", "scan"]
