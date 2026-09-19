# The theory axis: what safe mode stops you saying

The candidates on this axis, with the command that produced each figure, read at
cvc5 `40a4bb7e4` — the revision `scripts/cvc5.lock` pins, so anybody can fetch
it and re-run the right-hand column. Its mirror is `options.md`,
and `../README.md` says why the two are separate questions.

**This project adds no instrument.** Where a row needed a measurement dokimasia
does not take, it is in `ledger.md` as a question rather than
reported here as a number.

## The four candidates, layer by layer

A proof of a step crosses three layers, and a theory can be empty at any of
them: the **C++** that constructs the rule, the **checker** registered for it,
and the **Eunoia signature** that declares it so ethos can read the proof. The
parent measures all three separately, which is why the table has three columns
where a single "is it supported" would have had one.

| candidate | safe mode clears it at | kinds available / blocked | how blocked |
| --- | --- | --- | --- |
| floating point | `fp.fp`, `set_defaults.cpp:142` | 0 / 48 | whole-theory sweep |
| bags | `bags.bags`, `set_defaults.cpp:140` | 0 / 25 | whole-theory sweep |
| finite fields | `ff.ff`, `set_defaults.cpp:141` | 0 / 6 | whole-theory sweep |
| higher-order | `uf.ufHoExp`, `set_defaults.cpp:144` | 9 / 1 | logic |

> `python3 -m dokimasia.fragment theories <cvc5>` · `python3 -m dokimasia.modes delta <cvc5>`

The four block **80 of the 125 kinds** safe mode blocks, over 341 kinds in
fourteen theories. The remaining 45 are spread across arith (19), sets (15),
arrays (2), datatypes (3) and sep (6), none of which is a whole theory except
sep.

| candidate | proof rules | produced | checker registered | in the signature | skolems the seam refuses |
| --- | --- | --- | --- | --- | --- |
| floating point | 0 | — | — | no file | 1 — `FP_TO_REAL` |
| bags | 0 | — | — | no file | 8 — `BAGS_*` |
| finite fields | 11 | **0 of 11** | **none of 11** | no file | 0 |
| higher-order | 2 | 2 of 2 | 2 of 2 | `Uf.eo` | 1 — `HO_DEQ_DIFF` |

> `python3 -m dokimasia.ledger table <cvc5>` · `python3 -m dokimasia.signature skolems <cvc5>` · the signature files are `proofs/eo/cpc/rules/` and `proofs/eo/cpc/expert/rules/`

## What each row says, and what it does not

**Floating point and bags have no proof vocabulary.** No `ProofRule` names
either theory among the 170 declared, and neither has a signature file. The
blocked-kind counts are the whole of what safe mode is refusing, and they are
the two extremes of that count: 48 and 25.

**Finite fields is the odd one.** Eleven rules — ten `FF_*` and
`MACRO_FF_POLY_COMBINATION` — are declared in `cvc5_proof_rule.h` and every one
of them is produced by nothing, checked by nothing, expanded by nothing, and
refused by the seam. The parent's ledger reports them under `RULE0001` (no
registered checker), `RULE0003` (declared and nothing produces it) and
`ELAB0001` (a macro nothing expands) simultaneously. **A vocabulary was written
and never wired**, and *why* is the first thing this project should find out,
because the answer changes the cost estimate more than any other fact here.

**Higher-order already works at every layer the parent can see.**
`HO_APP_ENCODE` and `HO_CONG` are produced, have registered checkers, are
elaborated by nothing because they need no expansion, and are **always
printable**. `Uf.eo` declares `ho_cong`. What keeps higher-order out of safe
mode is therefore not missing proof machinery: it is `ufHoExp` being cleared,
`HO_APPLY` being unavailable through the logic rather than through a kind deny
list, and one skolem — `HO_DEQ_DIFF` — that the solver constructs and the seam
cannot print.

cvc5's own `illegal_checker.cpp` carries a comment worth reading beside that
last point: *"we don't guard against HO_APPLY, since it can naturally be handled
in proofs."* **That is cvc5 saying the kind is not the obstacle**, and it is the
strongest single piece of evidence in this file for where the cheapest candidate
is. It is also somebody's comment rather than a measurement, and it is quoted
here as the former.

## What none of this establishes

- **Not reachability.** Every figure above is static. A refused skolem is a
  refusal, not a proof that an input reaches it, and the parent's own latent
  census exists because the distinction keeps mattering.
- **Not cost.** *Eleven rules exist and nothing produces them* is not *eleven
  rules' worth of work remaining*, in either direction: they may be a stub
  somebody abandoned, or most of a design already thought through.
- **Not demand.** Nothing here says anybody wants any of these four in safe
  mode. The starting set was given rather than derived, and a candidate nobody
  needs ranks last whatever its cost shape.
- **Not the signature's position.** That a theory has no `.eo` file is a fact
  about `proofs/eo/`, not an argument that it should have one.
