# Why cvc5 should care

The question this repository has to answer before it asks for anyone's time.
The answer is not "we run checks." It is three claims, ranked by how well we
can back them, and one admission.

Everything below was measured against cvc5 `16c4001e53` and each row names the
command that reproduces it. Nothing here is an estimate.

---

## 1. We supply the denominator your own counters lack

**This is the strongest claim, and it is the one only static analysis can
make.**

cvc5 already measures proof incompleteness. `src/smt/proof_final_callback.cpp`
registers `finalProof::trustCount`, `finalProof::ruleUnhandledEoCount`,
`finalProof::theoryRewriteRuleUnhandledEoCount`,
`finalProof::trustTheoryLemmaCount` and `finalProof::minPedanticLevel`, all
switched on by `--stats-internal`. Run over a corpus, those are a **numerator**:
the holes something actually reached.

They cannot be a denominator. *How many holes exist to be reached* is a property
of the code, not of a run, and no execution can report the paths it did not
take. That number is what we compute:

| the population | today | from |
| --- | --- | --- |
| declared `TrustId`s, constructed somewhere | **70 of 75** | `trust census` |
| inferences whose theory has an `InferProofCons` that does not name them, so its default case builds a `TRUST` step | **79** | `infer coverage` |
| `ProofRule`s the solver emits that `EoPrinter::isHandled` refuses | **14** | `ledger holes` |
| rewrites applied and unprintable | **40** | `rewrites gaps` |

Put the two together and you get the number nobody had. **We have now measured
it for one corpus**, and it is in [`reachability.md`](reachability.md):

| over all 2,608 `regress0` benchmarks | proofs produced | reached **any** hole |
| --- | --- | --- |
| `--safe-mode=safe` | 1,061 | **0** |
| unrestricted | 1,236 | **129** (10.4%) |

Of the denominator, unrestricted mode touched **10 of 70 live `TrustId`s** and
**2 of 40** statically-unprintable rewrites. The other 86% and 95% are holes this
corpus has never exercised — which is the population this repository is for,
now measured instead of assumed.

The same run validated the static tier against the runtime oracle. cvc5's
completeness check is literally `!EoPrinter::isHandled(...)`, the predicate
`dokimasia.ledger` computes without building: **nine of the fourteen gaps we
predicted were hit, and nothing hit was outside our prediction.**

And it bounds us honestly: **on `regress0`, safe mode is clean.** If a safe-mode
completeness defect exists, it is not in this corpus.

