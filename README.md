# dokimasia

A static analyzer for the **proof-production code of cvc5** — the C++ that is
supposed to emit a proof for everything the solver does, and the seam where that
proof becomes a [Eunoia](https://github.com/cvc5/ethos) proof for `ethos` to
check.

Modelled on [`anoieu`](https://github.com/ajreynol/anoieu), which does the same
job for Eunoia signatures. Signatures are its subject; the C++ is ours.

*Status: two subtools exist and have produced one report. Everything else is
design. Numbers below were measured against cvc5 `16c4001e53`.*

## Philosophy

**Completeness, not soundness.** Not *is this proof step valid*, but *is there a
path through the solver that produces no proof at all*.

**The goal is complete proofs, always.** cvc5 already promises exactly this in
one configuration — `--safe-mode=safe` is defined as allowing no feature "that
does not have full proof and model support." Everything here is an instrument
for making that promise true and keeping it true.

**White box.** We read the code. Finding holes by generating inputs is
[murxla's job](docs/tooling.md#posture-toward-murxla) and it is good at it; the
holes that matter now are the ones **no input has reached**, which is what
reading finds and running cannot.

**Eager, where cvc5 is lazy.** `--check-proofs-complete` asks our question at
runtime, one benchmark at a time, and fires only on an input that reaches the
step. We ask it of the code, with no benchmark in hand.

**Agility over coverage.** Safe mode already has almost no proof holes on
SMT-LIB. So the corpus is a good oracle and an exhausted signal, and the
bottleneck is not compute but **feedback latency** — how fast can we find the
*next* hole, and tell whether a change introduced one.

**Only claims we can back.** Every number here comes from a tool in this
repository that runs in seconds against a checkout. A claim we cannot measure is
a design note, and lives in [`TODO.md`](TODO.md) as one.

**A false positive is our bug.** Including a retracted one:
[our first headline number was wrong](docs/findings.md#retractions), and the
retraction is published beside the finding.

## The analyses

The facets of cvc5 we audit. Each is a namespace of check codes; each check owns
a witness; each says something about the pipeline that is true or false.

✅ live · ◐ partial · ○ designed

| | prefix | facet | asks |
| --- | --- | --- | --- |
| ✅ | `TCB` | **the checker's dependency surface** | how much of cvc5 must be right for `--check-proofs` to mean anything — and is it growing? |
| ◐ | `MODE` | **the safe-mode contract** | is anything reachable in safe mode without proof support? what does enabling proofs change about the solver at all? |
| ✅ | `RULE` | **the rule ledger** | for every `ProofRule`: who produces it, checks it, elaborates it, prints it. The interesting rows are the ones with a hole |
| ✅ | `TRUST` | **the trust census** | every site that can introduce a trust step, keyed by `TrustId`: which are reachable, which are dead, which are unnamed |
| ○ | `INFER` | **inference coverage** | for each `InferenceId` a theory emits, does its reconstruction have a case, and is a `ProofGenerator` attached? |
| ○ | `RW` | **rewrite coverage** | can every rewrite the rewriter performs be reconstructed — and which reconstructions depend on a search budget? |
| ◐ | `PP` | **preprocessing coverage** | does every pass either prove its work or declare a `PREPROCESS_*` trust id? |
| ◐ | `ELAB` | **macro elaboration** | is every `MACRO_*` expanded at each granularity, terminating in non-macro rules? |
| ◐ | `SEAM` | **the Eunoia seam** | `isHandled` and `isHandledSkolemId` as coverage problems, including their argument-dependent arms |
| ◐ | `INFERID` | **inference-id hygiene** | is each `InferenceId` produced at one place, so the control-flow graph is unambiguous? |
| ✅ | `CI` | **is cvc5's proof CI intact?** | do the jobs that guard proof completeness still run, with the flags they need — independently of anyone remembering to keep them? |
| ○ | `API` | **proof API contracts** | does a `ProofGenerator` return a proof of what was asked? which invariants vanish in a release build? |
| ○ | `KRN` | **kernel obligations** | see [the stretch goals](docs/kernel.md) |

Two of these — the ledger's arity column, and severity derived from reachability
rather than presence — are things [cvc5 asked anoieu
for](https://github.com/ajreynol/anoieu/blob/main/docs/README.md). They are C++
questions, so they live here.

## What exists today

No dependencies; Python 3.10+; reads a checkout, needs no build.

**[`dokimasia.tcb`](dokimasia/tcb/)** — the trusted computing base of the
internal proof checker, the natural kernel candidate.

```bash
python3 -m dokimasia.tcb measure  <cvc5>   # 179 files, 41,446 lines, 8.0% of src/
python3 -m dokimasia.tcb cuts     <cvc5>   # what each dependency edge costs
python3 -m dokimasia.tcb why      <cvc5> theory/strings/core_solver.h
python3 -m dokimasia.tcb baseline <cvc5> --check    # ratchet, for CI
```

**[`dokimasia.modes`](dokimasia/modes/)** — what safe and stable mode change
about the defaults, from all 172 option-setting sites in `set_defaults.cpp`.

```bash
python3 -m dokimasia.modes delta    <cvc5>          # safe mode: 24 option changes
python3 -m dokimasia.modes check    <cvc5>          # options that escape the promise
python3 -m dokimasia.modes baseline <cvc5> --check  # ratchet, for CI
```

**[`dokimasia.inferid`](dokimasia/inferid/)** — whether each `InferenceId` names
a single program point.

```bash
python3 -m dokimasia.inferid check <cvc5>          # 51 ids used in more than one place
python3 -m dokimasia.inferid show  <cvc5> STRINGS_CODE_PROXY
python3 -m dokimasia.inferid dead  <cvc5>          # 14 declared, produced nowhere
python3 -m dokimasia.inferid stats <cvc5>
```

**[`dokimasia.ledger`](dokimasia/ledger/)** — one row per `ProofRule`, four
columns: produced, checked, elaborated, printed.

```bash
python3 -m dokimasia.ledger holes <cvc5>          # 14 rules the Eunoia seam cannot print
python3 -m dokimasia.ledger rule  <cvc5> ARITH_POW2_INIT
python3 -m dokimasia.ledger table <cvc5> --produced-only
```

**[`dokimasia.trust`](dokimasia/trust/)** — the census of cvc5's declared holes:
every `TrustId`, where it is constructed, and the preprocessing correspondence.

```bash
python3 -m dokimasia.trust census <cvc5>          # 75 ids: 70 live, 4 dead
python3 -m dokimasia.trust passes <cvc5>          # which passes declare a hole
python3 -m dokimasia.trust show   <cvc5> THEORY_LEMMA
```

**[`dokimasia.ci`](dokimasia/ci/)** — an independent check that cvc5's proof
testing is still attached. CI is the safety net today, and one that quietly
stops being attached looks exactly like one that works.

```bash
python3 -m dokimasia.ci proofs  <cvc5>            # the completeness chain
python3 -m dokimasia.ci matrix  <cvc5>            # job x tester
python3 -m dokimasia.ci testers <cvc5>            # what each tester passes
```

Between them they have produced one report and several candidates:

- **[`tcb-001`](docs/findings/tcb-001.md)** — six proof rule checkers compile
  against the theory solvers they check, to reach `static` helpers parked on the
  solver classes. Mechanical fix, named per site.
- **`stringLazyPreproc`** declares `no_support = ["proofs"]`, defaults to `true`,
  and is disabled by neither mechanism that enforces safe mode. Either reading is
  a defect.
- **14 proof rules the solver emits, the Eunoia seam cannot print.** All 13
  arith ones sit behind `--arith-exp`, which safe mode disables — so they are
  unrestricted-mode gaps, not contract violations. `SAT_REFUTATION` is the one
  that is not arith.
- **8 trust steps are built with `TrustId::NONE`** — a hole with no stated
  reason, so nothing downstream can attribute them.
- **3 `PREPROCESS_*` trust ids are dead**, including both `bv_to_int` ids: that
  pass's trust step is attributed to `INT_BLASTER`, from a different file.
- **Proof completeness is never named in cvc5's CI.** `--check-proofs-complete`
  appears nowhere; in a safe build `setDefaultsPre` turns it on as a side effect
  of `--check-proofs`. Four links hold and nothing asserts any of them — 4 of 22
  build jobs run a proof tester, and the one that carries the contract would stop
  testing completeness if a `--proof-granularity` flag were ever added to it.

All [candidates, not findings](TODO.md#candidate-findings-from-the-design-pass),
until someone confirms them.

## The name

**δοκιμασία** was the scrutiny every official-elect in classical Athens
underwent before taking office. It did not ask whether the man had done wrong;
it asked whether he was **fit to serve**, and it asked *before* he served.

That is the distinction. Soundness asks, after the fact, whether a proof is
valid. Completeness asks, in advance, whether a code path can produce a proof at
all. cvc5's own scrutiny happens at runtime, when a benchmark finally exercises
the path. Ours happens first.

## Documentation

| | |
| --- | --- |
| [`TODO.md`](TODO.md) | the route to the goal, ordered by feedback latency |
| [`docs/goals.md`](docs/goals.md) | the goal, the agility constraint, and how we would know it is working |
| [`docs/contract.md`](docs/contract.md) | what cvc5 promises, where, and the three ways completeness breaks |
| [`docs/pipeline.md`](docs/pipeline.md) | the stages of proof production and where each leaks |
| [`docs/kernel.md`](docs/kernel.md) | the two stretch goals: a kernel you can argue about, and a safe build that cannot be unsafe |
| [`docs/hygiene.md`](docs/hygiene.md) | proof hygiene for cvc5 — ten rules, each with a measurement |
| [`docs/tooling.md`](docs/tooling.md) | the C++ static-analysis landscape, our design decisions, and the posture toward murxla |
| [`docs/findings.md`](docs/findings.md) | what a finding is, what we promise about it, and the log — including retractions |

## How this repository is maintained

**Written by an AI agent, under light human supervision.** A human maintainer
directs the work, reviews it, and decides what is reported upstream. Findings
are filed by the human, not the agent.
