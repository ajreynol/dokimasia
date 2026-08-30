"""ci -- an independent check that cvc5's proof testing is still attached.

CI is what keeps cvc5's proofs complete today. A safety net that quietly stops
being attached looks exactly like one that is working: every job still passes.
This reads the workflow matrix and the regression runner and reports what is
actually being tested, so the answer does not depend on anyone remembering.
"""

from .scan import Job, Tester, CiModel, scan

__all__ = ["Job", "Tester", "CiModel", "scan"]
