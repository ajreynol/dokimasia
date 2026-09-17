# dokimasia

A static analyzer for **cvc5’s proof-production code**: the C++ that constructs
proofs and the seam that prints them in Eunoia for ethos to check.

It looks for gaps in proof coverage, inconsistencies in the safe-mode contract,
and changes to the machinery that checks proofs. It reads a source checkout;
it needs no cvc5 build. The analysis is partial: a clean run means the selected
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
all 13 analyses and writes a dump with a matching evidence record. The third
also appends observations to [the database](docs/reports/bugs.json) through
[Koine](https://github.com/ajreynol/koine) and regenerates
[the readable table](docs/reports/static-analysis.md).

Database updates require a clean Koine checkout at `scripts/koine.lock`, found
through `$KOINE`, a sibling `koine` directory, or `deps/koine`. No checkout is
fetched or changed by the analyzer. Set `DOKIMASIA_CVC5` or add a cvc5 path to
ignored `scripts/repos.local` to omit `--cvc5` on subsequent runs.

See [the analyzer guide](docs/analyzer.md) for target selection, evidence,
identity, database conflicts and comparison of independent producers.

## What exists today

The existing commands remain available:

```bash
python3 -m dokimasia check  /path/to/cvc5  # eight baseline ratchets and one invariant
python3 -m dokimasia report /path/to/cvc5  # individual analysis reports
```

The analyses cover proof-rule and rewrite coverage, inference reconstruction,
trust steps, option gates, the supported fragment, safe-build behavior,
signature agreement, proof CI and the checker’s dependency surface.
[Individual commands](docs/usage.md) expose the details;
[the check catalogue](docs/checks.md) states their limitations.

`scripts/sweep_corpus` records runtime counters from an existing cvc5 binary.
The latent analysis compares its historical census with the static inventory;
a source-only analyzer run does not refresh that runtime evidence.

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
| [Individual commands](docs/usage.md) | existing analysis interfaces |
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
