"""The latent holes: declared, and never reached by any input we have run.

    static inventory  -  what the corpus reached  =  the latent set

That subtraction is the one thing this repository can do that neither cvc5's
runtime oracle nor a fuzzer can. The oracle fires on an input reaching a step,
so it can only ever report the holes something reached; the difference is
invisible from that side.
"""
from .latent import Latent, State, scan  # noqa: F401
