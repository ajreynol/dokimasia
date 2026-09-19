"""modes -- track what cvc5's safe and stable modes change about the defaults.

Safe mode promises "no feature that does not have full proof and model support."
It keeps that promise at runtime, by `SetDefaults` turning options off by name.
That list is hand-maintained and nothing checks it, so this subtool extracts it
from the source, renders it as a table, and ratchets it against a baseline so a
change to the list is visible in review.
"""

from .delta import ModeDelta, OptionChange, parse_set_defaults

__all__ = ["ModeDelta", "OptionChange", "parse_set_defaults"]
