# Proof hygiene

A proposed standard for cvc5's proof system: naming, calling conventions,
checker registration, and the discipline around inference ids.

This is the warm-up project, and it is not busywork. It is the **precondition
for every later goal in this repository**, for a reason worth stating plainly:

> You cannot draw a boundary around a thing you cannot name.

The kernel goal ([README](kernel.md))
is about making it *easier to argue* which part of cvc5 is its proof-producing
core. Every such argument is made out of entities — inferences, rules, trust
steps — and an argument is only as sharp as the entities are. If an
`InferenceId` is emitted at eight different places, then "the inferences theory
X can make" is not an enumerable set, and no statement quantified over it means
anything precise. Hygiene is what turns cvc5's informal proof markers into
things you can quantify over.

So the chain is:

**hygiene → nameable entities → a drawable boundary → an argument someone can
check → (eventually, in places) mechanization.**

Hygiene is the first link, it is cheap, and it pays off immediately in ordinary
maintenance whether or not anyone ever builds a kernel.

## Why inference ids specifically

`InferenceId` is cvc5's existing, *informal* proof annotation. It predates most
of the proof infrastructure and it is attached to essentially every lemma and
conflict a theory emits. It is not a proof and does not claim to be — but it is
the closest thing cvc5 has to a complete index of "what inferences exist," and
it is the natural spine for the analysis this project wants to do.

That only works if an id means one thing. Below is what the code says today.

---

## The rules

Each rule states the norm, the evidence for it, how it would be checked, and
what it buys. Measured against cvc5 `40a4bb7e4`.

### H1 — One id, one place

**An `InferenceId` is produced at exactly one point in the code.**

The rationale is the whole of it: **so the control-flow graph is unambiguous.**
Seeing an id in a trace, a statistic or a proof should identify one place the
solver can have been. An id with three production sites identifies three, which
is to say it identifies none of them — and every claim quantified over "the
inferences theory X can make" gets correspondingly weaker.

*Evidence.* Measured by [`dokimasia.inferid`](../dokimasia/inferid/):

| production sites | ids |
| --- | --- |
| 1 — contract holds | **346** |
| 2 | 34 |
| 3 | 11 |
| 4–8 | 6 |
| 0 — dead marker | 14 |

**346 of 411 (84%) already satisfy it.** The worst are
`ARITH_NL_T_INIT_REFINE`, `ARRAYS_EQ_TAUTOLOGY` and `FP_PREPROCESS` at 8 sites
each. Separately, **21 inferences are emitted with a sentinel id**
(`UNKNOWN` ×15, `NONE` ×6) — see H2.

*What counts as a use.* The tool distinguishes four kinds and only one violates
the contract: **production** (the id passed as a value — the site the id names),
against **dispatch** (`case InferenceId::X:`), **comparison** (`== X`) and the
**definition**. A `case` label consumes an id produced elsewhere; it creates no
ambiguity about where the inference came from. `--strict` counts every use
outside the enum, for the stricter reading.

*What it buys.* The id becomes a **key**. "Which inferences can theory X make"
becomes a set you can enumerate, and "does this inference have a proof" becomes
a question with one answer instead of eight. This is the highest-value hygiene
rule for everything downstream, and at 84% it is a norm to ratify and 51
exceptions to work through, not a rewrite.

*A sub-case worth its own row.* 14 ids are declared and produced nowhere, and at
least one — `STRINGS_CODE_PROXY` — is *dispatched on* in
`strings/infer_proof_cons.cpp` while nothing emits it: a proof reconstruction
case for an inference the solver does not make.

### H2 — No anonymous inferences

**`InferenceId::UNKNOWN` and `InferenceId::NONE` are not acceptable in
theory-emitted lemmas.**

*Evidence.* 20 sites use `UNKNOWN`, 6 use `NONE` — 26 inferences that carry no
marker at all. These are precisely the places where the later analysis has
nothing to say, and where a trust step, if one appears, cannot be attributed.

*What it buys.* The index becomes total. An analysis over `InferenceId` that
starts with "except for the 26 anonymous ones" is an analysis with a hole in it.

### H3 — The prefix names the owner

**An `InferenceId`'s prefix is the theory that emits it.**

*Evidence.* Already near-universal: `STRINGS` 87, `QUANTIFIERS` 75, `ARITH` 69,
`SETS` 58, `DATATYPES` 27, `BAGS` 23, `UF` 22, `SEP` 13, `TABLES` 11, `BV` 7,
`ARRAYS` 6, `FP` 3, plus a handful of cross-cutting singletons (`INPUT`,
`PLUGIN`, `PARTITION`, `THEORY`).

