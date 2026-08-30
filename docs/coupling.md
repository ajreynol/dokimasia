# Coupling to cvc5

Two lists, in the two directions.

**What we would like cvc5 to change**, because it would make this analysis
sharper or cheaper. These are asks, and the reasoning is attached to each.

**What we parse, and what would break us.** Recorded so a break is diagnosable,
not so anyone holds still.

> **This repository imposes no constraints on refactoring cvc5.** dokimasia is
> downstream. If cvc5 changes and a tool here breaks, that is our bug to fix —
> exactly like a false positive. Nothing below is a request that cvc5 keep a
> name, a file or a switch. The point of writing it down is that when a tool
> does break, we already know why.

## What we would like cvc5 to change

Ordered by leverage, not by effort.

### R1 — emit the tables cvc5 already has

**The single highest-leverage change.** A build target that dumps the proof
registries as JSON: `ProofRule` with its checker and pedantic level, `TrustId`,
`InferenceId`, `ProofRewriteRule` with its RARE origin, and what the Eunoia
seam accepts.

Today we recover all of that by parsing C++ — enum blocks, `switch` bodies,
`registerChecker` calls. That works, and it is exactly as brittle as it sounds:
**three parser bugs in one afternoon of building these tools**, two of which
produced confidently wrong numbers before a cross-check caught them. A dumped
table would make the whole tier-0 analysis exact instead of inferred.

It is also useful to cvc5 independently of us: the same JSON documents the
calculus, feeds the signature, and lets cvc5 assert its own invariants at build
time. R1 makes several of the asks below unnecessary rather than merely easier.

### R2 — name the completeness guarantee

`--check-proofs-complete` appears nowhere in `.github/` or `test/`. In a safe
build, `setDefaultsPre` enables it as a side effect of `--check-proofs`, so
completeness is tested through a four-link chain nothing asserts. Passing the
flag explicitly in the `proof` tester costs one line and makes the guarantee
visible. See [`CI0002`](../TODO.md#stage-a2--is-cvc5s-proof-ci-intact).

### R3 — get the theory solvers out of the proof checker's includes

Six rule checkers `#include` the headers of the solvers they check, to reach
`static` helpers parked on solver classes. Extracting those helpers into
dependency-light headers shrinks the checker's compile-time surface and breaks
the coupling. Written up as [`tcb-001`](findings/tcb-001.md).

### R4 — one InferenceId, one place

51 ids are produced at more than one site, 14 are produced nowhere, and 21
inferences are emitted with a sentinel id. Until an id names one program point,
"the inferences theory X can make" is not an enumerable set, and the `INFER`
coverage analysis cannot be precise. [`docs/hygiene.md`](hygiene.md#h1--one-id-one-place).

### R5 — make `no_support` cover defaults

Option definitions carry a machine-readable `no_support = ["proofs"]`, and
`SolverEngine` throws if a user *sets* such an option in safe mode. It never
fires for an option already on by default, which is how `stringLazyPreproc`
reaches a safe-mode run. Either the guard should consider defaults, or safe
mode's disable list should be derived from the annotation rather than
maintained beside it.

### R6 — declare what the seam is *supposed* to reject

`EoPrinter::isHandled` refuses 40 rules; 14 are refused **by design** (macros
that get elaborated away, trust steps, other formats' rules). We infer that
distinction from the rule's name and whether the post-processor expands it,
which is a heuristic that already needed one correction (`SUBS` is not named
`MACRO_*` but is elaborated). If cvc5 stated the intent, the analysis would
report gaps instead of guessing which refusals are gaps.

### R7 — make the pass↔TrustId correspondence derivable

Seven `PREPROCESS_*` ids are not derivable from their pass filename, including
`PREPROCESS_BV_GUASS` — a misspelling of Gauss. We work around it by matching
construction sites, which is more robust anyway, but a naming rule would make
the correspondence checkable directly and would catch a pass added without a
declared hole.

### R8 — safe mode as a build-time property

`ENABLE_SAFE_MODE` exists and prunes almost nothing of cvc5's own code: five
files in `src/` mention `CVC5_SAFE_MODE`, two only to reword an error message.
Moving features from "disabled at runtime" to "not compiled" turns a class of
proof hole into a link error. [`docs/kernel.md`](kernel.md#a-safe-build-that-cannot-be-unsafe).

## What we parse, and what would break us

Kept short on purpose. The mitigation is not an abstraction layer — it is that
**every tool has tests asserting facts we verified by hand against a pinned
checkout**, so a break shows up as a named test failure rather than a quietly
wrong number. That is the whole robustness budget, and it is enough.

| we read | tool | what breaks us |
| --- | --- | --- |
| `EVALUE(...)` enum blocks in `cvc5_proof_rule.h`, `cvc5_skolem_id.h` | ledger, rewrites | changing the macro, or splitting the enums across files |
| `enum class` bodies in `inference_id.h`, `trust_id.h` | inferid, trust | moving the enum, or generating it |
| `EoPrinter::isHandled`, `isHandledTheoryRewrite` switches | ledger, rewrites | renaming them, or replacing the switch with a table (**which would be an improvement** — see R1) |
| `registerChecker` / `registerTrustedChecker` call sites | ledger | registering in a loop over a list instead of call-by-call |
| `rewriteViaRule` switch bodies | rewrites | same |
| `SET_AND_NOTIFY*` macros in `set_defaults.cpp` | modes | renaming the macros, or moving the logic out of one file |
| `*.toml` option definitions | modes | switching option format |
| `.github/workflows/*.yml` matrix entries | ci | restructuring the matrix, or moving tester selection into a script |
| `run_regression.py` tester classes | ci | building tester args somewhere other than the class body |
| `preprocessing/passes/*` filenames | trust | reorganising the directory |
| `theory/*/rewrites` RARE files | rewrites | moving or renaming them |
| `#include` graph under `src/` | tcb | nothing much; it is the most robust thing here |

### Known limits, not breakages

Worth separating from the above, because these are things the tools *cannot*
do rather than things that might stop working:

- **Option gates are not computed.** Whether a rule or trust step is reachable
  under `--safe-mode=safe` usually depends on a guard far from the site — often
  a kind-legality check in `illegal_checker.cpp`, not a local `if`. Every
  severity claim that needs this is currently made by hand and labelled as such.
- **Generated headers are invisible.** `options/options.h` is built from the
  `.toml` files, so the TCB closure does not follow edges through it.
- **`rewriteViaRule` is one route.** A rewrite applied another way will look
  unimplemented to the `rewrites` tool.

## Parser bugs found while building these tools

Recorded because they are the argument for R1, and because two of them produced
wrong output that a cross-check caught rather than a test.

| bug | effect | caught by |
| --- | --- | --- |
| `//.*` under `re.DOTALL` | any switch arm whose body opened with a line comment was read as a fallthrough and its labels silently lost | a rule appearing in the seam that the tool called unhandled |
| next-label bound used `m.end()` instead of `m.start()` | fallthrough groups mis-grouped | the same investigation |
| anchoring on `bool EoPrinter::isHandled` | matched the call site, then `isHandledTheoryRewrite` is a prefix-match hazard for the other tool | zero results where 53 were expected |
| fixed-size window past a class declaration | `BaseTester` inherited `UnsatCoreTester`'s flags; the last tester swallowed the module's argparse | reading the output against the source |
| `exec`-mode include closure | saturated at cvc5's whole link unit, giving 74% for any seed | seeding from an unrelated file |
