"""trust -- the census of cvc5's declared holes.

A `TrustId` names a step cvc5 admits without proving. Being named is the point:
these are the holes cvc5 knows about. What nobody has is the census -- which are
still constructed, from where, and which are dead.
"""

from .census import Census, TrustSite, census

__all__ = ["Census", "TrustSite", "census"]