*How it is checked.* Tier 0: prefix against the directory of the emitting file.
Cheap, exact, and a good first check to write because it should find almost
nothing — which is how you validate a checker.

### H4 — One vocabulary per theory

**A theory's `ProofRule`s and its `InferenceId`s use the same name for the same
theory.**

*Evidence.* They do not, today. `InferenceId` uses `STRINGS_*`; `ProofRule` uses
`STRING_*` (8 rules) — singular against plural — and then does not use a theory
prefix at all for `CONCAT_*` (6) and `RE_*` (5), which are also strings rules.
More broadly, `ProofRule` prefixes mix *theory* names (`ARITH` 31, `BV`, `SETS`,
`ARRAYS`) with *logical form* names (`CNF` 21, `NOT` 11, `ITE`, `XOR`, `TRUE`).

*What it buys.* Cross-referencing an inference to the rules that discharge it is
currently a manual act of translation. This is the rule with the highest
annoyance-to-difficulty ratio in the document, and the one most likely to be
declined as churn — which is a fine outcome, provided it is declined explicitly
and written down rather than rediscovered.

### H5 — Every id has one reconstruction home

**If an `InferenceId` has a proof reconstruction, it lives in one place, and
that place is findable from the id.**

*Evidence.* Only `strings`, `datatypes` and `sets` have an
`infer_proof_cons.cpp`. Other proof-producing theories attach generators at the
inference site instead. Both are defensible; having both without a rule for
which applies is not, because it means "does this inference have a proof" cannot
be answered by looking in one place.

*What it buys.* A total function from id to proof status. That function *is* the
completeness analysis; everything else is machinery for computing it.

### H6 — "No proof" must be said out loud

**The proofless path stops being the default.**

*Evidence.* This is the sharpest finding in the document.
`TheoryInferenceManager` declares `ProofGenerator* pg = nullptr` as a **default
argument**, and `conflict(TNode conf, InferenceId id)` and
`lemma(TNode lem, InferenceId id, LemmaProperty p)` take no proof generator at
all. So a theory author who writes

```cpp
d_im.lemma(lem, InferenceId::ARITH_MY_NEW_INFERENCE);
```

gets a trust step, silently, and nothing in the code or the review says so. The
ergonomic path is the proofless one.

*The proposal.* Make it explicit at the call site — something like

```cpp
d_im.lemma(lem, InferenceId::ARITH_MY_NEW_INFERENCE,
           NoProof(TrustId::THEORY_INFERENCE_ARITH));
```

so that "this inference has no proof" is a thing someone **typed**, is greppable,
is countable, and forces a *named* `TrustId` rather than a generic one.

