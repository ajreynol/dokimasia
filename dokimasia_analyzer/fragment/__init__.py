"""fragment -- what logical fragment does cvc5 actually support, per theory?

Safe mode promises no feature "that does not have full proof and model support".
In terms of *terms*, that promise is a statement about which `Kind`s may appear
in an assertion. This documents that fragment per theory, and checks that the
mechanisms meant to enforce it actually cover it.
"""

from .fragment import Fragment, scan

__all__ = ["Fragment", "scan"]
