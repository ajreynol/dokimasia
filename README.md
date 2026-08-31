# dokimasia

A static analyzer for the **proof-production code of cvc5** — the C++ that is
supposed to emit a proof for everything the solver does, and the seam where that
proof becomes a [Eunoia](https://github.com/cvc5/ethos) proof for `ethos` to
check.

It asks one question: **is there a path through the solver that produces no
proof at all?** Not whether a proof step is valid — completeness, not soundness.
It reads a checkout in seconds and builds nothing, so what it finds are the
holes no input has reached.

Modelled on [`anoieu`](https://github.com/ajreynol/anoieu), which does the same
job for Eunoia signatures. Signatures are its subject; the C++ is ours.

*Status: two subtools exist and have produced one report. Everything else is
design. Numbers below were measured against cvc5 `16c4001e53`.*

> **A quiet run is not a complete proof pipeline.** When a check here reports
> nothing, that is a fact about the check and not about cvc5. Every analysis in
> this repository is partial, and the holes that matter are the ones nothing has
> reached yet — so silence here is not coverage, and nothing downstream should
> read it as any.

Why this question and not another is [`docs/goals.md`](docs/goals.md); what we
will and will not publish about somebody else's code is
[`philosophy.md`](https://github.com/ajreynol/anoieu/blob/main/docs/philosophy.md),
shared with anoieu.

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
| ✅ | `RW` | **rewrite coverage** | can every rewrite the rewriter performs be reconstructed — and which reconstructions depend on a search budget? |
| ◐ | `PP` | **preprocessing coverage** | does every pass either prove its work or declare a `PREPROCESS_*` trust id? |
| ◐ | `ELAB` | **macro elaboration** | is every `MACRO_*` expanded at each granularity, terminating in non-macro rules? |
| ◐ | `SEAM` | **the Eunoia seam** | `isHandled` and `isHandledSkolemId` as coverage problems, including their argument-dependent arms |
| ◐ | `INFERID` | **inference-id hygiene** | is each `InferenceId` produced at one place, so the control-flow graph is unambiguous? |
| ✅ | `CI` | **is cvc5's proof CI intact?** | do the jobs that guard proof completeness still run, with the flags they need — independently of anyone remembering to keep them? |
| ○ | `API` | **proof API contracts** | does a `ProofGenerator` return a proof of what was asked? which invariants vanish in a release build? |
| ✅ | `GATE` | **option gates** | which option must be on for a term kind — and so a rule — to occur, so severity can be computed instead of guessed |
| ✅ | `FRAG` | **the supported fragment** | which term kinds may appear per theory under safe mode — and do the three enforcement mechanisms actually cover it? |
| ✅ | `SIG` | **signature agreement** | do the rules and skolems cvc5 can print exist in the Eunoia signature, and does its own documentation match? |
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

**[`dokimasia.rewrites`](dokimasia/rewrites/)** — coverage of the 533-rule
rewrite vocabulary at the Eunoia seam.

```bash
python3 -m dokimasia.rewrites coverage <cvc5>     # RARE vs hand-written vs applied
python3 -m dokimasia.rewrites gaps     <cvc5>     # applied, and unprintable
```

**[`dokimasia.fragment`](dokimasia/fragment/)** — the logical fragment cvc5
supports, per theory, and whether it is enforced. Generates
[`docs/fragment.md`](docs/fragment.md).

```bash
python3 -m dokimasia.fragment theories <cvc5>     # 352 kinds over 14 theories
python3 -m dokimasia.fragment check    <cvc5>     # is the fragment enforced?
python3 -m dokimasia.fragment doc      <cvc5> --out docs/fragment.md
```

**[`dokimasia.signature`](dokimasia/signature/)** — does the Eunoia signature
agree with cvc5's own account of a rule?

```bash
python3 -m dokimasia.signature rules   <cvc5>     # 0 printable rules undeclared
python3 -m dokimasia.signature skolems <cvc5>     # 24 constructed but unprintable
python3 -m dokimasia.signature checker <cvc5>     # documented arity vs what the checker enforces
```

**[`dokimasia.gates`](dokimasia/gates/)** — the machinery the other tools kept
needing: which option legalises each term kind, and so whether a rule can fire
under `--safe-mode=safe`.

```bash
python3 -m dokimasia.gates kinds    <cvc5>        # 52 gated term kinds
python3 -m dokimasia.gates rule     <cvc5> LAMBDA_ELIM
python3 -m dokimasia.gates verdicts <cvc5>        # blocked / partial / open
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
- **Safe mode is *stricter* at the Eunoia seam than the default.** Three
  rewrites are accepted by `isHandledTheoryRewrite` only when
  `safeMode == UNRESTRICTED`, and all three are implemented by a rewriter. The
  gate analysis blocks two of them in safe mode — but **`LAMBDA_ELIM` comes back
  open**: its arm fires on `Kind::LAMBDA`, which nothing gates. That is the
  strongest safe-mode candidate this repository has produced.
- **Proof completeness is never named in cvc5's CI.** `--check-proofs-complete`
  appears nowhere; in a safe build `setDefaultsPre` turns it on as a side effect
  of `--check-proofs`. Four links hold and nothing asserts any of them — 4 of 22
  build jobs run a proof tester, and the one that carries the contract would stop
  testing completeness if a `--proof-granularity` flag were ever added to it.

All [candidates, not findings](docs/issues.md),
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
| [`TODO.md`](TODO.md) | what the analysis is for: five metric groups, what each aims at, and the next four things |
| [`docs/goals.md`](docs/goals.md) | the stance, the goal, the agility constraint, and how we would know it is working |
| [`docs/contract.md`](docs/contract.md) | what cvc5 promises, where, and the three ways completeness breaks |
| [`docs/pipeline.md`](docs/pipeline.md) | the stages of proof production and where each leaks |
| [`docs/kernel.md`](docs/kernel.md) | the two stretch goals: a kernel you can argue about, and a safe build that cannot be unsafe |
| [`docs/hygiene.md`](docs/hygiene.md) | proof hygiene for cvc5 — ten rules, each with a measurement |
| [`docs/coupling.md`](docs/coupling.md) | what we ask of cvc5, and what we parse that could break |
| [`docs/tooling.md`](docs/tooling.md) | the C++ static-analysis landscape, our design decisions, and the posture toward murxla |
| [`docs/findings.md`](docs/findings.md) | what a finding is, what we promise about it, and the log — including retractions |
| [`docs/workflows.md`](docs/workflows.md) | how a candidate is carried to cvc5 and back: the conventions we share with anoieu, and the two prompts |
| [`philosophy.md`](https://github.com/ajreynol/anoieu/blob/main/docs/philosophy.md) | *anoieu's, shared* — the position both tools take on reporting on code they do not own |
| [`reporting-policy.md`](https://github.com/ajreynol/anoieu/blob/main/docs/reporting-policy.md) | *anoieu's, shared* — the conventions our workflow implements, and the shape of a reply |

## How this repository is maintained

**Written by an AI agent, under light human supervision.** A human maintainer
directs the work, reviews it, and decides what is reported upstream; findings
are filed by the human, not the agent. What *light* covers, and why the audience
is people who know cvc5 well enough to throw a finding out, is stated in
[`philosophy.md`](https://github.com/ajreynol/anoieu/blob/main/docs/philosophy.md).
The workflow for carrying a candidate out and reading the answer is
[`docs/workflows.md`](docs/workflows.md).
