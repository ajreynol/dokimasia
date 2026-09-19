# The option axis: what safe mode stops cvc5 doing

The candidates on this axis, with the parent's measurements behind each, read at
cvc5 `40a4bb7e4`. Its mirror is [`theories.md`](theories.md), and
[`../README.md`](../README.md) says why the two are separate questions.

**This project adds no instrument.** Every figure is
`python3 -m dokimasia.modes delta <cvc5>`, its `--mode stable` form, or
`python3 -m dokimasia.modes check <cvc5>`.

## Where the candidates come from

`setDefaultsPre` opens with a block that runs whenever the mode is not
unrestricted, and cvc5's own comment says what it is for: *"all 'experimental'
theories that are enabled by default should be disabled here"*. **Nested inside
it** is a second block, guarded on the mode being `SAFE` specifically, whose
comment is the sentence this whole axis turns on:

> *"disable features that have no proof support but are considered regular."*

**The nesting is load-bearing and easy to read past**, because a row in the
inner block sits under both guards and looks like a shared one. It is the
difference between *safe mode costs you this* and *both restricted modes cost
you this*, and the two lead to different arguments.

Counted from the two deltas: **safe changes 24 options, stable changes 13, and
every stable change is also a safe one.** The eleven in the gap are this axis's
priority set plus the proof plumbing that configures the mode itself.

## Tier 1 — priority: the options only safe mode takes

**These five are the whole capability difference between `--safe-mode=safe` and
`--safe-mode=stable`.** Every one is `category = "regular"`, declares
`no_support = ["proofs"]` in its own `.toml`, and is cleared in the `SAFE`-only
block. Four of the five are on by default.

| option | flag | default | what it does | how safe takes it |
| --- | --- | --- | --- | --- |
| `nlCov` | `--nl-cov` | `true` | the cylindrical algebraic coverings solver for non-linear arithmetic | **refuses an explicit setting**, then clears |
| `ufSymmetryBreaker` | `--symmetry-breaker` | `true` | UF symmetry breaker (Deharbe et al., CADE 2011) | silently |
| `cegqiBv` | `--cegqi-bv` | `true` | word-level inversion for counterexample-guided instantiation over bit-vectors | silently |
| `varEntEqElimQuant` | `--var-ent-eq-elim-quant` | `true` | variable elimination for quantified formulas via entailed equalities | silently |
| `bvSolver` | `--bv-solver` | `BITBLAST` | choice of bit-vector solver | **substitutes** `BITBLAST_INTERNAL` |

**Why these are the priority, and it is cvc5's own framing rather than ours.**
`regular` means an ordinary user is offered it; `default = true` means they get
it without asking. So each row is a technique a user has today, loses by asking
for the proof guarantee, and **keeps if they ask for stable instead** — which
makes this list the price of safe over stable, on a distinction cvc5 thought
worth having two modes for.

**Two of the five are not like the other three.**

- **`nlCov` is the only option safe mode refuses rather than overrides.** The
  `SAFE` block guards it with `OPTION_EXCEPTION_IF_NOT` before clearing it, so
  `--safe-mode=safe --nl-cov` is an error while `--safe-mode=safe
  --symmetry-breaker` is silently ignored. Whether that asymmetry is deliberate
  is a question for cvc5 and not an argument for promotion; it is recorded here
  because the answer changes how loudly the other four fail.
- **`bvSolver` is a substitution, not a refusal.** Safe mode swaps one
  bit-vector solver for another that does produce proofs, so nothing is lost
  unless `BITBLAST` can do something `BITBLAST_INTERNAL` cannot. **It may not
  belong in a promotion ranking at all**, and establishing that is cheaper than
  ranking it.

## Tier 2 — the shared block, where this axis and the theory axis are one list

Ten options, all `expert`, all on by default, cleared in **both** restricted
modes: `sep`, `bags`, `ff`, `fp`, `ufHoExp`, `ufCardExp`, `datatypesExp`,
`arithExp`, `relsExp`, `setsCardExp`.

**Four of them are the theory candidates** — `bags`, `ff`, `fp` and `ufHoExp` —
and for those, promoting the theory and promoting the option are the same act:
the option is how the theory is switched off. The two axes are mirrored, not
disjoint, and this is where they touch.

**The other six are theory-axis candidates nobody has proposed yet**: `sep`, and
the expert extensions to arith, datatypes, sets, relations and UF cardinality.
Listing them is not proposing them. It is saying that the starting set of four
was given rather than derived, and here is what deriving it would have to
consider.

## Tier 3 — cleared, but nothing is lost

`arraysExp`, `setsExp` and `fpExp` are cleared by the shared block and are
already `default = false`. cvc5 says why in place: *"these are disabled by
default but are listed here in case they are enabled by default later."*

**These are not promotion candidates and should not be added as any.** Nobody
has them today, so nobody loses them; the rows are a guard against a future
default change, and reading them as a cost is the mistake this tier exists to
prevent.

## Not capability at all

`checkProofsComplete`, `proofMode`, `cegqiMidpoint`, `cegqiUseInfInt`,
`cegqiUseInfReal` and `dtSharedSelectors` are safe mode turning proofs on and
configuring them, not refusing anything a user wanted. **Out of this axis by
definition**, and named so that a later reading of the 24-row delta does not put
them back in.

## The complement, and it is the parent's

Two options declare `no_support = ["proofs"]` and safe mode leaves them **on**:
`stringLazyPreproc` and `macrosQuantMode`. That is the opposite defect — not
*should we promote this* but *why is this still here* — and it is already the
parent's `i-2` and its settled `s-4`. **Out of scope here**, named so nobody
re-derives it as a finding of this project.

## Other options worth promoting

For options outside the cleared set that are useful in practice — an expert
option worth making regular in a restricted mode, or a capability refused by a
route other than `setDefaultsPre`. **A row here needs a use, not just an
absence**, which is the whole difference between this table and the three tiers
above.

| option | why a user wants it in safe or stable | what refuses it today |
| --- | --- | --- |

## What none of this establishes

- **Not that any of these is load-bearing.** Every row is a default cvc5
  changes, not a measurement that anything got slower or went unsolved. `nlCov`
  matters only on inputs where coverings beat the alternative, and nothing here
  says how many those are. **This is the single biggest gap on this axis** and
  it is booked in [`ledger.md`](ledger.md).
- **Not the cost of proof support.** *Declares no proof support* is an
  annotation, not a measure of how far the technique is from having proofs.
- **Not that stable is the right comparison.** Tier 1 is the safe↔stable gap
  because that is what the guard makes measurable, not because a user choosing
  between them is the case that matters most.
