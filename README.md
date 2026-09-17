# dokimasia

A static analyzer for **cvc5’s proof-production code**: the C++ that constructs
proofs and the seam that prints them in Eunoia for ethos to check.

It looks for gaps in proof coverage, inconsistencies in the safe-mode contract,
and mismatches between proof production, checking and printing. It reads a
source checkout; it needs no cvc5 build. The analysis is partial: a clean run means the selected
checks found nothing, and a reported static gap still needs evidence of reachability.

Modelled on [anoieu](https://github.com/ajreynol/anoieu), whose subject is
Eunoia signatures. Dokimasia’s subject is the proof-production C++.

## Run the analyzer

Python 3.10 or later; no Python dependencies.

```bash
scripts/dokimasia_analyzer --cvc5 /path/to/cvc5 --dry-run
scripts/dokimasia_analyzer --cvc5 /path/to/cvc5 --no-update
scripts/dokimasia_analyzer --cvc5 /path/to/cvc5
```

The first command shows the source scope and missing inputs. The second runs
the nine analyses below and writes a dump with a matching evidence record.
The third also appends observations to [the database](docs/reports/bugs.json) through
[Koine](https://github.com/ajreynol/koine) and regenerates
[the readable table](docs/reports/static-analysis.md).

Database updates require a clean Koine checkout at `scripts/koine.lock`, found
through `$KOINE`, a sibling `koine` directory, or `deps/koine`. No checkout is
fetched or changed by the analyzer. Set `DOKIMASIA_CVC5` or add a cvc5 path to
ignored `scripts/repos.local` to omit `--cvc5` on subsequent runs.
The reporting launcher uses the same checkout configuration. See
[dependency setup](docs/maintenance.md#local-dependencies) for pinned checkouts
and Koine's shared updater.

See [the analyzer guide](docs/analyzer.md) for target selection, evidence,
identity, database conflicts and comparison of independent producers.

## What the analyzer checks

The default run covers the nine analyses that emit documented observations:

| analysis | observations |
| --- | --- |
| `ledger` | produced proof rules missing checkers or detected macro expansion, trusted registrations, and printer refusals |
| `ci` | gaps in proof-testing configuration and its completeness chain |
| `buildmode` | changes that need review against the safe-build invariant |
| `modes` | proof-unsupported options enabled without a direct safe-mode override |
| `rewrites` | implemented rewrites refused by the printer or restricted to unrestricted mode |
| `trust` | trust steps constructed without a reason id |
| `infer` | emitted inferences missing cases in a reconstructor with a trust fallback |
| `inferid` | inference ids shared across production sites, or sentinel ids used in production |
| `signature` | missing signature declarations, refused skolems, and rule-arity disagreements |

Both producers use this scope by default. `--analysis` selects a subset;
[the check catalogue](docs/checks.md#structured-observations) explains the
claims and their limitations. Developer reports and regression checks are
documented in [the command reference](docs/usage.md).

## An independent reading

```bash
prompts/dokimasia_analyzer_agent --cvc5 /path/to/cvc5 --dry-run
prompts/dokimasia_analyzer_agent --cvc5 /path/to/cvc5
scripts/compare_findings scratch/new-bugs.json scratch/agent-bugs.json
scripts/append_findings scratch/agent-bugs.json --dry-run
```

The assistant examines the same declared scope independently and writes the
same record format, with evidence and its actual coverage. Review new claims
before appending them. Agreement is evidence about the two producers; it does
not establish correctness.

## Findings and reporting

The [issue register](docs/issues.md) records candidates, requests and settled
hypotheses. [Filed findings and retractions](docs/findings.md) remain the
reviewed record. The database preserves observations across runs, including
ones subsequently disputed or resolved. Disappearance does not close a finding.

The [reporting workflow](docs/workflows.md) explains how to carry a finding
and process a reply. Its launchers are `prompts/check_dokimasia`,
`prompts/process_dokimasia` and `prompts/check_cvc5_issue`.
The [reporting bar](docs/pr-policy.md) requires a reproducer for behavioral
claims and leaves publication to a human.

## Documentation and development

| document | purpose |
| --- | --- |
| [Analyzer guide](docs/analyzer.md) | targets, observation records and producer comparison |
| [Developer commands](docs/usage.md) | detailed reports and optional measurements |
| [Checks](docs/checks.md) | emitted checks and their limits |
| [Maintenance](docs/maintenance.md) | tests, pins and script catalogue |
| [Documentation index](docs/README.md) | findings, case studies and design notes |

## The name

**δοκιμασία** was the scrutiny an official-elect in classical Athens underwent
before taking office. This tool examines the proof-production machinery before
a benchmark exercises a gap in it.

## How this repository is maintained

This repository is part of the **Eunoia ecosystem** and follows its shared
[repository policy](https://github.com/ajreynol/kanon/blob/main/docs/policy.md),
kept by Kanon. Anoieu implements the checker; CI pins its revision in
`scripts/deps.lock`.

**Written by AI agents, under light human supervision.** A human maintainer
directs the work, reviews it and decides what is reported upstream. Findings
are filed by the human. The shared
[reporting policy](https://github.com/ajreynol/anoieu/blob/main/docs/reports/reporting-policy.md)
describes that boundary and the intended audience.
