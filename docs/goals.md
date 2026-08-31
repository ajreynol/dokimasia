# The goal, and how we would know it is working

**cvc5 should have complete proofs, always.**

That is the point of this repository. Everything else in it — the checks, the
hygiene standard, the TCB measurement, the CI proposals — is an *instrument* for
that, and should be judged by how much it moves it.

## The stance

**Completeness, not soundness.** Not *is this proof step valid*, but *is there a
path through the solver that produces no proof at all*. cvc5 already promises
exactly that in one configuration — `--safe-mode=safe` is defined as allowing no
feature "that does not have full proof and model support" — and everything here
is an instrument for making the promise true and keeping it true.

**White box, and eager.** We read the code. Finding holes by generating inputs
is [murxla's job](tooling.md#posture-toward-murxla) and it is good at it; the
ones that matter now are the holes **no input has reached**, which is what
reading finds and running cannot. cvc5 asks our question at runtime —
`--check-proofs-complete`, one benchmark at a time, firing only on an input that
reaches the step. We ask it of the code, with no benchmark in hand.

**Only claims we can back.** Every number we publish comes from a tool in this
repository that runs in seconds against a checkout. A claim we cannot measure is
a design note, and lives in [`TODO.md`](../TODO.md) as one.

What we will and will not say about somebody else's code — silence is never
evidence, a false positive is ours, an artifact settles a finding — is the
position shared with anoieu in
[`reporting-policy.md`](https://github.com/ajreynol/anoieu/blob/main/docs/reports/reporting-policy.md),
and is not restated here.

## The operating constraint: agility

Safe mode already has **almost no proof holes on SMT-LIB**. That single fact
sets the strategy, because it means the obvious approach is the wrong one:

- running a benchmark corpus is a **good oracle** and a **slow, largely
  exhausted signal**. It is worth doing once for a baseline. It is not where the
  next hole comes from;
- the holes that remain are, by definition, the ones **SMT-LIB does not reach**;
- so the thing to optimize is not compute — it is **feedback latency**. How
  quickly can we find the *next* hole, and how cheaply can we tell whether a
  change introduced one?

Ranked by how fast they return an answer, not by how much they cost:

| | signal | latency | finds |
| --- | --- | --- | --- |
| **1** | **static analysis** of the pipeline | seconds, no build | holes no input has ever reached — *the ones that are left* |
| **2** | **safe-mode consistency** — does safe mode do what it says? | seconds, no build | features that escape their own guard |
| **3** | **build-time pruning** — is the unsafe code even linked? | one build | a whole class of hole, converted into a link error |
| **4** | **fuzzing** — *[murxla's job, not ours](tooling.md#posture-toward-murxla)* | minutes | inputs a fixed corpus does not contain |
| **5** | **a curated corpus of known holes** | seconds | regressions on holes already reported |
| **6** | **SMT-LIB census** | hours | the baseline, once |

The priority order, so it is not ambiguous:

| | | |
| --- | --- | --- |
| **1** | **Complete proofs, always** | the goal |
| **2** | **Find the next hole fast** | latency is the metric. Rows 1–5 above, in that order |
| **3** | **Close the holes** | each is a concrete work item for a cvc5 developer, with a reproducer |
| **4** | **Make safe mode true by construction** | not a hand-maintained list that happens to be right — see [a safe build that cannot be unsafe](kernel.md#a-safe-build-that-cannot-be-unsafe) |
| **5** | Keep closed holes closed | regression. Useful, not the point |
| **6** | Argue a growing fragment is hole-free | the [kernel](kernel.md#a-kernel-you-can-argue-about). The long game |

Assertions, SARIF uploads and nightly jobs live below all of this. They are
worth doing and they are not why this exists.

## How we will know it is working

Two numbers, and neither is "benchmarks passed":

> **latency** — how long from "a hole exists" to "we can point at it"?
>
> **the latent count** — how many holes are reachable that no input has hit?

cvc5 already instruments the second half of the measurement:
`src/smt/proof_final_callback.cpp` registers
`finalProof::ruleUnhandledEoCount`, `finalProof::theoryRewriteRuleUnhandledEoCount`,
`finalProof::trustCount`, `finalProof::trustTheoryLemmaCount` and
`finalProof::minPedanticLevel`, all switched on by `--stats-internal`. Run once,
that gives the baseline; the interesting number is the *difference* between what
static analysis says is reachable and what the corpus actually hit.

