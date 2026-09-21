# ydoki

An exploratory research project asking **which theories and options cvc5 should
make proof-supported in safe mode, and in what order**.

It uses Dokimasia's existing measurements to compare candidates and writes
prose only. Its proposals are neither Dokimasia's nor cvc5's position, and none
has been presented upstream.

## Two separate questions

Safe mode disables features that lack full proof support. Those restrictions
affect users in two ways:

| Axis | What safe mode restricts | What proof support could enable |
| --- | --- | --- |
| Theories | term kinds in the input language | accepting formulas the mode currently rejects |
| Options | solving techniques on accepted inputs | using techniques the mode currently disables |

Candidates are compared **within each axis**. The source can show which proof
components are missing; it cannot establish user demand, implementation effort
or the benefit of restoring a technique.

## Starting measurements

These measurements use cvc5 `40a4bb7e4`, the parent's reference revision.

The four theory candidates account for **80 of the 125 term kinds** safe mode
blocks. They are blocked in stable mode too.

| Candidate | Kinds blocked | Proof rules | Checker | Eunoia signature | Refused skolems |
| --- | --- | --- | --- | --- | --- |
| Floating point | 48 | 0 | none | none | 1 |
| Bags | 25 | 0 | none | none | 8 |
| Finite fields | 6 | 11 declared, 0 produced | none registered | none | 0 |
| Higher-order | 1 | 2, both produced | both registered | declared in `Uf.eo` | 1 |

This distinguishes missing proof infrastructure from infrastructure that exists
but remains restricted. It does not establish that an input reaches any of the
listed paths. Details and limitations are in `docs/theories.md`.

The option candidates start with the **five options disabled only in safe
mode**: `nlCov`, `ufSymmetryBreaker`, `cegqiBv`, `varEntEqElimQuant` and the
`bvSolver` choice. All declare no proof support; four are enabled by default,
and stable mode retains all five. `docs/options.md` explains this priority set,
the extensions both restricted modes disable, and the settings excluded from
the comparison. Whether any technique is essential on real inputs remains
unmeasured.

## Goals and limits

For each candidate, identify the missing components in proof production,
checking and Eunoia output; explain the restriction a user encounters; and
develop a prioritisation argument a cvc5 maintainer can assess.

The project has the following limits:

- It implements no code and estimates no schedule or staffing cost.
- It makes no performance claims or proposals about the Eunoia calculus.
- It adds no analyzer checks. Missing measurements become requests in
  `docs/ledger.md` for a person to review.
- It does not repeat the parent's investigation of options that lack proof
  support but remain enabled in safe mode (`i-2` and `s-4`).
- It writes only within `tools/ydoki/`. A person decides whether to take any
  feedback upstream; no program posts issues, pull requests or comments.

## Reading guide

Paths in this table are relative to `tools/ydoki/`.

| Read | For |
| --- | --- |
| `docs/theories.md` | the four theory candidates and the evidence by proof layer |
| `docs/options.md` | option candidates, tiers and limitations |
| `docs/ledger.md` | candidate feedback and requests for missing measurements |

All measurements come from the parent's `fragment`, `modes`, `ledger` and
`signature` modules. The parent's `docs/README.md` and `TODO.md` remain the
authority for its findings and plans. This project has no tests or CI jobs of
its own, and the analyzer does not depend on it.

## Project status

The maintainer has left the promotion decision open. The project may graduate
into its own repository, be folded into Dokimasia, or be retired with a record
of what was learned. The current comparison is not a paper claim; any broader
method would need separate evidence.

Two policy exceptions are explicit. The project is **not an island** for
advertising: the parent names it while it is still research. The name **ydoki**
follows the ecosystem's derived names rather than being a descriptive Greek
word. Neither exception changes its research status or scope.
