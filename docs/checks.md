# The checks

The facets of cvc5 we audit. Each is a namespace of check codes; each check owns
a witness; each says something about the pipeline that is true or false.

This is the catalogue. What it is *for* — why a cvc5 maintainer should spend
time on any of it — is [`why.md`](why.md); the commands that exist today are on
the [front page](../README.md#what-exists-today); the individual claims are in
[`issues.md`](issues.md).

✅ live · ◐ partial · ○ designed

| | prefix | facet | asks |
| --- | --- | --- | --- |
| ✅ | `TCB` | **the checker's dependency surface** | how much of cvc5 must be right for `--check-proofs` to mean anything — and is it growing? |
| ◐ | `MODE` | **the safe-mode contract** | is anything reachable in safe mode without proof support? what does enabling proofs change about the solver at all? |
| ✅ | `RULE` | **the rule ledger** | for every `ProofRule`: who produces it, checks it, elaborates it, prints it. The interesting rows are the ones with a hole |
| ✅ | `TRUST` | **the trust census** | every site that can introduce a trust step, keyed by `TrustId`: which are reachable, which are dead, which are unnamed |
| ✅ | `INFER` | **inference coverage** | for each `InferenceId` a theory emits, does its reconstruction have a case, and is a `ProofGenerator` attached? |
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
| ○ | `KRN` | **kernel obligations** | see [the stretch goals](kernel.md) |

Two of these — the ledger's arity column, and severity derived from reachability
rather than presence — are things [cvc5 asked anoieu
for](https://github.com/ajreynol/anoieu/blob/main/docs/README.md). They are C++
questions, so they live here.

## What each facet has produced

Only the live ones, and only what a check actually returned against a checkout.
The register row for each is in [`issues.md`](issues.md).

| prefix | tool | measured at `16c4001e53` | rows |
| --- | --- | --- | --- |
| `TCB` | `dokimasia.tcb` | 179 files, 41,446 lines, 8.0% of `src/`; 6 rule checkers compile against the solvers they check | [`f-1`](findings/tcb-001.md) |
| `MODE` | `dokimasia.modes` | 24 option changes in safe mode; 2 options declare no proof support and stay on, of which 1 survives review | `i-2`, `i-5` |
| `RULE` | `dokimasia.ledger` | 170 rules: 113 always printable, 17 conditionally, 40 never — 14 by design, 12 unreachable, **14 real gaps** | `i-7`, `i-12` |
| `TRUST` | `dokimasia.trust` | 75 declared ids: 70 live, 4 dead, 8 sites built with `TrustId::NONE` | `i-9`, `i-10`, `i-11` |
| `INFER` | `dokimasia.infer` | 79 inferences fall through to a trust step by construction; 10 theories have no `InferProofCons` at all | `i-22`, `i-6` |
| `RW` | `dokimasia.rewrites` | 533-rule vocabulary; 40 applied and unprintable; 3 taken only outside safe mode | `i-17`, `i-18` |
| `INFERID` | `dokimasia.inferid` | 51 ids produced at more than one site, 14 produced nowhere, 21 emitted with a sentinel | `i-8` |
| `CI` | `dokimasia.ci` | 4 of 22 jobs run a proof tester; 4 of 5 completeness links hold, the fifth is never named | `i-3`, `i-13`, `i-14` |
| `GATE` | `dokimasia.gates` | 59 term kinds carry an option gate; verdicts blocked / partial / open per rule | `i-1`, `s-1`–`s-5` |
| `FRAG` | `dokimasia.fragment` | 341 kinds over 14 theories (223 available, 118 blocked); two safe-mode options gate no kind at all | `i-15` |
| `SIG` | `dokimasia.signature` | 0 printable rules undeclared; 24 skolems constructed and unprintable; 1 documented arity disagreement | `i-19`, `i-20`, `i-21` |

The `MODE` row is the shape to notice: the check returned two options and one of
them ([`s-4`](issues.md#settled), `macrosQuantMode`) was spurious — its effect is
gated by a flag defaulting to `false`, which a defaults-only comparison cannot
see. The tool now prints that limit beside the result.

## What a partial or designed facet is waiting on

| prefix | blocked on |
| --- | --- |
| `PP` | the pass↔trust-id correspondence is not derivable by name (`i-11`, [`R7`](issues.md#open--asks)) |
| `ELAB` | granularity is a runtime property; deciding it statically needs the elaboration graph, not the rule list |
| `SEAM` | `SEAM0002` — characterising the unhandled *argument* set of the conditional arms, not just the rule |
| `INFERID` | nothing; it is live but its precision is bounded by `i-8`, which is cvc5's to fix ([`R4`](issues.md#open--asks)) |
| `API` | needs the call site, which is the AST tier — see [`tooling.md`](tooling.md) |
| `KRN` | [`i-4`](issues.md): reconstruction runs under a search budget with no termination argument, which bounds what any kernel contract can claim |

## The check-code convention

A check code is `PREFIX` plus four digits — `RULE0001`, `TRUST0003`,
`CI0002` — allocated once and never reused, the same convention anoieu uses for
signatures. A code names a *question asked of the code*, not an occurrence: one
code can return many rows or none, and returning none is a fact about the check
rather than about cvc5. The per-code list, with what is implemented and what is
not, is in [`TODO.md`](../TODO.md) under the group that owns it.
