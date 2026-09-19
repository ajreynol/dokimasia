"""signature -- does the Eunoia signature agree with cvc5's own account of a rule?

cvc5 states each proof rule three times: in the documentation comment above the
enum entry, in the C++ checker that validates it, and -- via the Eunoia printer
-- in `Cpc.eo`, which is what `ethos` will actually check against. Two
implementations of one calculus is how a second implementation earns its keep,
but only if someone compares them.

The signature is not our subject; it is a reference. A disagreement is reported
as a fact about the C++ side or the seam between them.
"""

from .compare import Signature, scan

__all__ = ["Signature", "scan"]
