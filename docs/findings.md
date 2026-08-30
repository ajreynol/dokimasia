# Findings

How each claim was confirmed, and where it stands. A finding is a **hypothesis
until it is reproduced** — see the promises in
[the README](../README.md#what-a-finding-is-and-what-we-promise-about-it).

Ranks come from [`tooling.md`](tooling.md#d5--safe-mode-first-and-the-reproducer-is-the-deliverable):
**1** an incomplete proof in `--safe-mode=safe` (a contract violation, needs an
input); **2** a hole reachable in safe mode, no input yet; **3** a gap in stable
or unrestricted.

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
