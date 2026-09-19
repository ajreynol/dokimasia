# ydoki — which theories should cvc5 make proof-supported in safe mode?

**A research project of dokimasia, and not part of what it ships.** It reads
whatever it likes and writes nothing outside `tools/ydoki/`. Nothing here is
dokimasia's position, nothing here is cvc5's, and nothing here has been carried
to anybody.

**A named exception: on the advertising rule it is not an island.** The parent's
front page and documentation index both name it, which a child is only supposed
to be once it has stopped being research, so the exception is written down here
rather than left to drift.

- **What it delivered.** The split of the question into two axes that cannot be
  ranked against each other, and a measured starting position on each: four
  theory candidates accounting for 80 of the 125 term kinds safe mode blocks,
  in four different states rather than one; and on the option axis the five
  `SAFE`-only options, derived from the guard rather than chosen.
- **What stopped being true.** Only the advertising. In every other respect it
  is still an island: nothing outside `tools/ydoki/` imports it, no test or CI
  job runs it, and deleting the directory changes nothing about what the
  analyzer does or what CI says.
- **The promotion decision is open**, and it is the maintainer's. The three
  endings are unchanged and are at the foot of this charter; being findable is
  not one of them.

## The question, on two axes

**Of what `--safe-mode=safe` switches off, which is worth making
proof-supported, and in what order?**

Safe mode is cvc5's promise that what it solves, it can prove. It keeps that
promise by refusing work, and it refuses two different kinds:

| axis | what is refused | promoting one means |
| --- | --- | --- |
| **theories** | term kinds, so the input language shrinks — 125 of 341 | cvc5 accepts a formula it currently rejects outright |
| **options** | techniques, on inputs it already accepts — 24 option changes | cvc5 solves a formula it accepts but may now fail or time out on |

**They are mirror images and not one list.** The theory axis is about what you
may *say* to cvc5; the option axis is about what cvc5 may *do* with what you
said. The same question is asked of both, and **the two cannot be ranked against
each other on one scale**, because their falsifiers are opposite: a theory
promotion is worth nothing if nobody writes those terms, while an option
promotion is worth nothing unless the technique was load-bearing on inputs safe
mode *already* accepts. This project ranks within an axis and does not pretend
to rank across them.

**There is a second mirror, and it is the sharper one.** The theory candidates
are lost in safe **and** stable mode, so the theory axis measures what the
restricted modes cost against unrestricted. The priority options are lost in
safe **only** — stable keeps every one of them — so the option axis measures
what safe costs against stable, a distinction cvc5 already thought worth
building two modes for.

**Which of any of it is worth buying back is a question about where effort
should go, and no check settles it.**

### Why this is a child project rather than a page in the parent

dokimasia measures and declines to recommend. Its standing decision is that a
design question is answered with an invariant, a verifier and a test showing the
verifier fire — *not an opinion and not a reading* — and it never opens an issue
or a pull request. A ranking across theories is the other thing: a judgement
about where somebody else should spend their effort, unfalsifiable by any run.

Folded into the parent's own pages it would be read as the analyzer's position
on cvc5's roadmap, which is exactly the credibility the analyzer has because it
does not take positions. **The parent is well placed to ask this and badly
placed to answer it**, which is what this directory is for.

**It is advertised, and that is a decision about reach rather than about
standing.** The maintainer judged the question important enough to be findable
from the front page; being named there makes none of this dokimasia's position,
and the first three sentences of this charter are the ones that travel with the
link. A reader who arrives from the parent is reading a ranking nobody has
carried anywhere, built on the parent's measurements and on judgements the
parent declines to make.

## Goals, in order

1. **Say what is actually missing per candidate, split by layer.** On the theory
   axis a proof crosses three: the C++ that produces a rule, the checker that
   checks it, and the Eunoia signature that declares it so ethos can read it.
   The option axis asks the same three of a technique rather than of a theory.
   The candidates differ most in *which* layer is empty, and the parent measures
   all three.
