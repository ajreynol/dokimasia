# Findings

Four kinds, extending anoieu's three:

| | kind | what it asks of cvc5 |
| --- | --- | --- |
| **A** | a defect | an incomplete proof, named down to the input that produces it |
| **B** | an adoption | run a check of ours in your CI, with the configuration it needs |
| **C** | a change to the pipeline | to the proof infrastructure or to what safe mode promises |
| **D** | **an assertion** | a patch adding an invariant to cvc5, so the check lives in your tree and not ours |

**Kind A is what this repository is for.** An incomplete proof, named down to
the input that produces it, is the only finding that directly serves
[the goal](goals.md). The other three are instruments: B and D are ways of
making a fix stick, C is a way of changing what the pipeline promises. They are
cheap and worth doing, and none of them is the reason this exists.

A note on D, since it is the most easily overrated: an assertion converts a
silent hole into a loud failure and no more. It does not close a hole. It is
worth proposing when an invariant we check is one cvc5 could check about itself
at startup — then the deliverable is the patch and our check gets deleted. See
[`docs/tooling.md`](tooling.md#d3--where-an-invariant-should-live).

The promises:

- **It was confirmed before it was filed, and for kind A that means an input.**
  Not a code location and an argument — a `.smt2` file, an option set, and the
  quoted `--check-proofs-complete` failure. A claim that a path is reachable is
  worth nothing until something reaches it, and the static analysis's job is to
  tell us *where to look*, not to substitute for looking.
- **A suggested assertion that fires falsely is our bug.** Exactly as a false
  positive is. So no assertion is proposed until it has been applied to a cvc5
  build configured `--assertions` and the regression suite has passed with it in
  place. An assertion we have not run is a hypothesis, and hypotheses go in
  `docs/findings.md`, not in a patch.
- **A false positive is our bug, not yours.** Every check that fires wrongly on
  cvc5 gets narrowed until it stops, and each narrowing is recorded as what it
  is — a fact about cvc5 we had got wrong. Our own CI runs the checks over a
  pinned cvc5 so that a change inventing a false positive fails *this* build
  before it reaches theirs.
- **Severity is reachability.** "This rule has no checker" is a different claim
  from "this rule has no checker and a default-options run in `QF_LIA` emits
  it." We will say which one we mean, every time.
- **Declining is an outcome.** A finding can end in "won't fix" with a reason,
  and the check gets a suppression or a `disable` in the policy file. Both beat
  the same argument every month.



## The log

Ranks: **1** an incomplete proof in `--safe-mode=safe` (a contract violation,
needs an input); **2** a hole reachable in safe mode, no input yet; **3** a gap
in stable or unrestricted.

| # | what | kind | rank | state |
| --- | --- | --- | --- | --- |
| [tcb-001](findings/tcb-001.md) | six proof rule checkers compile against the theory solvers they check, to reach `static` helpers parked on solver classes | C | — | open, refactoring proposed |

Everything else this repository currently believes is in
[`TODO.md`](../TODO.md#candidate-findings-from-the-design-pass) as an
unconfirmed candidate, and stays there until it is reproduced.

## Retractions

Kept visible, because the log of what we got wrong is the more useful half.

| # | what we claimed | what was true |
| --- | --- | --- |
| tcb-001 (draft) | the checker's TCB is **74% of `src/`** | an artifact of a mode that followed each header to its `.cpp`; the closure saturates at cvc5's whole link unit, and an unrelated seed (`printer/printer.cpp`) gave the identical figure. The compile-time surface is **8.0%**. The mode is no longer the default and warns; `tests/test_tcb.py` guards the result |
