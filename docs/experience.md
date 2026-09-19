# Experience: the defects we found in cvc5

**One entry per concrete defect**, newest first, each in the same shape: what was
wrong in cvc5, what happened to it, and what that says about the check that
found it. A defect leaves this page only by being written up in it — nothing is
edited away, and a claim that turned out false stays as
a retraction.

This is not the record of an observation. That is
`bug_db/`: identities, dates, archived evidence and the
`closed_*` fields a closure adds. The database says *that* a change closed an
observation; this page says what it meant. How the page is written and what each
field has to carry is at the foot.

## Where this stands

**Five entries, one closed.** The log below covers cvc5
`40a4bb7e4..dbf176dfb` and the branch answering `tcb-001`: one defect closed by
a merged pull request, one acted on and not yet merged, one filed and open, and
two questions that turned out to be no defect at all. A thin log is the honest
reading of a thin window, not a backlog of write-ups nobody got to.

The open hypotheses that have *not* reached this page — the ones still waiting
for a verdict — are the register in `docs/README.md`.
A row moves here when something happened to it.

## The log

### 2026-09-19 — the proof checkers included headers they never used

| | |
| --- | --- |
| **Status** | **acted on by cvc5**, in the branch answering `tcb-001` |
| **Identity** | `f-1` — filed finding, not a database observation |
| **Found by** | `dokimasia.tcb cuts`, then `Closure.edge_use` |
| **In cvc5** | `theory/arith/proof_checker.cpp`, `theory/datatypes/proof_checker.cpp`, `theory/builtin/proof_checker.cpp` |
| **Attribution** | cites us — the response names the report and re-runs `dokimasia.tcb measure` |

**Summary:** Three of cvc5's proof checkers pulled in headers they made no use
of, which made the code a proof checker must be right about look larger than it
is. Deleting four lines removed 38 files from that surface.

**What was wrong:** `theory/arith/proof_checker.cpp` included
`theory/arith/linear/constraint.h` and referenced none of the names it declares;
`theory/datatypes/proof_checker.cpp` did the same with `theory/rewriter.h` and
`expr/dtype_cons.h`, and `theory/builtin/proof_checker.cpp` with
`theory/quantifiers/extended_rewrite.h`. A dead include still enters the
compile-time closure, so each one inflated the checker's trusted surface for
nothing.

**What cvc5 did:** Removed all four includes, and separately extracted the
helpers behind the two *live* solver dependencies: `getConcatConclusion`,
`getDecomposeConclusion`, `getExtensionalityConclusion`,
`getSufficientNonEmptyOverlap`, `eagerReduce` and `lengthPositive` moved to
`strings::utils`, so the strings checker no longer includes `core_solver.h` or
`term_registry.h`. Validated by byte-for-byte identical CPC proofs on five
benchmarks and 525 passing regressions. **The measured closure fell from 179
files / 41,448 lines to 141 / 31,541.**

**Learned:** The check was pointing at something real and **the report attached
the wrong mechanism to part of it** — see the retraction below. The lesson is in
the tool now: `cuts` weighed an include by how much closure it carried and never
asked whether the file used what it included, so a dead include and a
load-bearing one produced identical rows and the prose supplied a reason for
both. Weight and deadness are different questions, and a cut list answers only
the first.

### 2026-09-19 — `SUBS`'s documentation omitted an argument its checker reads