2. **Give each candidate a cost shape rather than a cost.** *Nothing exists at
   any layer* and *everything exists but one skolem* are different kinds of
   work, and that distinction is available from the source without a build.
3. **Say what each refusal costs a user, in the terms its own axis makes
   available.** For a theory that is blocked term kinds; for an option it is the
   gap between safe and stable, which is the one comparison cvc5 has already
   made for us.
4. **Produce a ranked argument a cvc5 maintainer can disagree with**, one per
   axis, where the disagreement lands on a named claim rather than on the
   ranking.

**Wishue** — the outcome we would take if it went unusually well, and are not
committing to: a ranking cvc5 finds worth arguing with when choosing what to
make proof-supported next, on either axis. The honest form of that success is
being told which claim is wrong.

## What this project will not do

- **No implementation.** Not in cvc5, not here. This project writes prose.
- **No effort estimate in time or people.** We can say what is missing; we
  cannot say what it costs somebody who knows the code, and a number invented
  here would be quoted.
- **No claim about what cvc5 will do**, or about whether proof support for any
  of this is worth doing *at all*. The question is ordering among candidates,
  given that somebody has already decided to spend the effort.
- **No new checks in the parent.** Where an argument needs a measurement the
  parent does not have, that is a request recorded in
  [`docs/ledger.md`](docs/ledger.md) for a person to weigh — not a change this
  project makes.
- **No performance argument.** Proof-production overhead is outside dokimasia's
  scope and therefore outside this one's. **This bites hardest on the option
  axis**, where the case for promoting a technique is partly that losing it
  costs solving time — so the strongest argument available for a row there is
  one this project may not make, and a ranking that quietly made it anyway is
  the failure to watch for.
- **No ranking across the two axes.** They are mirror images with opposite
  falsifiers, and one ordered list over both would be a number invented to look
  decisive.
- **No re-deriving the complement.** An option that declares no proof support
  and that safe mode leaves *on* is the opposite defect, and it is already the
  parent's `i-2` and its settled `s-4`.
- **No proposal about Eunoia or CPC.** That a theory has no signature is a fact
  recorded here; what the calculus should cover is not ours, and a suggestion
  addressed to it is not a thing this directory produces.
- **Nothing carried anywhere by machine.** No issue, no pull request, no
  comment, no topic in the parent's discussion file. Candidate feedback
  accumulates in the ledger and a person decides whether any of it travels.

## The candidates on the theory axis

Four, given as the starting set rather than derived here: **finite fields**,
**floating point**, **theory of bags**, and **higher-order**. Together they
account for **80 of the 125 term kinds** safe mode blocks.

They are not four instances of one problem, and
[`docs/theories.md`](docs/theories.md) is the parent's measurements behind that
claim, at cvc5 `40a4bb7e4`:

| candidate | kinds blocked | proof rules | checker | signature | refused skolems |
| --- | --- | --- | --- | --- | --- |
| floating point | 48, whole-theory sweep | **0** | — | none | 1 |
| bags | 25, whole-theory sweep | **0** | — | none | 8 |
| finite fields | 6, whole-theory sweep | 11 declared, **0 produced** | none registered | none | 0 |
| higher-order | 1, by the logic axis | 2, **both produced** | both registered | `Uf.eo` declares them | 1 |

**The rows are in opposite states and that is the finding to start from.**
Floating point and bags have no proof vocabulary at all. Finite fields has
eleven declared rules that nothing produces, nothing checks and the seam cannot
print — a vocabulary written and never wired. Higher-order already works at
every layer the parent can see, and is kept out by an option default and one
skolem the seam refuses.

**That is a starting position, not a conclusion.** Each row is a static
reading, none of it establishes that any input reaches these paths, and *how
much is missing* is not the same question as *what it would take*.

## The candidates on the option axis