*What it buys.* Three things, in increasing order of value: reviewers see it;
the census in
[`TODO.md` M3](../TODO.md#g3--can-we-quantify-over-the-entities-at-all) becomes exact rather
than inferred; and the number of proofless inferences becomes a metric that can
be watched going down.

*Cost.* This is the most invasive rule here — it touches every theory. It is
also the one that would prevent the whole class of problem at the source, so it
is worth proposing even if the answer is "not now."

### H7 — Trusted is declared, never discovered

**`registerTrustedChecker` with an explicit pedantic level is the only way to
have a rule whose checker does not fully check it.**

*Evidence.* cvc5 already does this well: `registerTrustedChecker(id, checker,
level)` with levels 1–4 is an existing, deliberate ladder. The hygiene addition
is to make it **exhaustive** — a rule whose checker silently declines to verify
something, without being registered as trusted, is a hole nobody declared.

*What it buys.* `getPedanticLevel` becomes a trustworthy summary of how much of
a proof is actually checked, and the trust ladder becomes readable off the
registration table instead of by reading every checker.

### H8 — Registration is total, and cvc5 says so itself

**Every `ProofRule` has exactly one registered checker, asserted at startup.**

*Evidence.* 159 of 172 rules are registered; the 13 are two sentinels and the 11
`FF_*` rules behind `#ifdef CVC5_USE_COCOA`.

*How it is checked.* **This one should not be a check here at all.** It is
decidable from cvc5's own registry at startup, so the right deliverable is an
assertion in `ProofChecker` — finding kind D. See
[`tooling.md` D3](tooling.md#d3--where-an-invariant-should-live) for the rule,
and D4 for the promise that if the assertion we propose fires falsely, that is
our bug.

### H9 — The rule documentation is a contract

**The `\inferrule{premises | args}{conclusion}` block in `cvc5_proof_rule.h` is
machine-readable, and matches what the checker reads and what the printer
prints.**

*Evidence.* The documentation is already highly structured — every rule carries
an `\inferrule` with an explicit premise and argument list. It is a
specification that nothing currently validates.

*What it buys.* This is `RULE0010`, and it is one of the two things
[cvc5 asked anoieu for](https://github.com/ajreynol/anoieu/blob/main/docs/README.md).
Making the docstring authoritative means a rule's arity is stated once instead
of three times.

### H10 — The checker's dependencies are the thing to minimize

**The internal proof checker depends on as little of cvc5 as possible, and that
number is measured, published, and ratcheted.**

This is the strictest rule in the document, and the one most directly connected
to the kernel goal. A proof checker is worth what its independence is worth: the
less of cvc5 it needs in order to be correct, the more `--check-proofs` means.

*Evidence.* Measured by [`dokimasia.tcb`](../dokimasia/tcb/), seeded from
`ProofChecker`, `ProofRuleChecker` and all 13 registered theory rule checkers:

```
closure         179 files      41,446 lines
all of src/    1663 files     521,073 lines
                               = 8.0% of cvc5 by line count
```

*The good news first.* The base class is already right —
`ProofRuleChecker(NodeManager* nm)` — and **12 of the 13 rule checkers take
nothing but a `NodeManager*`**. cvc5's design is close to the discipline this
rule asks for.

*Where the weight is.* Six checkers `#include` the headers of the theory solvers
they check, to reach `static` helper functions parked on the solver classes:

| edge | uniquely worth | the header's own closure |
| --- | --- | --- |
| `strings/proof_checker.cpp` → `strings/core_solver.h` | 3,193 lines | 86 files, 21,904 |
| `arith/proof_checker.cpp` → `arith/linear/constraint.h` | 2,556 lines | 29 files, 9,374 |
| `datatypes/proof_checker.cpp` → `theory_datatypes_utils.h` | 1,027 lines | |
| `arrays/proof_checker.cpp` → `theory/rewriter.h` | — | 12 files, 3,840 |

`CoreSolver::getConclusion` and its two siblings are already pure functions of
`NodeManager*` and `Node` — they are simply on the wrong class, and C++ makes
you include the class to reach them.

*And a hypothesis we checked and dropped.* `Env` looked like the culprit, since
`BuiltinProofRuleChecker(NodeManager*, Rewriter*, Env&)` is the one checker that
takes one. Measured, `smt/env.h` closes over **23 files and 7,012 lines** — a
third of `core_solver.h` alone. `Env` is widely included *because* it is thin. A
stripped-down `Env` is an architectural argument, not a line-count one.

*The rule.* **A rule checker includes only what it needs to check a rule.**
Shared conclusion-computing helpers belong in dependency-light headers that both
the solver and the checker include — not on the solver class.

*The connection to H7.* A checker that is *handed a rewriter* cannot be checking
that rewriter: `MACRO_REWRITE`'s checker replays the rewrite with the same code
that produced it. cvc5 already says so, by registering that rule through
`registerTrustedChecker` at pedantic level 4. The dependency measurement and the
pedantic ladder are two languages for one fact, and they should agree.

*How it is enforced.* `python3 -m dokimasia.tcb baseline <cvc5> --check` in CI.
The ratchet turns one way. This is the one measurement in this repository
designed to be watched over time rather than resolved once.

*Filed as* [`findings/tcb-001.md`](findings/tcb-001.md), with the refactoring.


### H11 — The RARE correspondence is stated, not inferred

**Every `ProofRewriteRule` says where it came from, and a RARE rule's owning
theory is recoverable from its name or its marker.**

*Evidence.* 533 rules: **439 generated from RARE, 94 hand-written.** The
correspondence for the generated half already exists and is **exact in both
directions** — `mkrewrites.py` emits

```cpp
/** Auto-generated from RARE rule bool-double-not-elim */
EVALUE(BOOL_DOUBLE_NOT_ELIM),
```

and 439 markers match 439 definitions with nothing left over on either side. It
holds because it is *generated*: nobody maintains it, so it cannot drift. That
is the model the rest of this document keeps asking for, already working.

*Where it is nonuniform.* Four things, in increasing order of how much they cost
a consumer:

1. **Hand-written entries are identified by absence.** A rule is hand-written
   iff it has *no* marker. That is inference from silence: a generator change
   that dropped markers would silently reclassify 439 rules.
2. **The marker names the rule but not its file**, so the owning theory is not
   recoverable from the header. Every consumer has to go find the RARE files.
3. **RARE files have six basenames** — `rewrites`, `rewrites-card`,
   `rewrites-elimination`, `rewrites-regexp-membership`,
   `rewrites-simplification`, `rewrites-transcendentals` — and no extension, so
   they must be located by content. *(This one bit us: an early version of
   `dokimasia.rewrites` globbed `theory/*/rewrites` and undercounted by 118
   rules, reporting 212 hand-written where the true figure is 94.)*
4. **Rule-name prefixes do not determine the theory.** `ite-` is claimed by both
   `booleans` and `builtin`; `strings` uses three prefixes (`str`, `re`, `seq`),
   `uf` three (`uf`, `eq`, `distinct`), `booleans` two.

*The convention, in the order worth doing it.*

- **C1 — put the source file in the marker.** One line in `mkrewrites.py`:
  `/** Auto-generated from RARE rule bool-double-not-elim (theory/booleans/rewrites) */`.
  Fixes (2) and makes (3) and (4) not matter to any consumer of the header,
  because ownership stops being something you have to reconstruct. **Highest
  value per effort by a distance.**
- **C2 — mark the hand-written entries too**, with something as plain as
  `/** Hand-written theory rewrite */`. Turns (1) from an inference into a fact.
- **C3 — one prefix, one theory.** `ite-` is the only outright collision;
  several theories using several prefixes is untidy but unambiguous, so this is
  worth doing only if it is cheap.
- **C4 — settle the file naming**, or write down that it is deliberately free
  and consumers must scan by content. Either is fine; the present state is
  neither.

*What this buys.* The rewrite vocabulary is the largest in the calculus and the
one where "is this rule declarative or is it C++ someone must teach the seam
about" decides whether a proof can be printed. Today that question is answered
by cross-referencing two directories. C1 and C2 make it a property of the
header.

### On an auto-compiler for RARE rules

Worth taking seriously, and worth being precise about what it means — cvc5
already compiles RARE rules into a rewrite database and a discrimination tree.

The interesting question is not "compile the rules" but **"can rewrite proof
reconstruction be made to terminate without a depth bound?"** That is an open
research problem, and the reasons are set out with citations in
[`rare-correspondence.md`](rare-correspondence.md): applying one rule spawns
recursive sub-problems — its preconditions, and the gap between its instantiated
right-hand side and the target — which are not provably simpler than the goal.
[FMCAD 2022](https://homepage.divms.uiowa.edu/~ajreynol/fmcad2022.pdf) says so
outright, which is why the depth limit exists at all.

The risk worth naming separately: RARE's value is that a rule is *checkable by
construction* and shared with the Eunoia signature. A DSL extended until it can
express every hand-written rewrite is a general-purpose language, and a
general-purpose rule is exactly as trustworthy as C++. **Coverage is not the
goal; sharing a definition with the signature is.**


---

## What to do with this document

cvc5's proof documentation is **161 lines across five files**, and
`docs/proofs/proofs.rst` is an overview that points at the rule list and the
output formats. **There is no contributor guide for adding a proof rule or an
inference id.**

So the natural home for a settled version of this is upstream, as that missing
guide — which makes it a finding of kind C, and a more useful one than most
defects. A convention that is written down is enforced by reviewers on every
pull request, for free, forever; a convention enforced only by our checker is
enforced nightly, by us, at a cost.

The order of business:

0. **Measure H10 continuously**, starting now. It needs nobody's agreement to
   be useful, and the number is the argument.
1. **Propose** the rules that are already near-universal (H2, H3, H7, H8) —
   these ratify existing practice and should be uncontroversial.
2. **Argue** the ones that cost something (H1's 76 exceptions, H5's missing
   rule, H6's API change), with the measurements above attached.
3. **Write the checks only for what is accepted.** A check enforcing a
   convention its owners have not agreed to is noise, and it will be turned off.
4. **Prefer an assertion or a documented rule over a check of ours**, every
   time.

## What this buys the kernel

Restating the through-line, because it is the reason this comes first.

| hygiene rule | what it makes possible |
| --- | --- |
| H1, H2 | "the inferences of theory X" becomes an enumerable set |
| H3, H4 | an entity's owner is readable from its name, so the boundary can be drawn by *naming* rather than by tracing |
| H5 | "does this inference have a proof" becomes a total function |
| H6 | the proofless set becomes explicit, countable, and watchable |
| H7, H8 | the trust ladder is readable off a table instead of reconstructed |
| H9 | a rule's contract is stated once |
| **H10** | **the checker becomes small enough to be the kernel, and the number is watched** |
| H11 | a rule's origin — declarative or hand-written — is a fact in the header, not a cross-reference |

None of that verifies anything. All of it shortens the argument — which is the
actual goal.
