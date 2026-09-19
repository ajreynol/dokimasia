"""ledger -- one row per ProofRule, four columns.

For every rule in cvc5's proof calculus:

* **produced** -- does anything in the solver emit it?
* **checked**  -- is a checker registered, and does that checker actually check?
* **elaborated** -- if it is a macro, does anything expand it?
* **printed**  -- will the Eunoia printer accept it, and for which arguments?

A rule with a hole in any column is a claim about the pipeline. The ledger is
the spine the other analyses hang off.
"""

from .build import Ledger, Row, build

__all__ = ["Ledger", "Row", "build"]
