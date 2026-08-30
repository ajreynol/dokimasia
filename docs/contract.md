# The contract

What cvc5 promises about proofs, where it promises it, and the three ways
the promise can break. Background for [the analyses](../README.md#the-analyses).

## The gap this exists to close

cvc5 already asks our question — at runtime, one benchmark at a time.
`--check-proofs-complete` walks the finished proof and fails the run if any node
is one `proof::EoPrinter::isHandled` rejects
([`src/smt/proof_final_callback.cpp:177`](https://github.com/cvc5/cvc5/blob/main/src/smt/proof_final_callback.cpp)):

```
The proof was incomplete due to a trust step with id THEORY_LEMMA, from theory THEORY_STRINGS
```

That is the right check. It has one property that no amount of CI fixes: **it
fires only on an input that reaches the step.** A theory can carry an inference
with no proof for years and no benchmark in the suite will name it. The check is
a sampler over a space nobody has measured.

dokimasia reads the same pipeline the other way. `--check-proofs-complete` takes
the proof a run produced and asks whether it is complete. dokimasia takes the
*code* and asks **which proofs it could ever produce**, and whether any of them
is not — with no benchmark in hand.

The relationship is the one `anoieu` has to `ethos`, and dokimasia is modelled
on [`anoieu`](https://github.com/ajreynol/anoieu) deliberately: same staging,
same check-with-a-witness discipline, same promise that a false positive is our
bug. Where anoieu is the eager counterpart to a lazy *checker*, dokimasia is the
static counterpart to a *dynamic* completeness test.

## The contract

The target, stated as one line:

> **If cvc5 solves it, cvc5 will produce a proof of it.**

### cvc5 already promises this, in one configuration

That sentence is not our invention. `--safe-mode=safe` is defined in
[`base_options.toml`](https://github.com/cvc5/cvc5/blob/main/src/options/base_options.toml)
as:

> *"Do not allow using expert options or theories, more than one regular option,
> or any feature that does not have **full proof and model support**."*

and its sibling `--safe-mode=stable` is defined as the one that *"**may allow
incomplete proofs** or models."*

So cvc5 draws the line itself, and **safe mode is the side of it that carries
the contract**. `SetDefaults::setDefaultsPre` implements the promise by
disabling, by name, the features that would break it — `nlCov`,
`ufSymmetryBreaker` ("never use symmetry breaker, which does not have proofs"),
`cegqiBv` ("proofs not yet supported"), `varEntEqElimQuant` ("a class of
rewrites in quantifiers we don't have proof support for"), the experimental
theories, and `bvSolver → BITBLAST_INTERNAL`. It upgrades `proofMode` to
`FULL_STRICT`, and turns on `checkProofsComplete` when proofs are checked.

**That list is hand-maintained.** Which gives dokimasia its sharpest question,
and its first priority:

> Is there anything reachable in safe mode with no proof support that nobody
> remembered to put on the list?

An input for which

```bash
cvc5 --safe-mode=safe --produce-proofs --check-proofs benchmark.smt2
```

reports `The proof was incomplete` is not a gap or a wish. It is **cvc5 failing
a promise it makes in its own documentation** — and it is the bug report this
project exists to produce.

Stable and unrestricted are worth analyzing too, and most of the checks below
apply unchanged. But findings there are *roadmap items*: those modes never
promised complete proofs, so a hole in them is a gap to prioritize, not a
contract to enforce. The ranking is in
[`docs/tooling.md`](tooling.md#d5--safe-mode-first-and-the-reproducer-is-the-deliverable).

### The three ways it breaks

Three things have to hold for that to be true, and each is a different kind of
analysis. Keeping them apart is most of the design.

| | the claim | what breaks it |
| --- | --- | --- |
| **1. Coverage** | every inference the solver can make has a proof step | a theory lemma sent with no `ProofGenerator`; an `InferenceId` its theory's `InferProofCons` has no case for |
| **2. Admissibility** | every step it emits survives to a checkable proof | a `ProofRule` `EoPrinter::isHandled` rejects; a `MACRO_*` nothing elaborates; a rewrite reconstruction that runs out of budget |
| **3. Agreement** | the solver that produces the proof is the solver that solved it | `incompatibleWithProofs` silently turning a technique off, so the proof-producing run is a different run |

### Why (3) is not a footnote

**Proofs are off by default.** Solving without proofs is what users do, because
proofs are slow. So `produce-proofs` does not merely *observe* the solver — it
*changes* it, and cvc5 says so out loud in
[`SetDefaults::incompatibleWithProofs`](https://github.com/cvc5/cvc5/blob/main/src/smt/set_defaults.cpp):

- **refused outright** — `fresh-binders`, `global-negate`, deep restarts, lemma
  inprocessing, and sygus under full proofs; the run throws
  `FatalOptionException`;
- **changed underneath the user** — `bvAssertInput → false`,
  `bvSolver → BITBLAST_INTERNAL`, `nlCovVarElim → false`, and under
  `FULL_STRICT` also `ufSymmetryBreaker → false`, `cegqiMidpoint → true`,
  `cegqiUseInfInt/Real → false`, `dtSharedSelectors → false`.

Every line in the second group is a place where **the run that produced the
proof is not the run that solved the problem**. That is fine when it is
deliberate and written down. It is not fine that the list is hand-maintained: a
technique added without a line here produces proofs nobody has reasoned about,
and a technique added *with* a line here quietly makes the prover weaker than
the solver, with no record of how much.

So dokimasia analyzes **both configurations and the difference between them**.
A contract about a solver users do not run is not the contract.

## What we look at, and what we do not

**We analyze the C++ of cvc5.** The proof infrastructure in `src/proof`, the
proof reconstruction in `src/theory/*/infer_proof_cons.cpp` and
`src/rewriter`, the post-processing in `src/smt`, the option logic in
`src/smt/set_defaults.cpp`, and the rule/id enumerations that tie them together.

**We do not analyze Eunoia signatures.** `Cpc.eo` and its semantics are
`anoieu`'s subject and it is better at them. Where a question genuinely spans
the boundary — *does this `ProofRule` have a Eunoia rule to land on* — the C++
half is ours and the signature half is a reference we consult, never a file we
diagnose. Findings that belong to the signature get handed to anoieu.

The seam itself is C++ and is very much ours:
[`src/proof/eo/`](https://github.com/cvc5/cvc5/tree/main/src/proof/eo) is where
a cvc5 proof becomes a Eunoia proof, and "is the Eunoia pipeline healthy" is,
on this side of the line, a question about `eo_printer.cpp` and
`eo_node_converter.cpp`.