What remains is scale: one corpus at one level, on a branch build. The levels
and benchmark sets we cannot run are still worth a maintainer's cheap `make`
target, and that is what [`R12`](issues.md#open--asks) now asks for.

---

## 2. Three properties your pipeline depends on are true today and asserted nowhere

Each holds at `16c4001e53`. None is checked by anything in cvc5's tree, and the
failure mode of all three is **silence** — nothing goes red when they stop
holding.

### The completeness chain is an implication, not a flag

`--check-proofs-complete` **appears nowhere in cvc5's CI**. Completeness is
tested as a side effect: in a safe build `setDefaultsPre` turns it on when
`--check-proofs` is set and no granularity was requested. Five links, and
`dokimasia.ci proofs` prints the state of each:

```
1. [ok ] a build job runs in safe mode              ubuntu:safe-mode
2. [ok ] that job runs --tester proof               ubuntu:safe-mode
3. [ok ] the tester passes --check-proofs           --check-proofs --proof-check=lazy
4. [ok ] the tester requests no --proof-granularity none requested
5. [NO ] completeness is named explicitly           --check-proofs-complete appears nowhere
```

Four of 22 build-matrix jobs run a proof tester at all. Adding a
`--proof-granularity` flag to the proof tester — an ordinary thing to want —
breaks link 4, and completeness testing stops. **No test fails.** Naming the
flag costs one line and converts the implication into an assertion
([`i-3`](issues.md), [`R2`](issues.md#open--asks)).

### Safe mode's disable list is hand-maintained and unchecked

`--safe-mode=safe` promises no feature "that does not have full proof and model
support" (`src/options/base_options.toml:364`). What implements the promise is a
list in `setDefaultsPre` plus a `SolverEngine` guard, and the guard fires when a
user *sets* an option — never on its default value.

`stringLazyPreproc` declares `no_support = ["proofs"]`, defaults to `true`, and
is disabled by neither mechanism. Either safe mode should turn it off or the
annotation is stale; **one sentence from a maintainer settles it**, which makes
it the cheapest row we have ([`i-2`](issues.md)). The general point is the one
that outlives the row: nothing checks that the list still covers every option
cvc5 itself annotates as unproven, so the check exists to catch the *next*
feature added, not this one.

### The checker's trusted surface is not measured

`--check-proofs` means something exactly to the extent that the code it depends
on is right. That surface is **179 files, 41,446 lines, 8.0% of `src/`**
(`tcb measure`). Nothing in cvc5 measures it, so nothing would notice it
growing — and it is the number any future kernel argument has to start from.

We got this one wrong first: we published 74%, and retracted it when the closure
turned out to saturate at cvc5's whole link unit. The retraction is in
[`findings.md`](findings.md#retractions) and a test guards the corrected figure.
We would rather show that than not.

### The mechanism, and the first thing it caught

Every property above has a `baseline --check` ratchet here: no build, no
dependencies, Python 3.10+, eight of them, seconds against a checkout.

Writing this page, we ran all eight against `16c4001e53` — **the commit they
were recorded at.** Six were clean and two failed. Not because cvc5 had changed:
because our baselines named `SETS_RELS_TCLOSURE_DOWN`, an `InferenceId` cvc5 has
never had. `git log --all -S` finds it in no commit in cvc5's history, and the
enum at that commit carries `SETS_RELS_TCLOSURE_FWD` and `SETS_RELS_TCLOSURE_UP`.
The baselines had been written rather than generated.

One of the two failures was then **misreported by our own tool.**
`dokimasia.infer` took the ids that had left the unhandled set and called them
*now reconstructed* — but an id leaves that set for two unrelated reasons: the
theory has started proving it, or it is no longer emitted at all. The tool could
not tell those apart, so it stood ready to report a rename in cvc5 as an
improvement in cvc5's proof coverage. That is precisely the class of unbacked
claim about somebody else's code this repository exists in order not to make.

Both are fixed. The baselines are regenerated by running the tools; all eight
are clean at `16c4001e53`; and the delta now separates *reconstructed* from *no
longer emitted*, marking the second `?` rather than `-` because it is a question
about our own scan, not a fact about cvc5.

**This is reported because it is the honest state of the evidence, and because
it is the argument.** A ratchet earns its place by failing when something it
asserts stops being true, and the failure has to be legible enough to act on.
The first thing ours caught was us — which is a smaller claim than we might have
liked to make here, and a better-evidenced one.

---

## 3. A candidate list with the option gate already applied

The weakest of the three claims, and still worth something: when we say a hole
is reachable, we have asked whether safe mode blocks it, rather than reporting
presence and leaving severity to the reader.

That distinction has already killed several of our own rows —
[`s-1`](issues.md#settled) through [`s-5`](issues.md#settled) are hypotheses the
gate analysis destroyed, including two "hard rewrite gaps" that turned out to
need `--arrays-exp` and `--datatypes-exp`. It is also what makes
[`i-1`](issues.md) (`LAMBDA_ELIM`) stand out: its seam arm fires on
`Kind::LAMBDA`, and the fragment analysis finds **no `uf` kind blocked in safe
mode at all**.

The full register, ranked, with what would settle each, is
[`issues.md`](issues.md). Rank 1 is a contract violation, rank 2 a hole
reachable in safe mode with no input yet, rank 3 a gap outside safe mode or a
cleanup.

---

## What we have not delivered

[Kind A](findings.md) — an incomplete proof, named down to the input that
produces it — is what this repository is for, and **we have produced none.**

One finding is filed ([`tcb-001`](findings/tcb-001.md)), and it is a kind C: a
refactoring ask, not a hole. The strongest safe-mode candidate we have,
[`i-1`](issues.md), is a static argument that needs a `.smt2` file we have not
written, and `canEliminateLambda` may only succeed in the HOL cases `ufHoExp`
already gates — static work cannot tell. Most of the rest of the register is
rank 3.

So the accurate summary of this repository today is: **instrumentation that
works, a small number of live hypotheses, and no confirmed hole.** A cvc5
maintainer is entitled to weigh it on that basis, and the bar we hold ourselves
to is the one we have not yet cleared.

## What would show we are wrong

- **The corpus difference in §1 comes back small.** Then the static surface has
  little headroom, the runtime oracle is sufficient, and this is a ratchet
  repository rather than a hole-finding one.
- **Our parsing is load-bearing and brittle.** We read C++ and TOML with
  regexes. What we depend on, and what an upstream change would break, is
  [`coupling.md`](coupling.md) — and three parser bugs in one session are the
  whole argument for [`R1`](issues.md#open--asks), emitting the registries as
  JSON.
- **Silence here is not coverage.** When a check reports nothing, that is a fact
  about the check. Every analysis in this repository is partial, and we do not
  let a quiet run stand in for a guarantee.

## What it costs cvc5 to find out

Reading a row. Every number on this page is reproducible in seconds from a
checkout with no build and no dependencies, which means no claim here requires
trusting us — only running the command beside it. A false positive is ours, and
so is anything we asked you to run that turned out to waste your time
([reporting policy](https://github.com/ajreynol/anoieu/blob/main/docs/reports/reporting-policy.md)).
