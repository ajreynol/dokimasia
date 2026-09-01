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

*Status: eleven subtools are live and have produced one filed finding and a
register of candidates; five facets are partial or designed. Every number in
this file was measured against cvc5 `16c4001e53`, and each is reproducible with
the command beside it.*

> **A quiet run is not a complete proof pipeline.** When a check here reports
> nothing, that is a fact about the check and not about cvc5. Every analysis in
> this repository is partial, and the holes that matter are the ones nothing has
> reached yet — so silence here is not coverage, and nothing downstream should
> read it as any.

Why this question and not another is [`docs/goals.md`](docs/goals.md); what we
will and will not publish about somebody else's code is
[`reporting-policy.md`](https://github.com/ajreynol/anoieu/blob/main/docs/reports/reporting-policy.md),
shared with anoieu.

## Why cvc5 should care

The question this repository has to answer before it asks for anyone's time.
The full answer, with every number reproducible against a checkout, is
**[`docs/why.md`](docs/why.md)**. The short form is three claims and one
admission.

**1 — We supply the denominator cvc5's own counters cannot.**
`proof_final_callback.cpp` already counts trust steps and unhandled rules at
runtime, which is a numerator: the holes some input reached. *How many exist to
be reached* is a property of the code, and no execution can report the paths it
did not take. We count them: 70 live `TrustId`s, 79 inferences that fall through
to a trust step by construction, 14 rules the Eunoia seam refuses, 40 rewrites
applied and unprintable. Put those beside one corpus run with `--stats-internal`
and you get the number nobody has — **what fraction of cvc5's declared holes has
any input ever reached** — which decides how much the rest of this matters, in
either direction.

**2 — Three properties the proof pipeline depends on hold today and are
asserted nowhere.** `--check-proofs-complete` appears nowhere in cvc5's CI:
completeness is tested through a five-link implication, four links hold, and the
fifth is that nobody has added a `--proof-granularity` flag to the proof tester.
Safe mode's disable list is hand-maintained, and `stringLazyPreproc` declares
`no_support = ["proofs"]`, defaults `true`, and escapes both mechanisms. The
proof checker's trusted surface is 41,446 lines and nothing measures it. The
failure mode of all three is **silence**; each has a ratchet here that runs in
seconds with no build.

**3 — Our candidates arrive with the option gate already applied.** Severity is
computed rather than guessed, which has already killed five of our own
hypotheses ([`s-1`–`s-5`](docs/issues.md#settled)) and is what makes
[`i-1`](docs/issues.md) stand out.

**And the admission: we have produced no kind A finding.** An incomplete proof
named down to the input that produces it is what this repository is *for*, and
we have none. One finding is filed and it is a refactoring ask. That is the bar,
and we have not cleared it.

## The checks

Sixteen facets, each a namespace of check codes, each owning a witness — eleven
live, five partial or designed. The catalogue, what each has returned against
cvc5 `16c4001e53`, and what the unfinished ones are waiting on:

> **→ [`docs/checks.md`](docs/checks.md)**

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
python3 -m dokimasia.inferid check <cvc5>          # 51 ids produced at more than one site
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
python3 -m dokimasia.fragment theories <cvc5>     # 341 kinds over 14 theories
python3 -m dokimasia.fragment check    <cvc5>     # is the fragment enforced?
python3 -m dokimasia.fragment doc      <cvc5> --out docs/fragment.md
```

**[`dokimasia.infer`](dokimasia/infer/)** — does every inference a theory makes
have a proof reconstruction? The completeness core.

```bash
python3 -m dokimasia.infer coverage  <cvc5>          # per theory
python3 -m dokimasia.infer unhandled <cvc5> strings  # the ids that fall through
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
python3 -m dokimasia.gates kinds    <cvc5>        # 59 kinds carry an option gate
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
- **79 inferences fall through to a trust step by construction.** Their theory
  has an `InferProofCons`, its default case builds a `TRUST` step, and the
  switch does not name them — strings covers 78% of what it emits, datatypes
  42%, sets 22%.
- **Proof completeness is never named in cvc5's CI.** `--check-proofs-complete`
  appears nowhere; in a safe build `setDefaultsPre` turns it on as a side effect
  of `--check-proofs`. Four links hold and nothing asserts any of them — 4 of 22
  build jobs run a proof tester, and the one that carries the contract would stop
  testing completeness if a `--proof-granularity` flag were ever added to it.

All [candidates, not findings](docs/issues.md),
until someone confirms them.

## Auditing ourselves

We ask cvc5 how much of itself its proof checker depends on; it is only fair to
answer the same question here. `scripts/audit_loc` partitions this repository by
analysis, by role and by language.

```bash
scripts/audit_loc                # by analysis
scripts/audit_loc --by role      # engine / cli / tests / docs
scripts/audit_loc --by language
scripts/audit_loc --files --json
```

Lines are split into **code**, **comment**, **prose** and **data**, because a
bare total would hide the thing worth watching: the engines run at 29% comment
and the CLIs at 4%, which is roughly right — the reasoning belongs where the
analysis is, and a formatter should not need explaining. It also shows the
implementation is about half presentation, and that tests sit at 0.22× the
implementation, which is lower than it should be.

## Carrying a row to cvc5, and reading the answer

Two scripts, mirroring anoieu's `check_anoieu` and `process_anoieu`, because
cvc5 is the only project we report on and the protocol is the ecosystem's
rather than ours. The first runs in a cvc5 checkout and drafts a reply there;
the second runs here and reads it.

```bash
scripts/check_dokimasia i-4              # in cvc5: answer one row
scripts/check_dokimasia                  # in cvc5: sweep every open row
scripts/process_dokimasia i-4            # here: read what came back
scripts/process_dokimasia --status       # what became of the branch; no agent
scripts/process_dokimasia --dry-run      # what it would do; no agent
```

Both prompts are defined in [`docs/workflows.md`](docs/workflows.md) and the
scripts hold a copy, so `tests/test_workflow.py` fails when the two disagree —
a drifted copy is invisible from the side that matters, which is somebody in
cvc5 reading a prompt they were sent. Nothing is pushed and no tracker is
touched: `TRIAGE:` is an assistant's reading, `HUMAN RESPONSE:` is a
maintainer's decision, and a person carries anything that crosses between the
two repositories. What a round teaches us about the workflow goes in
[`docs/postmortem.md`](docs/postmortem.md); what it settles about cvc5 goes in
the register.

## Working an issue with an assistant

A different workflow, and a plainer one: it is not about our rows at all. It
starts an assistant inside a cvc5 checkout, points it at an issue from cvc5's
own tracker, and asks it to triage and fix.

```bash
scripts/check_cvc5_issue --issue 12884       # one issue
scripts/check_cvc5_issue --all --sample 5    # a sample the assistant picks
scripts/check_cvc5_issue --codex --issue 12884
scripts/check_cvc5_issue --issue 12884 --show-prompt   # print it, run nothing
```

Run it in the root of a cvc5 checkout; it refuses to run anywhere else. It is
interactive on purpose — the assistant is told to finish by asking what to do
next, because the useful part is usually the second turn. Where there is
something worth a maintainer's time it appends a `TRIAGE:` / `HUMAN RESPONSE:`
block to `cvc5-issue-triage.md`, and `HUMAN RESPONSE` stays empty: it is the
maintainer's, and the two labels keep what an assistant concluded apart from
what a person decided.

**The script makes no network calls.** It builds a prompt and hands it to an
assistant; whatever the assistant then reads is the assistant's business, in a
session a person is driving. Nothing here shells out to a tracker, so a run with
`--show-prompt` gives the same answer anywhere, and the script's behaviour does
not depend on what the tracker says today. With `--all` the assistant picks the
sample and is asked to say why — the choice is part of the triage.

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
| **[`docs/why.md`](docs/why.md)** | **why cvc5 should care** — the denominator argument, the three unasserted properties, what we have not delivered, and what would show we are wrong |
| **[`docs/checks.md`](docs/checks.md)** | **the checks** — sixteen facets, what each has returned, and what the unfinished ones wait on |
| **[`docs/next-report.md`](docs/next-report.md)** | **what to report next, and why** — the recommendation, the runner-up, and what is not ready to carry |
| **[`docs/reachability.md`](docs/reachability.md)** | **what the corpus actually reaches** — safe mode: 0 holes over 1,061 proofs; unrestricted: one benchmark in ten |
| **[`docs/pr-policy.md`](docs/pr-policy.md)** | **we never open a pull request** — what the tools may and may not do, and why the rate limit is a person |
| [`TODO.md`](TODO.md) | what the analysis is for: five metric groups, what each aims at, and the next four things |
| [`docs/goals.md`](docs/goals.md) | the stance, the goal, the agility constraint, and how we would know it is working |
| [`docs/contract.md`](docs/contract.md) | what cvc5 promises, where, and the three ways completeness breaks |
| [`docs/pipeline.md`](docs/pipeline.md) | the stages of proof production and where each leaks |
| [`docs/kernel.md`](docs/kernel.md) | the two stretch goals: a kernel you can argue about, and a safe build that cannot be unsafe |
| [`docs/hygiene.md`](docs/hygiene.md) | proof hygiene for cvc5 — ten rules, each with a measurement |
| [`docs/coupling.md`](docs/coupling.md) | what we ask of cvc5, and what we parse that could break |
| [`docs/tooling.md`](docs/tooling.md) | the C++ static-analysis landscape, our design decisions, and the posture toward murxla |
| [`docs/findings.md`](docs/findings.md) | what a finding is, what we promise about it, and the log — including retractions |
| [`docs/workflows.md`](docs/workflows.md) | how a candidate is carried to cvc5 and back: the conventions we share with anoieu, the two prompts, and the two scripts that run them |
| [`docs/postmortem.md`](docs/postmortem.md) | what a round of that taught us about the workflow itself — one entry per reply worked |
| [`reporting-policy.md`](https://github.com/ajreynol/anoieu/blob/main/docs/reports/reporting-policy.md) | *anoieu's, shared* — the position both tools take on reporting on code they do not own |
| [`reporting-workflow.md`](https://github.com/ajreynol/anoieu/blob/main/docs/reports/reporting-workflow.md) | *anoieu's, shared* — the conventions our workflow implements, and the shape of a reply |

## How this repository is maintained

This repository is part of the **Eunoia ecosystem** and follows its shared
repository policy, kept by [anoieu](https://github.com/ajreynol/anoieu) in
[`docs/policy.md`](https://github.com/ajreynol/anoieu/blob/main/docs/policy.md).
CI checks that claim against a pinned commit of anoieu, recorded in
[`tools/deps.lock`](tools/deps.lock) and moved by
[`scripts/bump_anoieu`](scripts/bump_anoieu), which will not move it onto a
version this repository does not pass at — so the policy we are held to changes
when somebody here decides it does.

**Written by an AI agent, under light human supervision.** A human maintainer
directs the work, reviews it, and decides what is reported upstream; findings
are filed by the human, not the agent. What *light* covers, and why the audience
is people who know cvc5 well enough to throw a finding out, is stated in
[`reporting-policy.md`](https://github.com/ajreynol/anoieu/blob/main/docs/reports/reporting-policy.md).
The workflow for carrying a candidate out and reading the answer is
[`docs/workflows.md`](docs/workflows.md).