| | |
| --- | --- |
| **Status** | **closed** by [cvc5 #12948](https://github.com/cvc5/cvc5/pull/12948) — `6e62c7cf595273b7fdfdc0a607aa53a8555530ee` |
| **Identity** | `dokimasia:398b7ed5b492831606d98491` (`SIG0003`) |
| **Found by** | `dokimasia.signature checker` |
| **In cvc5** | `include/cvc5/cvc5_proof_rule.h`, against `theory/builtin/proof_checker.cpp` |
| **Attribution** | cites us — *"Based on an initial pass from ajreynol/dokimasia"* |

**Summary:** cvc5's substitution proof rule takes a third argument that selects
how the substitutions get applied, but its reference documentation described
only two. A reader building or auditing such a proof would not have known the
argument was there.

**What was wrong:** The `\inferrule` block above `EVALUE(SUBS)` read
`\inferrule{F_1 \dots F_n \mid t, ids?}`, and its prose said the substitutions
are *"applied in reverse order"* as though that were the only possibility.
`BuiltinProofRuleChecker::checkInternal` has all along asserted
`1 <= args.size() && args.size() <= 3` and read `args[2]` as a second
`MethodId`, `ida`, defaulting to `SBA_SEQUENTIAL`.

**What cvc5 did:** Rewrote the block to
`\inferrule{F_1 \dots F_n \mid t, ids?, ida?}`, restated the conclusion as
`\texttt{apply}_{ida}(t, \sigma_{ids}(F_1), \dots)`, and named the three modes
— `SBA_SEQUENTIAL`, `SBA_SIMUL`, `SBA_FIXPOINT` — with the termination condition
the fixpoint mode requires. **The checker was not touched; the documentation was
brought up to it.** The same pull request deleted four dead `TrustId`s and
fourteen unproduced `InferenceId`s, which closed nothing here: none carried an
observation.

**Learned:** `SIG0003` compares two partial parsers — LaTeX on one side,
`Assert`s and subscript reads on the other — and the worry was that a
disagreement between two approximations is an artifact rather than a finding.
Here it was not, and the fix landed on the side the check said was wrong. What
made this row actionable where others in the same facet are not: it named one
rule, one file, and two numbers to compare, so confirming it took reading a
single comment and a single `else if`. The 24 `SIG0002` rows name a skolem and a
file but no comparable discriminator, and none of them moved.

### 2026-09-18 — six proof rule checkers compile against the solvers they check

| | |
| --- | --- |
| **Status** | **filed**, partly addressed — see the entry above |
| **Identity** | `f-1` / `R3` |
| **Found by** | `dokimasia.tcb measure`, `cuts`, `why` |
| **In cvc5** | `theory/*/proof_checker.cpp` |
| **Attribution** | ours, reported |

**Summary:** The component that decides whether a cvc5 proof is valid is worth
as much as it is small, and six of its thirteen rule checkers were compiled
against the theory solvers they check.

**What was wrong:** the helpers those checkers want are `static` methods parked
on solver classes — pure functions of `NodeManager*` and `Node` that do not need
the solver — and C++ makes you include the whole class to reach one. The
coupling is lexical rather than semantic, which is why the fix is mechanical.
The full writeup as filed follows, including the correction to its original
account of *why* each edge existed.

**Learned:** the closure figures were right throughout and the mechanism
attached to them was not, which is the retraction below. A measurement can be
exactly correct and still carry a wrong story if the tool never checked the
story.

**Status:** open · **Kind:** C (a change to the pipeline) · **Reported against:**
cvc5 `40a4bb7e4` · **Severity:** not a bug — an architectural coupling with a
cheap, local fix

#### Summary

cvc5's internal proof checker is the natural candidate for a trusted kernel: it
is the component that decides whether a cvc5 proof is valid. Its value depends
on how little of cvc5 it needs to be correct.

The base class is already disciplined — `ProofRuleChecker(NodeManager* nm)` —
and **12 of the 13 registered rule checkers take nothing but a `NodeManager*`**.

But six of them `#include` the headers of the *theory solvers they are checking*.
For the strings checker this is to call `static` helper functions that live on
the solver class: pure functions of `NodeManager*` and `Node` that do not need
the solver, reached by including the whole class. Including the solver drags its
entire header closure into the checker's.

> **Corrected 2026-09-19, and the correction is ours.** This section originally
> gave that mechanism for all six edges. cvc5 replied that the arithmetic
> checker uses nothing from `linear/constraint.h` and the datatypes checker
> nothing from `theory/rewriter.h`: those includes were simply dead, and were
> removed in one line each with no helper extraction. **The measurement never
> established the mechanism** — `cuts` weighed include edges by closure size and
> could not see whether a file used what it included, so a dead include and a
> load-bearing one appeared in the same list and the prose supplied a reason for
> both. The tool now classifies every edge `used`, `unused` or `unknown`
> (`dokimasia.tcb cuts`, and `Closure.dead_includes`), and
> `tests/test_tcb.py` pins these three edges by name. The closure figures below
> are unchanged: they were never what was wrong.

The result: the checker's compile-time dependency surface is **179 files,
41,446 lines — 8.0% of `src/`** — and it contains `theory/strings/core_solver.h`,
`theory/arith/linear/constraint.h`, `theory/theory.h` and `theory/rewriter.h`.

The fix is mechanical, local, and does not change behaviour: move the pure static
helpers out of the solver classes into dependency-light headers that both the
solver and the checker include.

#### How to reproduce

No build required; the tool reads a source tree.

```bash
git clone https://github.com/ajreynol/dokimasia && cd dokimasia
python3 -m dokimasia.tcb measure <cvc5>            # the headline figures
python3 -m dokimasia.tcb cuts    <cvc5>            # what each edge costs
python3 -m dokimasia.tcb why     <cvc5> theory/strings/core_solver.h
```

Seeds are `ProofChecker`, `ProofRuleChecker` and all 13 registered theory rule
checkers (`SEED_SETS["proof-checker"]`).

#### The measurement

```
closure         179 files      41,446 lines
all of src/    1663 files     521,070 lines
                               = 8.0% of cvc5 by line count
```

Ten theory subsystems are inside it. The heaviest individual checkers:

| checker | closure |
| --- | --- |
| `theory/strings/proof_checker.cpp` | 105 files, 26,985 lines |
| `theory/builtin/proof_checker.cpp` | 72 files, 17,150 lines |
| `theory/arith/nl/transcendental/proof_checker.cpp` | 55 files, 13,811 lines |
| `theory/arith/proof_checker.cpp` | 52 files, 13,153 lines |

#### The finding

Every load-bearing edge is a checker including a solver. `cuts` reports what each
is uniquely worth — the lines that leave the closure if that one `#include` goes:

**Every load-bearing edge is a checker including a solver — and not every edge is
load-bearing.** The `use` column is what the original table lacked: `used` means
the file references something the header declares, so the line cannot go until
the declaration moves; `unused` means it references nothing, so deleting the line
is the whole fix.

| from | include | uniquely worth | use | that header's own closure |
| --- | --- | --- | --- | --- |
| `theory/strings/proof_checker.cpp` | `theory/strings/core_solver.h` | **3,193 lines** | used | 86 files, 21,904 lines |
| `theory/arith/proof_checker.cpp` | `theory/arith/linear/constraint.h` | **2,556 lines** | **unused** | 29 files, 9,374 lines |
| `theory/datatypes/proof_checker.cpp` | `theory/datatypes/theory_datatypes_utils.h` | 1,027 lines | used | |
| `theory/arith/nl/transcendental/proof_checker.cpp` | `theory/arith/nl/transcendental/sine_solver.h` | 809 lines | used | |
| `theory/datatypes/proof_checker.cpp` | `expr/dtype_cons.h` | 479 lines | **unused** | |
| `theory/builtin/proof_checker.cpp` | `rewriter/rewrite_db.h` | 332 lines | used | |
| `theory/builtin/proof_checker.cpp` | `theory/quantifiers/extended_rewrite.h` | 270 lines | **unused** | 11 files, 3,568 lines |
| `theory/builtin/proof_checker.cpp` | `smt/term_formula_removal.h` | 237 lines | used | |
| `theory/arrays/proof_checker.cpp` | `theory/rewriter.h` | — | **unused** | 12 files, 3,840 lines |

**19 seed includes in all reference nothing their header declares**, 3 of which
shrink the closure; the other 16 are reachable by another path and are dead
anyway. `python3 -m dokimasia.tcb cuts <cvc5>` lists them.

#### Root cause

The helpers the checkers want are `static` methods on solver classes. From
`theory/strings/core_solver.h`:

```cpp
static Node getConclusion(NodeManager* nm, ...);              // :267
static Node getDecomposeConclusion(NodeManager* nm, ...);     // :309
static Node getExtensionalityConclusion(NodeManager* nm, ...);// :325
```

and `theory/strings/proof_checker.cpp` calls exactly these three, at lines 239,
266 and 502. They take a `NodeManager*` and `Node`s, touch no solver state, and
are *already* written as pure functions. They are simply parked on the wrong
class, and C++ makes you include the whole class to reach them.

This is a good sign, not a bad one: the coupling is lexical, not semantic. The
checker and the solver genuinely share a conclusion-computing function — which
is correct and desirable, since the checker should compute the same conclusion
the solver claimed — but sharing it should not mean depending on the solver.

#### Proposed refactoring

**Extract the shared pure helpers into dependency-light headers.**

Taking strings as the worked example:

1. Add `theory/strings/core_conclusions.h` — or extend the existing
   `theory/strings/theory_strings_utils.h`, which is light (10 files, 3,454
   lines) and already the home for this sort of thing.
2. Move `getConclusion`, `getDecomposeConclusion` and
   `getExtensionalityConclusion` there as free functions in
   `cvc5::internal::theory::strings`. They are already `static` and already take
   a `NodeManager*`, so the move is a cut-and-paste plus a namespace.
3. `CoreSolver` includes the new header and calls the free functions (or keeps
   thin forwarding wrappers, if call sites elsewhere are numerous).
4. `theory/strings/proof_checker.cpp` includes the new header **instead of**
   `core_solver.h`.

Result: −3,193 lines from the checker's closure, and — the part that matters
more than the number — `StringProofRuleChecker` stops compiling against
`CoreSolver` entirely.

The same shape applies to `transcendental` ↔ `sine_solver.h`, which is `used`.
**It does not apply to `arith/proof_checker.cpp` ↔ `linear/constraint.h`**, where
the include is dead and `git rm` of one line is the entire change — as cvc5
established, and as the tool now reports without being told.

#### On `Env` — we checked, and it is not the problem

An earlier hypothesis was that `Env` was the culprit, since
`BuiltinProofRuleChecker` is the one checker that takes one:

```cpp
BuiltinProofRuleChecker(NodeManager* nm, Rewriter* r, Env& env);
```

**Measured, `smt/env.h` closes over 23 files and 7,012 lines** — a third of the
weight of `core_solver.h` alone. `Env` is widely included precisely because it is
thin. So a stripped-down `Env` is *not* where the lines are, and we would not
propose one on size grounds.

There is still an argument for a narrow `ProofCheckerContext` (a `NodeManager*`,
the handful of options the checkers read, and a `Rewriter*` where genuinely
required), but it is an *architectural* argument — it makes "a checker cannot
reach the solver" true by construction rather than by convention — not a
line-count one. We would rather see the solver-header extraction done first; it
is cheaper and it is where the weight actually is.

#### Why this is worth doing

`--check-proofs` is most valuable when the checker is small and independent of
the code that produced the proof. Two of these couplings are directly
self-referential: `theory/arrays/proof_checker.cpp` includes `theory/rewriter.h`,
and `BuiltinProofRuleChecker` is *handed* a `Rewriter*` — so `MACRO_REWRITE` is
checked by replaying the rewrite with the same rewriter that produced it. cvc5
already knows this and says so, by registering that rule through
`registerTrustedChecker` at pedantic level 4. The dependency measurement and the
pedantic ladder are two descriptions of one fact.

Shrinking the checker's dependency surface is also the most concrete step
available toward being able to say *which part of cvc5 is its proof kernel* —
an argument that gets shorter every time a coupling like this is removed.

#### Keeping it fixed

```bash
python3 -m dokimasia.tcb baseline <cvc5> --write   # record
python3 -m dokimasia.tcb baseline <cvc5> --check   # fail if it grew
```

Runs in seconds, needs no build, and fits cvc5's existing nightly. The ratchet
turns one way; if growth is intended, the baseline moves in the same commit with
a reason.

#### What we got wrong first

Recorded because our own errors belong in the same place as our findings.

The first version of this measurement reported that the checker depended on
**74% of `src/`**. That was an artifact. The tool had a mode that followed each
reached header to its `.cpp`, as a proxy for "what could execute". Once any
`.cpp` enters the closure it includes further headers, whose `.cpp` files follow,
and the closure saturates at cvc5's whole link unit: seeding from
`printer/printer.cpp` — unrelated to proof checking — produced the identical
383,760-line figure.

A measure that returns the same answer for every seed measures nothing. The mode
is no longer the default and now prints a warning. The 8.0% figure above is the
compile-time surface, which discriminates.

The real lesson: "what could execute during checking" is a **call-graph**
question, not an `#include` question, and answering it properly needs a build.

**Known under-approximation:** generated headers are invisible to the tool.
`options/options.h` is produced from the `.toml` files at build time and is not
in the source tree, so edges through it are not followed.

### 2026-09-17 — cvc5 #12905: a real bug report that is not a proof bug

| | |
| --- | --- |
| **Status** | **no defect of ours** — a routing question, answered with a boundary |
| **Identity** | — |
| **Found by** | a maintainer's request |
| **In cvc5** | [#12905](https://github.com/cvc5/cvc5/issues/12905), `theory_engine.cpp:2030` |
| **Attribution** | n/a |

**Summary:** A fatal cvc5 failure on a strings benchmark was routed here. It is
a real bug and not a proof-completeness one, so what this repository owed was a
boundary rather than a verifier.

**What was wrong:** nothing of ours. The question was whether an assertion
failure reachable from an ordinary benchmark is this repository's subject, and
the answer turns on whether the reproducer produces a *proof hole* — which it
does not.

**Learned:** the routing test is cheap and worth having written down, because
more of these will arrive. A case that ends in a boundary constrains future
behaviour exactly as a verifier does.

**The request.** cvc5 [#12905](https://github.com/cvc5/cvc5/issues/12905) — a
fatal failure at `theory_engine.cpp:2030` on a strings-and-quantifiers
benchmark:

```
(declare-const x Int)
(assert (exists ((s String) (t Int))
  (and (= 1 (str.len (str.++ (str.substr s 0 1) (str.at s t))))
       (not (str.suffixof (ite (str.in_re "/" (str.to_re s))
                               (str.substr s 0 x)
                               (str.replace "/" s "")) s)))))
(check-sat)
```

> *wasn't sent to you, so why are you explaining it trivially, for fact
> `(not (= (+ (str.len @quantifiers_skolemize_2) (* (- 1) (str.len @purify_4))) 0))`*

**This is not a proof bug.** It is a theory-explanation defect: a fact reached
the explanation machinery that the engine did not think it had sent. Nothing in
it concerns whether a step can produce a proof, which is the whole of what this
repository is for.

**Two questions follow, and they have different answers.**

#### 1. What does this repository do with it?

**Nothing, and it says so.** dokimasia holds one role — *what no proof step
covers* — and an assertion failure in theory combination is not it. Taking it
would be the most ordinary failure mode available to a tool with a working
analysis and spare attention: scope creep dressed as helpfulness.

The register stays clean: #12905 gets no `i-` id, because
the register (`docs/README.md`) is *things we are asking cvc5 to act on*, and we are
asking nothing. cvc5 already has the report; a second opinion from us is not a
contribution.

**The one thing worth checking is whether the classification is right.** "Not a
proof bug" is a claim, and the cheap version is: does the reproducer produce a
proof hole? If it did, the issue would be partly ours after all. That check is
the corpus sweep (`docs/maintenance.md`) pointed at one file, and it costs a
minute.

#### 2. Where does the *learning* live?

This is the question worth a case study, because the answer is not "nowhere".

The maintainer will answer #12905 — reproduce it, locate it, fix it or explain
why it is not a bug. **That answer is evidence about how cvc5 issues get
addressed**, and it is evidence this repository is well placed to collect and
badly placed to act on. We ran assistants against cvc5 issues already, through a
`prompts/check_cvc5_issue` launcher since retired with the rest of that
workflow; what we have never done is record what the human answer taught that
the assistant missed.

**The current home is [Paideia](https://github.com/ajreynol/paideia).** The
original decision was to start `empeiria` as a child project under Dokimasia's
`tools/`, using the existing issue workflow and reporting discipline. On
2026-09-18, the maintainer moved it and `anakrisis` to Paideia. That repository
is now the source of truth for their charters, plans, protocols and ledgers.

[Empeiria's charter](https://github.com/ajreynol/paideia/blob/main/tools/empeiria/README.md)
owns the question of **working a cvc5 bug and learning from how the maintainers
answered**. General cvc5 development belongs there. Dokimasia keeps the proof
question: if an issue exposes a proof-completeness gap, that gap enters this
repository's register. Performance, including proof-production overhead,
belongs to
[Tachyon's Elaphros](https://github.com/ajreynol/tachyon/tree/main/tools/elaphros)
and is outside this repository's scope.

#### What the original decision sought to change

The maintainer's side of the loop was already defined — that launcher wrote a
`TRIAGE:` block and left `HUMAN RESPONSE:` empty for a person. What was missing
is what happened **after** the response arrived: the answer was read and the
file was forgotten.

The change is small and is the whole point: **the response is an artifact, and
the delta between it and the triage is the thing worth keeping.** Not the
issue, not the fix — the difference between what an assistant concluded and what
a maintainer did. The work to record and learn from it belongs to Paideia,
which carries its status.

#### Verdict

| | |
| --- | --- |
| **never** — for the issue itself | #12905 is not ours. No id, no register row, no report. The only work it earns is confirming it produces no proof hole |
| **carry — to ourselves** | the routing decision; [Empeiria in Paideia](https://github.com/ajreynol/paideia/tree/main/tools/empeiria) holds the general bug-work question |
| what would change it | the reproducer turning out to produce a trust step or an unhandled rule, which would make it partly a proof bug and partly ours |

**What we are not claiming.** We have not run the reproducer. The
classification rests on reading the assertion message, which names theory
explanation and not proof production — good enough to decline the issue, not
good enough to assert there is no proof hole behind it. That check is queued,
not done.

#### A note on scope, since more of these will arrive

The generalisable part is the second question, not the first. Declining
out-of-scope work is easy and this repository should keep doing it. The harder
discipline is **noticing that the out-of-scope thing still produced evidence**,
and putting the evidence somewhere with a boundary around it rather than either
absorbing it or throwing it away.

The routing test, for the next one:

1. **Is it ours?** If it is about whether a step can produce a proof, it is a
   normal candidate and goes in the register.
2. **Is it about performance?** Time and memory overhead, including that of
   producing proofs, belong to
   [Tachyon's Elaphros](https://github.com/ajreynol/tachyon/tree/main/tools/elaphros).
3. **Is it general cvc5 development or learning from that work?** Route it to
   [Paideia](https://github.com/ajreynol/paideia); its project charters determine
   what work it takes on.
4. **If none applies, decline it and say why in one line.** Silence reads as
   agreement, and a tool that quietly collects other people's problems has
   stopped having a role.

### 2026-09-17 — cvc5 #12899: is forbidding safe mode with debug symbols a restriction?

| | |
| --- | --- |
| **Status** | **no defect** — the decision is sound, and now has a verifier behind it |
| **Identity** | — no observation: `BUILD0001` returned none, which is the result |
| **Found by** | `dokimasia.buildmode check` — 8 conditionals, all benign |
| **In cvc5** | `configure.sh`, and the eight `CVC5_SAFE_MODE` conditionals in `src/` |
| **Attribution** | ours, offered |

**Summary:** cvc5 forbids combining a safe build with debug symbols. The
question worth answering was not why it is forbidden but what forbidding it
costs, and that rests on an invariant a check can hold.

**What was wrong:** nothing — the decision is a reasonable simplification, and
reading it as an oversight would have got the case wrong. What was missing was
any way to know it stays cheap: the claim *a safe build differs only in
defaults, text and reporting* is checkable, and nothing was checking it.

**Learned:** this is the shape to repeat. An opinion is worth nothing to
somebody who knows the code better than we do; a reading of the source is worth
something once. The invariant with the verifier attached is the only answer that
survives the next edit.

**The design decision.** cvc5's configure script does not allow a safe build to
be combined with debug symbols. This is **deliberate and for clarity**: the
build already carries a large configuration space, and every combination
permitted is one more thing to explain, test and keep working. Forbidding a
combination nobody has needed is a reasonable simplification, and
[#12899](https://github.com/cvc5/cvc5/pull/12899) flattening the build system is
the natural moment to ask whether it is still the right one.

**The research question is not why it is forbidden.** It is: **does forbidding
it actually deny anyone anything?**

**Our answer:** almost nothing, and we can say exactly what the *almost* is. A
safe build differs from an ordinary build in one semantic respect — the default
value of a runtime option — so an unrestricted debug build run with
`--safe-mode=safe` reproduces a safe build's *behaviour* exactly. What it does
not reproduce is the diagnostic text, and that text is read by the regression
testers.

**So the simplification is currently free, and the reason it is free is an
invariant that nothing in cvc5 maintains.** That is what this case is really
about, and what
[`dokimasia.buildmode`](../dokimasia/buildmode/) exists to protect.

*Measured against cvc5 `40a4bb7e4`.*

#### What a safe build actually is

`ENABLE_SAFE_MODE` does three things in `CMakeLists.txt`: defines
`-DCVC5_SAFE_MODE`, turns off `USE_POLY` / `USE_COCOA` / `USE_NORMALIZ`, and
changes the printed build profile. The macro is referenced in **eight places in
all of `src/`**, and every one falls into one of three categories:

| where | what it does | category |
| --- | --- | --- |
| `options/options_template.cpp` | `d_base->safeMode = options::SafeMode::SAFE` in the `Options` constructor | **an option default** |
| `base/configuration_private.h` | `#define IS_SAFE_BUILD true` | build self-report |
| `smt/logic_exception.h` | prepends `"Logic restricted in safe mode. "` | message text |
| `theory/theory_rewriter.cpp` | omits `" Try --ff."`-style hints | message text |
| `smt/illegal_checker.cpp` | omits `" Try --arrays-exp."`-style hints | message text |

Two further facts complete the picture:

- **No source file is excluded.** `src/CMakeLists.txt` never mentions
  `ENABLE_SAFE_MODE`; a safe build compiles the same translation units.
- **Nothing branches on the build.** `Configuration::isSafeBuild()` has exactly
  one caller — `options_handler.cpp`, printing `--show-config`. It is reported,
  never acted on.

The safe build's only semantic act is to change the *starting value* of a
runtime option, which is exactly what `--safe-mode=safe` does.

#### What the restriction costs

Three things a safe build gives you, and whether a debug build with
`--safe-mode=safe` gives them too:

| | reproduced by `--safe-mode=safe`? |
| --- | --- |
| the solver's behaviour — what is accepted, rewritten, proved | **yes, exactly.** It is the same option, set the same way |
| the three optional libraries being absent from the binary | **no** — they are linked and simply not reached |
| the diagnostic text, including the `"in safe mode"` prefix | **no** — that is decided at compile time |

Only the third is a cost to a developer, and it is a real one:

**The exception text is load-bearing for CI.** `SafeLogicException` prepends
`"Logic restricted in safe mode. "` at compile time, and
`smt/logic_exception.h` says why that matters:

> *The regression testers will consider any exception having text "in safe mode"
> or "in stable mode" as an admissible failure, and skip the benchmark.*

Verified on an unrestricted binary at `--safe-mode=safe`:

```
$ cvc5 --safe-mode=safe cos.smt2
(error "Cannot handle assertion with term of kind cos in this configuration.")
```

No `"in safe mode"` prefix — a safe build emits one. The same run also *keeps* a
hint a safe build drops:

```
$ cvc5 --safe-mode=safe ff.smt2
(error "Cannot handle assertion with term of kind CONST_FINITE_FIELD in this
        configuration. Try --ff.")
```

**Consequence:** a benchmark that a safe build *skips*, an unrestricted build at
`--safe-mode=safe` *fails*. So the restriction bites in exactly one situation —
**debugging a safe-mode regression skip** — where you would want a debug binary
that produces safe-build diagnostics, and cannot have one. Whether anybody has
wanted that is a question for cvc5, not for us. Our contribution is that the
list is this short, and that we can keep it this short.

#### The invariant, and why it is the real subject

> **A safe build differs from an unrestricted build only in (a) the default
> value of the `safeMode` option, (b) the text of diagnostics, and (c) what the
> build reports about itself. No solver behaviour is gated on the build macro.**

**This invariant is what makes the configure restriction cheap.** While it
holds, refusing safe + debug denies a developer only the diagnostic text, and
the simplification pays for itself. If it ever stops holding — if some behaviour
becomes reachable in a safe build and not under `--safe-mode=safe` — then the
same configure line stops being a simplification and becomes a genuine
restriction, because no runtime flag substitutes for the build any more.

Nothing in cvc5 currently maintains it. It holds today by accident, and the
natural way to add a safe-mode restriction is `#ifdef CVC5_SAFE_MODE` around the
restriction, which would break it on the first use. **The invariant is worth
maintaining deliberately, and it is cheap to maintain**: it is a property of
eight lines that a check can read in a tenth of a second.

Keeping it also has a benefit beyond this question: while it holds, "safe mode"
is unambiguous. Every claim anyone makes about safe mode — ours included — is
true of both the build and the flag, and nobody has to say which.

#### The check

```bash
python3 -m dokimasia.buildmode check <cvc5>    # BUILD0001
python3 -m dokimasia.buildmode sites <cvc5>    # every conditional, classified
```

It enumerates every `CVC5_SAFE_MODE` / `CVC5_STABLE_MODE` conditional and
classifies each as an option default, a diagnostic, or a build self-report. The
classifier is **closed**: anything it does not positively recognise is reported,
so a new conditional has to argue for itself rather than slip through. It also
fails if a source file becomes excluded from a safe build, or if anything starts
branching on `isSafeBuild()`.

One block — the hint selection in `illegal_checker.cpp` — is message-only but
computes *which* hint to print, which the classifier is too strict to see. It is
allowlisted with a hash of its contents, so editing it re-triggers review rather
than silently staying approved.

`tests/test_buildmode.py` checks that the verifier fires on each way the
invariant can break, because a checker nobody has seen fail is a checker nobody
should trust.

#### What we would ask of cvc5

**Not a change to the configure script.** The restriction is a reasonable
simplification and we are not arguing against it; whether the one lost
capability — a debug binary with safe-build diagnostics — is worth a
combination in the build matrix is cvc5's call, and depends on whether anyone
has ever wanted it.

**What we would ask for is the invariant, maintained.** Run `BUILD0001` as a
kind B adoption: seconds, no build, no dependencies. Its value
is not the eight sites it finds today — it is that the ninth gets noticed, and
that the configure simplification keeps being free.

Better still if cvc5 owns it rather than us. The same property could be a
build-time test or an assertion in their tree, at which point our check retires.
That is the kind D outcome and we prefer it.

#### Verdict

| | |
| --- | --- |
| **carry** | the answer to the question #12899 raised, with the check as evidence |
| rules it clears | `theirs-not-ours`, `run-it` (the diagnostic divergence is demonstrated, not argued), `cheap-to-refute`, `falsifiable`, `worth-the-attention` |
| falsified by | a `CVC5_SAFE_MODE` conditional that gates behaviour — which is what the check looks for; or a developer naming a use for safe + debug that the flag does not cover, which would make the restriction a real cost after all |

**What we are not claiming.** We have not built a safe build and compared
binaries. The equivalence argument is static and exhaustive over the eight
sites; the divergence we demonstrate empirically is the diagnostic text. A
direct A/B of a safe build against `--safe-mode=safe` over the regression suite
would settle it completely, and needs a build we do not have.

## Retractions

Kept visible, because the log of what we got wrong is the more useful half. Each
is a claim we made about cvc5 that turned out to be false.

Kept visible, because the log of what we got wrong is the more useful half.

| # | what we claimed | what was true |
| --- | --- | --- |
| `i-3` / `R2` | `checkProofsComplete` should stop being an **expert** option, so the safe-mode tester can name the guarantee it is testing | **the ask was for cvc5 to weaken the thing we were auditing, and it was rejected.** An option's category governs *both* assignments: promoting it also permits `--no-check-proofs-complete` and `(set-option :check-proofs-complete false)`, and `setDefaultsPre` honours an explicit user assignment through `checkProofsCompleteWasSetByUser`. So the promotion converts a guarantee that safe mode turns on into one a user can switch off — **the expert refusal is the mechanism keeping it non-negotiable, not an obstacle to stating it.** cvc5 built the promotion at `a960d7d7210e731cf48ad7baa6ad42fc7345b297`, reproduced the opt-out, and reverted it at `215eed21a6c8380075c46513e69181a295b6e3b2`. We reasoned from *the positive flag is refused* to *the option should be settable* without asking what else becomes settable, and one `--no-` run would have shown it. The chain's fifth link, `explicit-completeness`, is withdrawn from `CiModel.completeness_chain` and its `CI0002` entity retired; links three and four carry the exposure that is real. The surviving ask is the assertion form alone, and cvc5 notes it must allow for the deliberate lower-granularity exception |
| tcb-001 | six proof rule checkers include their theory solvers **to reach `static` helpers parked on solver classes** | **true of the strings edge, and asserted of five others without evidence.** cvc5 replied that the arithmetic checker uses nothing from `linear/constraint.h` and the datatypes checker nothing from `theory/rewriter.h`; both were dead includes, deleted in a line each, and the helper extraction the finding proposed for them was work nobody needed to do. The measurement could not have supported the claim: `cuts` weighed an include edge by how much closure it carried and never asked whether the file used what it included, so a dead include and a load-bearing one came out identical and the prose supplied a mechanism for both. `Closure.edge_use` now classifies every edge `used`, `unused` or `unknown` — `unknown` is never collapsed into `unused`, since calling a live include dead is the same error reflected — and `tests/test_tcb.py` pins the three edges cvc5 named. The closure figures were right throughout and are unchanged |
| every published number | measured against cvc5 `16c4001e53`, quoted as though anyone could check it | **that commit is not on `cvc5/cvc5`.** It is on the `ajreynol/CVC4` fork, so no reader could fetch it, and the promise that *every claim is re-checkable without us* was void for the whole document set. The baselines happened to be valid — all eight ratchets are clean at upstream `40a4bb7e4` — so nothing measured was wrong, but nothing was checkable either. Now pinned in [`scripts/cvc5.lock`](../scripts/cvc5.lock), enforced by `tests/test_pin.py`, and fetched in CI by a job that fails if the pin is fork-only |
| `infer`/`inferid` baselines | our baselines named `SETS_RELS_TCLOSURE_DOWN` as an `InferenceId` cvc5 emits | **no such id has ever existed in cvc5.** `git log --all -S` finds it in no commit; the enum at `40a4bb7e4` carries `SETS_RELS_TCLOSURE_FWD` and `_UP`. The baselines had been written rather than generated by running the tools, so two of the eight ratchets failed against the very commit they were recorded at. Both are regenerated and all eight are clean; found while writing why cvc5 should care (`docs/README.md`) |
| `dokimasia.infer baseline --check` | an id leaving the unhandled set was reported as *now reconstructed* | it leaves for two unrelated reasons — the theory now proves it, or it is no longer emitted. The tool could not distinguish them, so a rename in cvc5 would have been reported as an improvement in cvc5's proof coverage. The delta now marks the second case `?` and says *no longer emitted, NOT reconstructed* |
| tcb-001 (draft) | the checker's TCB is **74% of `src/`** | an artifact of a mode that followed each header to its `.cpp`; the closure saturates at cvc5's whole link unit, and an unrelated seed (`printer/printer.cpp`) gave the identical figure. The compile-time surface is **8.0%**. The mode is no longer the default and warns; `tests/test_tcb.py` guards the result |

## How this page is maintained

**Who writes it.** [`prompts/close_bug_db`](../prompts/close_bug_db), which
reads a window of cvc5 history against the revision the observations were taken
at and leaves this file and [`bug_db/bugs.json`](../bug_db/bugs.json) changed and
uncommitted. A maintainer reads the diff. No entry is written by hand, and none
is written for a closure the database does not carry.

**The template.** One section per defect, newest first, whatever number of
database rows it touched — the unit is the thing that happened, not the row.

```text

### <date> — <the defect, in one line, in cvc5's terms>

| | |
| --- | --- |
| **Status** | closed by cvc5 #<pr> — <sha> · filed · acted on · no defect · retracted |
| **Identity** | <dokimasia:… (CODE)>, or the finding id, or — |
| **Found by** | the command or check code that produced it |
| **In cvc5** | the files a reader would open |
| **Attribution** | cites us · independent · cannot tell — and what that rests on |

**Summary:** what was actually wrong, for somebody who works on neither
project: no identities, no check codes, no procedure. **Two sentences, 250
characters at most.**

**What was wrong:** the mechanism in cvc5, at the level of the code somebody
would have had to read.

**What cvc5 did:** long enough to be checkable against the diff. Omit where
nothing has happened yet.

**Learned:** what this says about the check that produced it — whether it was
pointing where we thought, what it over- or under-claimed, and what would have
made the row easier for cvc5 to act on.
```

**`Learned` is the field that makes this a post-mortem rather than a
changelog**, and it is the one a thin run drops first. A section without it
records that something happened and nothing about what to do differently.

**Attribution is secondary, and recorded anyway.** Whether cvc5 made the change
because we reported it or found it themselves, the observation is closed either
way and the check was pointing at something real either way. Only the first is
also evidence that the *reporting* works. So the field says which, in one line,
and nothing here argues for credit.

**What a closure rests on.** A closure is a decision about a **cvc5 change**,
never about a row going quiet: absence closes nothing, and the claim has to be
re-read in cvc5's current source rather than taken from a commit message. The
rules are in the launcher and are checked by `tests/test_experience.py`.

**Where the rest lives.** What counts as a finding, the promises we publish
under and the bar a claim clears before anybody carries it are the analyzer's
design philosophy, in `dokimasia/README.md`. The
register of open hypotheses and everything we are asking cvc5 to act on is in
`docs/README.md`.
