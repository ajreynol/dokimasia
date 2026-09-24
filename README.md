# Dokimasia

Dokimasia is a static analyzer for **cvc5's proof-production code**. It reads
the C++ that constructs, checks and prints proofs, looking for missing proof
support and inconsistencies in safe mode. It works on a source checkout;
**no cvc5 build is needed**.

A clean run means the selected checks found nothing. A reported gap is a
candidate for investigation: static analysis alone does not establish that an
input can reach it or that cvc5 produces an incomplete proof.

## Quick start

You need Python 3.10 or later and a cvc5 source checkout. There are no Python
dependencies. From this repository's root:

```bash
# Preview the source files and check for missing inputs.
scripts/dokimasia_analyzer --cvc5 /path/to/cvc5 --dry-run

# Run the checks and save observations and evidence in scratch/.
scripts/dokimasia_analyzer --cvc5 /path/to/cvc5 --no-update
```

The second command writes `scratch/new-bugs.json` and its evidence sidecar,
`scratch/new-bugs.json.run.json`. Any cvc5 revision can be analyzed; the revision
in [scripts/cvc5.lock](scripts/cvc5.lock) is the reference for regression tests
and published measurements.

To record a run in the repository's database, omit `--no-update`:

```bash
scripts/dokimasia_analyzer --cvc5 /path/to/cvc5
```

Recording uses [Koine](https://github.com/ajreynol/koine)'s shared database tools
and requires a clean Koine checkout at the revision in
[scripts/koine.lock](scripts/koine.lock). See **Local dependencies** in
`docs/maintenance.md` for setup. The analyzer never fetches or changes a
dependency checkout.

## What it checks

The default run includes eleven analyses. Repeat `--analysis NAME` to select a
subset, for example `--analysis ledger --analysis ci`.

| Analysis | Looks for |
| --- | --- |
| `ledger` | proof rules missing checkers or detected macro expansion, trusted registrations, and printer refusals |
| `ci` | gaps in cvc5's proof-testing configuration |
| `buildmode` | changes that may violate the safe-build invariant |
| `modes` | options without proof support that lack a direct safe-mode override |
| `rewrites` | implemented rewrites the printer refuses or restricts to unrestricted mode |
| `trust` | trust steps constructed without a reason identifier |
| `infer` | inferences missing reconstruction cases where the fallback is a trust step |
| `preprocess` | preprocessing skolem lemmas explicitly constructed without a proof generator |
| `proofshape` | literal proof-step premise and argument counts that disagree with checker entry assertions |
| `inferid` | inference identifiers shared across production sites or sentinel identifiers used in production |
| `signature` | missing declarations in the Eunoia proof format, refused auxiliary symbols (skolems), and disagreements about rule argument counts |

The check catalogue in `docs/README.md` describes each claim and its limits.
Optional developer reports and individual commands are in
`docs/maintenance.md`.

To see which regressions disable proof checking, run:

```bash
./scripts/eo_cvc5_regressions_audit
```

The [regression audit](regression_audit/README.md) lists `proof`, `cpc`, and
planned `cpc-logos` directives, inherited disables and
available reason comments. It uses the configured cvc5 checkout; `--cvc5`
selects another one. The default is a compact table with totals; `--verbose`
shows source evidence, and `--summary` prints just the totals and tester status.

To count the internal proof checker's trusted computing base (TCB), run:

```bash
./scripts/eo_cvc5_tcb_count
./scripts/eo_cvc5_tcb_count --cvc5 /path/to/cvc5 --json
```

The [TCB count](scripts/eo_cvc5_tcb_count) uses the configured cvc5 checkout and
reports file and line counts, the share of `src/`, and a subsystem breakdown.
`--json` prints the headline counts for scripting. It measures the transitive
`#include` closure: compile-time dependencies, not runtime reachability.
Generated headers are omitted; no cvc5 build is needed.

## Reading the results

**Browse the [recorded observations](bug_db/bugs.md)** for the accumulated
results, or the [supported fragment](bug_db/fragment.md) for proof support by
theory. These are generated views; recording commands refresh the observation
page and CI checks it against the JSON.

`bug_db/README.md` explains the records, archived evidence and review process.
The issue register in `docs/README.md` separates open candidates, settled claims
and filed findings. `docs/experience.md` records cvc5's responses and changes.
An observation disappearing from a later run does not establish that it was
fixed; closure requires evidence from cvc5's history.

For an independent assistant analysis or a closure assessment, see **An
independent second producer** and **Assessing closure** in
`docs/maintenance.md`.

## Documentation

Documentation paths below are relative to the repository root.

| Read | For |
| --- | --- |
| `docs/README.md` | scope, check catalogue, limitations and issue register |
| `docs/maintenance.md` | setup, commands, dependency pins and development checks |
| `dokimasia_analyzer/README.md` | module overview and standards for reviewing findings |
| `regression_audit/README.md` | regression exclusions, reason attribution and audit commands |
| `bug_db/README.md` | recording runs and interpreting the database |
| `docs/experience.md` | interactions with cvc5 and what they taught us |
| `TODO.md` | planned work and priorities |
| `tools/ydoki/README.md` | exploratory research on which theories and options to make proof-supported next |
| `docs/discussion.md` | correspondence with related projects |

## Scope

Dokimasia covers cvc5's proofs. Related projects cover
[Eunoia signatures](https://github.com/ajreynol/anoieu),
[general cvc5 development](https://github.com/ajreynol/paideia), and
[proof-production performance](https://github.com/ajreynol/tachyon/tree/main/tools/elaphros).
The research under `tools/ydoki/` uses Dokimasia's measurements; its proposals
are exploratory and have not been presented upstream.

## The name

The name **δοκιμασία** refers to the scrutiny an official-elect in classical
Athens underwent before taking office.

## How this repository is maintained

This repository is part of the **Eunoia ecosystem** and follows its
[repository policy](https://github.com/ajreynol/kanon/blob/main/docs/policy.md).
CI pins Anoieu's policy checker in `scripts/deps.lock`.

The repository is written by AI agents under human supervision. A human
maintainer reviews the work and decides what to report upstream. The review
standards are in `dokimasia_analyzer/README.md`.
