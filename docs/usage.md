# Individual analysis commands

These examples describe the measurements at cvc5 `40a4bb7e4`, the revision in
[`tools/cvc5.lock`](../tools/cvc5.lock). Run a command to measure another tree;
the comments are recorded examples, not assertions about current upstream.
For the collected observation workflow, see [the analyzer guide](analyzer.md).

## What exists today

No dependencies; Python 3.10+; reads a checkout, needs no build.

```bash
python3 -m dokimasia check  <cvc5>   # every ratchet, one process — 2.4s
python3 -m dokimasia report <cvc5>   # every analysis, printed
```

**[`dokimasia.buildmode`](../dokimasia/buildmode/)** — is a safe *build* still an
unrestricted build with one option default flipped? That invariant is what keeps
cvc5's deliberate refusal to combine safe mode with debug symbols nearly
costless; see [the case study](cases/safe-build-vs-safe-mode.md) for cvc5
[#12899](https://github.com/cvc5/cvc5/pull/12899).

```bash
python3 -m dokimasia.buildmode check <cvc5>       # 8 conditionals, all benign
python3 -m dokimasia.buildmode sites <cvc5>       # each one, classified
```

**[`dokimasia.latent`](../dokimasia/latent/)** — the subtraction the rest of the
repository exists to make: *static inventory − what a corpus reached = the holes
nothing has hit*.

```bash
python3 -m dokimasia.latent census <cvc5>          # 182 of 203 latent, 0 in safe mode
python3 -m dokimasia.latent list   <cvc5> --kind seam-rule
scripts/sweep_corpus --cvc5 <binary> --corpus <dir>  # regenerate the census
```

**[`dokimasia.tcb`](../dokimasia/tcb/)** — the trusted computing base of the
internal proof checker, the natural kernel candidate.

```bash
python3 -m dokimasia.tcb measure  <cvc5>   # 179 files, 41,446 lines, 8.0% of src/
python3 -m dokimasia.tcb cuts     <cvc5>   # what each dependency edge costs
python3 -m dokimasia.tcb why      <cvc5> theory/strings/core_solver.h
python3 -m dokimasia.tcb baseline <cvc5> --check    # ratchet, for CI
```

**[`dokimasia.modes`](../dokimasia/modes/)** — what safe and stable mode change
about the defaults, from all 172 option-setting sites in `set_defaults.cpp`.

```bash
python3 -m dokimasia.modes delta    <cvc5>          # safe mode: 24 option changes
python3 -m dokimasia.modes check    <cvc5>          # options that escape the promise
python3 -m dokimasia.modes baseline <cvc5> --check  # ratchet, for CI
```

**[`dokimasia.inferid`](../dokimasia/inferid/)** — whether each `InferenceId` names
a single program point.

```bash
python3 -m dokimasia.inferid check <cvc5>          # 51 ids produced at more than one site
python3 -m dokimasia.inferid show  <cvc5> STRINGS_CODE_PROXY
python3 -m dokimasia.inferid dead  <cvc5>          # 14 declared, produced nowhere
python3 -m dokimasia.inferid stats <cvc5>
```

**[`dokimasia.ledger`](../dokimasia/ledger/)** — one row per `ProofRule`, four
columns: produced, checked, elaborated, printed.

```bash
python3 -m dokimasia.ledger holes <cvc5>          # 14 rules the Eunoia seam cannot print
python3 -m dokimasia.ledger rule  <cvc5> ARITH_POW2_INIT
python3 -m dokimasia.ledger table <cvc5> --produced-only
```

**[`dokimasia.trust`](../dokimasia/trust/)** — the census of cvc5's declared holes:
every `TrustId`, where it is constructed, and the preprocessing correspondence.

```bash
python3 -m dokimasia.trust census <cvc5>          # 75 ids: 70 live, 4 dead
python3 -m dokimasia.trust passes <cvc5>          # which passes declare a hole
python3 -m dokimasia.trust show   <cvc5> THEORY_LEMMA
```

**[`dokimasia.ci`](../dokimasia/ci/)** — an independent check that cvc5's proof
testing is still attached. CI is the safety net today, and one that quietly
stops being attached looks exactly like one that works.

```bash
python3 -m dokimasia.ci proofs  <cvc5>            # the completeness chain
python3 -m dokimasia.ci matrix  <cvc5>            # job x tester
python3 -m dokimasia.ci testers <cvc5>            # what each tester passes
```

**[`dokimasia.rewrites`](../dokimasia/rewrites/)** — coverage of the 533-rule
rewrite vocabulary at the Eunoia seam.

```bash
python3 -m dokimasia.rewrites coverage <cvc5>     # RARE vs hand-written vs applied
python3 -m dokimasia.rewrites gaps     <cvc5>     # applied, and unprintable
```

**[`dokimasia.fragment`](../dokimasia/fragment/)** — the logical fragment cvc5
supports, per theory, and whether it is enforced. Generates
[`docs/fragment.md`](fragment.md).

```bash
python3 -m dokimasia.fragment theories <cvc5>     # 341 kinds over 14 theories
python3 -m dokimasia.fragment check    <cvc5>     # is the fragment enforced?
python3 -m dokimasia.fragment doc      <cvc5> --out docs/fragment.md
```

**[`dokimasia.infer`](../dokimasia/infer/)** — does every inference a theory makes
have a proof reconstruction? The completeness core.

```bash
python3 -m dokimasia.infer coverage  <cvc5>          # per theory
python3 -m dokimasia.infer unhandled <cvc5> strings  # the ids that fall through
```

**[`dokimasia.signature`](../dokimasia/signature/)** — does the Eunoia signature
agree with cvc5's own account of a rule?

```bash
python3 -m dokimasia.signature rules   <cvc5>     # 0 printable rules undeclared
python3 -m dokimasia.signature skolems <cvc5>     # 24 constructed but unprintable
python3 -m dokimasia.signature checker <cvc5>     # documented arity vs what the checker enforces
```

**[`dokimasia.gates`](../dokimasia/gates/)** — the machinery the other tools kept
needing: which option legalises each term kind, and so whether a rule can fire
under `--safe-mode=safe`.

```bash
python3 -m dokimasia.gates kinds    <cvc5>        # 59 kinds carry an option gate
python3 -m dokimasia.gates rule     <cvc5> LAMBDA_ELIM
python3 -m dokimasia.gates verdicts <cvc5>        # blocked / partial / open
```


The low-level commands keep their existing output and exit conventions.
A candidate needs the option gate and a reproducer before it becomes a
proof-completeness defect. See [the checks](checks.md) and [the register](issues.md).