Not given but derived, because here the guard does the deriving:
[`docs/options.md`](docs/options.md) has the measurements and the tiers.

**The priority set is the five options `setDefaultsPre` clears in its
`SAFE`-only block** — `nlCov`, `ufSymmetryBreaker`, `cegqiBv`,
`varEntEqElimQuant` and the `bvSolver` choice. Each is `category = "regular"`,
each declares `no_support = ["proofs"]` in its own `.toml`, four of the five are
on by default, and **stable mode keeps every one of them**. cvc5's comment on
the block is the reason they rank first: *"disable features that have no proof
support but are considered regular."* Regular and on by default means an
ordinary user has the technique without asking for it, and loses it by asking
for the guarantee.

**Below that sit the ten expert extensions both restricted modes clear**, of
which `bags`, `ff`, `fp` and `ufHoExp` are the theory candidates seen from this
side — the option is *how* the theory is switched off, so for those four the two
axes name one act. The remaining six are theory-axis candidates nobody has
proposed yet, and listing them is not proposing them.

**Two groups are excluded rather than ranked low**, and saying so is most of
what keeps this axis honest. `arraysExp`, `setsExp` and `fpExp` are cleared but
already off by default, so nothing is lost. `checkProofsComplete`, `proofMode`
and the `cegqi*`/`dtSharedSelectors` rows are safe mode turning proofs on and
configuring them, not refusing a capability.

**And the biggest gap on this axis is one we cannot close from the source.**
Nothing here says any of the five is load-bearing — `nlCov` matters only on
inputs where coverings beat the alternative, and that needs a build and a
corpus. It is booked in [`docs/ledger.md`](docs/ledger.md) as a question for the
parent rather than answered here.

## It builds on the parent, and here is where

Every figure above is something dokimasia already measures, and this project
adds no instrument:

- **`dokimasia.fragment`** — the term kinds per theory and how each is blocked.
- **`dokimasia.modes`** — the whole option axis: which options each mode
  changes, the guard each change sits under, and the line it happens at. The
  safe and stable deltas differing by exactly the `SAFE`-only block is what
  makes the priority set a set rather than an opinion.
- **`dokimasia.ledger`** — one row per `ProofRule`: produced, checked,
  elaborated, printed. The finite-field rows are the reason that theory is not
  grouped with the other two.
- **`dokimasia.signature`** — the skolems the solver constructs and the seam
  refuses, and which rules the signature declares.

**The parent's registers remain the authority.** `docs/checks.md`,
`docs/issues.md` and `TODO.md` govern what has been measured and what is being
asked of cvc5. Where this project disagrees with them, they win and the
disagreement is the interesting part; a version of this project that never
disagreed would be a paraphrase.

## How it ends

Three endings, and a person picks: it **graduates** into its own repository, it
is **folded** into the parent — most likely as a section of `docs/issues.md` if
the ranking turns into something we would ask cvc5 for — or it is **retired in
place** with a line saying what was learned. Going quiet is not one of them.

## Is there a paper in it?

**No.** A prioritisation argument over four theories in one solver is useful to
the people who maintain that solver and to nobody else. If the *method* for
splitting a theory's proof debt by layer turns out to generalise, that is the
parent's paper question and not this project's.

## The name

**It is not a Greek word and it does not describe the work.** It is formed from
**δοκιμασία** (*dokimasia*), the parent's name, the way **ynoia** is formed from
**εὔνοια** (*eunoia*) — the ecosystem's existing habit for naming a project
derived from another. The etymology stops there, and there is nothing further to
disagree with.

The shared policy asks a child for a Greek name that describes its work, and
this is neither. **That is a named exception rather than an oversight**, taken
by the maintainer for continuity with the ecosystem's other derived names;
writing a strained Greek etymology to satisfy the rule would have been the worse
answer, since the rule's own reason for existing is that a strained explanation
means the scope has not been decided. The scope is decided and it is above.
