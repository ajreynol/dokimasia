"""Loud failure when an extractor finds implausibly little.

Every tool here recovers structure by reading source text, and the failure mode
that costs the most is not a crash. It is an anchor that stops matching -- a
renamed function, a restructured switch -- after which the extractor returns
nothing and the tool reports a confident, wrong, plausible-looking answer.

That happened three times while these tools were built:

* `isHandledTheoryRewrite` was matched at its call site rather than its
  definition, and the parser returned 0 arms where 53 exist;
* a comment-stripping regex under `re.DOTALL` swallowed every switch arm whose
  body opened with `//`, silently losing their labels;
* an include-closure mode saturated at cvc5's whole link unit, giving the same
  answer for any seed.

Each was caught by a person noticing a number looked wrong. `expect` is the
cheap version of that noticing: state what a healthy extraction looks like, and
fail with a message naming the anchor when it does not hold.
"""

from __future__ import annotations


#: Thresholds describe a real cvc5 tree. Synthetic fixtures in the tests are
#: deliberately tiny, so they turn this off around the fixture and back on
#: after. A toggle rather than a size heuristic: "is this a real checkout" is
#: exactly the kind of guess that would eventually be wrong in the direction
#: that matters.
_ENABLED = True


def set_enabled(value: bool) -> None:
    global _ENABLED
    _ENABLED = value


class disabled:
    """Context manager: `with sanity.disabled():` around a synthetic fixture."""

    def __enter__(self):
        set_enabled(False)
        return self

    def __exit__(self, *exc):
        set_enabled(True)
        return False


class ExtractionError(RuntimeError):
    """An extractor found so little that its result should not be trusted."""


def expect(got: int, at_least: int, what: str, anchor: str) -> int:
    """Assert an extraction found at least *at_least* items.

    *anchor* names the thing whose change would explain the shortfall, so the
    error says where to look rather than only that something is wrong.
    """
    if _ENABLED and got < at_least:
        raise ExtractionError(
            f"found {got} {what}, expected at least {at_least}.\n"
            f"  The anchor is: {anchor}\n"
            f"  If cvc5 changed there, this tool needs updating -- that is our\n"
            f"  bug, not cvc5's. Do not trust any number this run produced."
        )
    return got


def warn_if(condition: bool, message: str) -> None:
    """Print a caveat to stderr without failing -- for soft anomalies."""
    if condition:
        import sys
        print(f"warning: {message}", file=sys.stderr)
