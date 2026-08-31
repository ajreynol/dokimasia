"""infer -- does every inference a theory makes have a proof reconstruction?

An `InferenceId` marks a lemma or conflict a theory emitted. For the proof to be
complete, something must turn that inference into proof steps. Where a theory
has an `InferProofCons`, that is a `switch` over ids, and its default case
builds a `TRUST` step -- so an id the switch does not name is, by construction,
a hole.

This is the completeness core: the other analyses ask what the pipeline can
express, this one asks what the solver actually does.
"""

from .coverage import Coverage, scan

__all__ = ["Coverage", "scan"]
