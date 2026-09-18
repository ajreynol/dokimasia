# ydoki — which theories should cvc5 make proof-supported in safe mode?

**A research project of dokimasia, and not part of what it ships.** It reads
whatever it likes and writes nothing outside `tools/ydoki/`. Nothing here is
dokimasia's position, nothing here is cvc5's, and nothing here has been carried
to anybody.

**Footing:** `unadvertised-child` — the parent's front page does not name it, because a prioritisation argument is speculative work that should not borrow the analyzer's credibility.

## The question

**Of the theories that `--safe-mode=safe` switches off, which are worth making
proof-supported, and in what order?**

Safe mode is cvc5's promise that what it solves, it can prove. It keeps that
promise partly by refusing work: fourteen theories, and 125 of 341 term kinds,
are unavailable inside it. Every one of those refusals is a capability traded
for the guarantee. **Which of them are worth buying back is a question about
where effort should go, and no check settles it.**

### Why this is a child project rather than a page in the parent

dokimasia measures and declines to recommend. Its standing decision is that a
design question is answered with an invariant, a verifier and a test showing the
verifier fire — *not an opinion and not a reading* — and it never opens an issue
or a pull request. A ranking across theories is the other thing: a judgement
about where somebody else should spend their effort, unfalsifiable by any run.

Published in the parent's own tree it would be read as the analyzer's position
on cvc5's roadmap, which is exactly the credibility the analyzer has because it
does not take positions. **The parent is well placed to ask this and badly
placed to answer it**, which is what this directory is for.

## Goals, in order

1. **Say what is actually missing per theory, split by layer.** A proof crosses
   three: the C++ that produces a rule, the checker that checks it, and the
   Eunoia signature that declares it so ethos can read it. The parent measures
   all three, and the candidates differ most in *which* layer is empty.
2. **Give each candidate a cost shape rather than a cost.** *Nothing exists at
   any layer* and *everything exists but one skolem* are different kinds of
   work, and that distinction is available from the source without a build.
3. **Produce a ranked argument a cvc5 maintainer can disagree with**, where the
   disagreement lands on a named claim rather than on the ranking.

**Wishue** — the outcome we would take if it went unusually well, and are not
committing to: a ranking cvc5 finds worth arguing with when choosing the next
theory. The honest form of that success is being told which claim is wrong.

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
  scope and therefore outside this one's.
- **No proposal about Eunoia or CPC.** That a theory has no signature is a fact
  recorded here; what the calculus should cover is not ours, and a suggestion
  addressed to it is not a thing this directory produces.
- **Nothing carried anywhere by machine.** No issue, no pull request, no
  comment, no topic in the parent's discussion file. Candidate feedback
  accumulates in the ledger and a person decides whether any of it travels.

## The candidates

Four, given as the starting set rather than derived here: **finite fields**,
**floating point**, **theory of bags**, and **higher-order**. Together they
account for **80 of the 125 term kinds** safe mode blocks.

They are not four instances of one problem, and
[`docs/evidence.md`](docs/evidence.md) is the parent's measurements behind that
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

## It builds on the parent, and here is where

Every figure above is something dokimasia already measures, and this project
adds no instrument:

- **`dokimasia.fragment`** — the term kinds per theory and how each is blocked.
- **`dokimasia.modes`** — that `bags`, `ff`, `fp` and `ufHoExp` are cleared in
  `setDefaultsPre` under *safe options*, with the line each is cleared at.
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
