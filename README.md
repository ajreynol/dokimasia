# dokimasia

A static analyzer for **cvc5’s proof-production code**: the C++ that constructs
proofs and the seam that prints them in Eunoia for ethos to check.

It looks for gaps in proof coverage, inconsistencies in the safe-mode contract,
and mismatches between proof production, checking and printing. It reads a
source checkout; it needs no cvc5 build. The analysis is partial: a clean run means the selected
checks found nothing, and a reported static gap still needs evidence of reachability.

Modelled on [anoieu](https://github.com/ajreynol/anoieu), whose subject is
Eunoia signatures. Dokimasia’s subject is the proof-production C++.

Dokimasia's scope is **cvc5's proofs**, not general cvc5 development. General
development work belongs to [Paideia](https://github.com/ajreynol/paideia),
which is the source of truth for it.

**Performance is out of scope**, including the time and memory overhead of
producing proofs. That work belongs to
[Elaphros in Tachyon](https://github.com/ajreynol/tachyon/tree/main/tools/elaphros).

## Run the analyzer

Python 3.10 or later; no Python dependencies.

Use any cvc5 source checkout, including the latest upstream `main`. The revision
in [`scripts/cvc5.lock`](scripts/cvc5.lock) is the reference for regression tests
and historical measurements; it does not restrict what the analyzer can read.

```bash
scripts/dokimasia_analyzer --cvc5 /path/to/cvc5 --dry-run
scripts/dokimasia_analyzer --cvc5 /path/to/cvc5 --no-update
scripts/dokimasia_analyzer --cvc5 /path/to/cvc5
```

The first command shows the source scope and missing inputs. The second runs
the nine analyses below and writes a dump with a matching evidence record.
The third also appends observations to [the database](bug_db/bugs.json) through
[Koine's writer](https://github.com/ajreynol/koine/tree/main/bug_db_manager) and regenerates
[the Markdown view](bug_db/bugs.md).

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

**[`bug_db/`](bug_db/README.md) is a data artifact of this repository:** the bugs
and observations recorded from Dokimasia runs, with their archived evidence.
Dokimasia owns that history and its interpretation; Koine provides the tooling.
**[Browse all recorded observations in Markdown](bug_db/bugs.md).** Recording
commands refresh the view, and CI checks that it matches the JSON.

The [issue register](docs/issues.md) records candidates, requests and settled
hypotheses. [Filed findings and retractions](docs/findings.md) remain the
reviewed record. The database preserves observations across runs, including
ones subsequently disputed or resolved. Disappearance does not close a finding.

**What cvc5 has since done about them** is assessed from cvc5's own history,
never from a finding going quiet:

```bash
prompts/close_bug_db --dry-run
prompts/close_bug_db
prompts/close_bug_db --use-local /path/to/cvc5
```

**No cvc5 checkout is needed.** The launcher names the window — the commits
between the revision an observation was recorded against and cvc5's `main` — and
the assistant reads it at [cvc5's repository](https://github.com/cvc5/cvc5),
where the history is public. `--use-local` points it at a checkout instead, when
one is to hand and has moved; it is an optimisation, not a requirement. The
launcher makes no network call itself, so `--show-prompt` prints the same text
anywhere. A closure names the commit and the pull
request on the database entry, and is written up in
[experience.md](docs/experience.md). Nothing is committed, nothing is pushed, and
no program here touches a tracker. See
[the closure assessment](docs/maintenance.md#assessing-closure).

## A question this repository will not answer

The analyzer measures and declines to recommend. **Which** of what safe mode
switches off is worth making proof-supported, and **in what order**, is a
judgement about where somebody else should spend their effort — unfalsifiable by
any run, and so deliberately outside what the checks claim.

[**ydoki**](tools/ydoki/README.md) is the research child that asks it anyway, on
two axes that are mirror images and are not ranked against each other: the
**theories** safe mode refuses, which shrink the input language, and the
**options** it refuses, which are techniques withheld on inputs it already
accepts. It adds no instrument — every figure in it comes from `fragment`,
`modes`, `ledger` and `signature` here — and it produces prose, not code.

**Nothing in it is this repository's position, and nothing in it has been
carried to anybody.** It is named here because the question is worth finding,
not because the analyzer endorses an answer; the charter's out-of-scope list is
the part to read first.

## Documentation and development

| document | purpose |
| --- | --- |
| [Bug database](bug_db/README.md) | the data artifact, recording commands and Markdown browsing |
| [Analyzer guide](docs/analyzer.md) | targets, observation records and producer comparison |
| [Developer commands](docs/usage.md) | detailed reports and optional measurements |
| [Checks](docs/checks.md) | emitted checks and their limits |
| [Experience](docs/experience.md) | the cvc5 changes that closed an observation, and what they say about the checks |
| [Maintenance](docs/maintenance.md) | tests, pins, closure assessment and the script catalogue |
| [The plan](TODO.md) | what is measured today, what is queued, and what we have decided not to do |
| [Documentation index](docs/README.md) | findings, case studies and design notes |
| [ydoki](tools/ydoki/README.md) | the research child: which theories and options are worth making proof-supported, and in what order |

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
are filed by the human. What this repository holds itself to is stated in its
own tree — [the promises](docs/findings.md#the-promises) and
[the bar](docs/findings.md#the-bar). They began as a position shared with
anoieu, in a [reporting policy](https://github.com/ajreynol/anoieu/blob/06bd7872ea5ce24bf4d264bf5e6958ed8edee3c2/docs/reports/reporting-policy.md)
anoieu deprecated and then removed; that link is pinned to the last commit the
page existed at, because provenance a reader cannot fetch is not provenance.
