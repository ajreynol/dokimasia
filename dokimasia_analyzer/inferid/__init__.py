"""inferid -- enforce that an InferenceId names exactly one program point.

`InferenceId` is cvc5's informal proof marker: it is attached to essentially
every lemma and conflict a theory emits, and it is the closest thing cvc5 has to
a complete index of what inferences exist.

The contract is simple: **an id should be used in one place**. Then seeing it in
a trace, a statistic or a proof identifies a unique point in the control-flow
graph. An id used at three sites identifies three, which is to say it identifies
none of them, and every claim quantified over "the inferences theory X can make"
gets correspondingly weaker.
"""

from .scan import Use, InferenceIds, scan

__all__ = ["Use", "InferenceIds", "scan"]
