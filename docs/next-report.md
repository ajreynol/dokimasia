# The next thing to report, and why it is that one

**Question:** of everything this repository believes, which class is most worth
a cvc5 maintainer's time — as a bug report, or as a patch a human carries?

Nothing here is sent by a program. See [`pr-policy.md`](pr-policy.md).

## The verdicts

Applying [the bar](pr-policy.md#the-bar). Two rows clear it; everything else
names the rule that blocks it.

| verdict | row | |
| --- | --- | --- |
| **carry** | `i-3` / `R2` | the completeness flag cannot be set in the mode that promises it |
| **carry** | `i-2` | `stringLazyPreproc` — safe mode refuses to let you set it *because it lacks proof support*, and leaves it on |
| not yet — **run-it** | `i-1`, `i-22`, `i-6` | a static argument with no input. `i-1` has had one attempt fail |
| not yet — **run-it** | the 182 [latent holes](reachability.md) | declared, and nothing has reached them |
| not yet — **worth-the-attention** | the dead-declaration cleanups | bundled, and only after something substantive lands |
| never | `i-4` | a termination argument for the reconstruction search settles it, and nothing else does |

## The recommendation

**Report the completeness flag first: `--check-proofs-complete` cannot be set in
either mode whose contract it enforces.** ([`i-3`](issues.md), [`R2`](issues.md#open--asks))

One command is the whole report:

```
$ cvc5 --safe-mode=safe --produce-proofs --check-proofs --check-proofs-complete f.smt2
(error "Fatal error in option parsing: expert option check-proofs-complete
        cannot be set in safe mode.")
```

`checkProofsComplete` is `category = "expert"` in `proof_options.toml`. Safe and
stable mode reject expert options. So the flag can only be passed in the
unrestricted job — the one mode that makes no completeness promise. In safe
mode the guarantee is obtainable **only** as a side effect: `setDefaultsPre`
turns the option on when `--check-proofs` is set and no `--proof-granularity`
was requested. Adding a granularity flag to the proof tester would switch
completeness testing off, and no test would fail.

**Why this one.**

| criterion | |
| --- | --- |
| **it is about the guarantee itself** | not a hole, but the mechanism that detects holes. Everything else this repository reports depends on it working |
| **it takes one command to verify** | no build, no corpus, no argument about reachability. A maintainer can refute or confirm it in thirty seconds |
| **it is not a matter of taste** | the option's own help text says *"enabled by default in safe builds"*, and safe builds are exactly where it cannot be named |
| **the fix is small and has a natural home** | an assertion in `setDefaultsPre` — a [kind D](findings.md), so the invariant lands in cvc5's tree and our `CI0002` check retires |
| **we found it by running, not reading** | the static analysis got this ask *wrong* (see below), which is itself worth telling them |

**The proposed fix**, in preference order:

1. **Assert the implication where it is created.** In `setDefaultsPre`, after a
   safe build enables `checkProofsComplete`, assert it is set. Smallest change,
   no option-semantics decision, and it makes the four-link chain a one-line
   fact in cvc5's own tree.
2. **Exempt `checkProofsComplete` from the expert refusal**, so the safe-mode
   regression tester can name what it is testing. Larger, and a maintainer's
   call about what "expert" means.

**What would sink it:** a maintainer saying the side effect is deliberate and
documented, and that naming the flag was never intended. That is a fine answer,
and it still leaves the `--proof-granularity` interaction worth an assertion.

## The second carry: `i-2`

Two commands, and they contradict each other:

```
$ cvc5 --safe-mode=safe --strings-lazy-pp f.smt2
(error "Fatal error in option parsing: cannot set option strings-lazy-pp in
        safe mode, as this option does not support proofs")
```

...while `strings_options.toml` gives it `default = "true"` and `setDefaultsPre`
never turns it off. **Safe mode refuses to let you set the option on the grounds
that it does not support proofs, and then runs with it on.**

`--no-strings-lazy-pp` is refused too, so the guard also blocks the one
assignment that would make the configuration safer — a user who has read the
annotation and wants to comply cannot.

Either reading is a defect and the fix is a maintainer's one-line call: disable
it in safe mode, or drop the stale annotation. It is cheap to receive, which is
why it goes with `i-3` rather than behind it.

## Runner-up, and why it is second

**[`i-23`](issues.md) — the `safeMode == UNRESTRICTED` guard in
`EoPrinter::isHandled` is inert.** Ten rules are accepted only in unrestricted
builds; none of the ten can be *produced* in safe or stable mode. Verified by
running: transcendental kinds are refused outright, and `set.filter` needs a
function-typed argument and so the higher-order logic both modes reject.

It is second because the fix is not obvious and the payoff is smaller. Deleting
the cases would be **wrong** — they would fall through to `default: return
false` and flip unrestricted mode from handled to unhandled. The right change is
to move them to the always-handled list or to document why the condition cannot
matter, and which of those is right is a question for whoever wrote it. It is a
good *question*, not a good patch.

## Explicitly not recommended yet

- **`i-1` (`LAMBDA_ELIM`).** Our strongest safe-mode candidate, and the one
  nearest to a `set.filter`-shaped mistake. The sweeping claim beside it — *no
  `uf` kind is blocked in safe mode* — turned out to be [half
  wrong](issues.md#settled). One reproducer attempt has already failed. **Do not
  carry this without an input.**
- **Anything resting on the 79 fall-through inferences.** Real by construction,
  but [the corpus reaches none of them in safe mode](reachability.md), so
  severity is unestablished and a maintainer would rightly ask for one input.
- **The dead-declaration cleanups** (4 dead `TrustId`s, 14 dead `InferenceId`s,
  3 dead `PREPROCESS_*` ids, the `PREPROCESS_BV_GUASS` misspelling). These are
  the *most* landable as a patch and the least valuable: near-zero risk,
  near-zero benefit, and they spend the credit that should go to the first
  report above. Worth bundling into one PR **after** something substantive has
  been accepted, never before.

## The general rule this session suggests

**Prefer the claim a maintainer can refute in one command.** Of the four things
this repository got wrong recently, three were static arguments that read
correctly and were false; every one was caught by running something. A report
whose evidence is a command carries its own refutation, which is the property
that makes it cheap to receive.
