"""Is a safe *build* still just an unrestricted build with an option default?

cvc5 ships `--safe-mode=safe` as a runtime option and `ENABLE_SAFE_MODE` as a
build option. While they agree, a configure script may exclude safe mode from a
build combination as a simplification and cost almost nothing, because the flag
substitutes for the build. If they ever diverge, that same exclusion becomes a
real restriction, and every claim about "safe mode" has to say which one it
means.

This checks the invariant that keeps them one thing.
"""
from .buildmode import Conditional, Report, scan  # noqa: F401
