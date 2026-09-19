# Dokimasia's bug database

**[Browse the recorded bugs in Markdown](bugs.md).** The generated table is
readable directly on GitHub, with no server or local setup.

This directory is a **data artifact of Dokimasia**: the bugs and observations
recorded from its runs, including candidates, disputed claims and observations
[since closed](#closing-an-observation) by a cvc5 change. Dokimasia owns the
records, evidence, triage and closure decisions. [Koine's `bug_db_manager`](https://github.com/ajreynol/koine/tree/main/bug_db_manager)
provides the shared writer; its tooling lives in Koine.

| Artifact | Contents |
| --- | --- |
| [bugs.json](bugs.json) | persistent observation history, with stable identities and ingestion dates |
| [bugs.md](bugs.md) | generated browsing view of every database entry |
| [runs/](runs/) | archived run records: observations, evidence, source revisions and actual coverage |

Scratch dumps are disposable; these committed artifacts preserve the record.

## Record a run

From the repository root, with Python 3.10 or later and a cvc5 source checkout:

```bash
scripts/dokimasia_analyzer --cvc5 /path/to/cvc5 --dry-run
scripts/dokimasia_analyzer --cvc5 /path/to/cvc5
```

The first command checks the input scope without writing. The second runs the
analyzer, writes a dump and matching evidence in `scratch/`, archives the run,
appends through Koine and refreshes `bugs.md`. Recording must succeed for the
command to succeed. Repeating a run adds no duplicate identities.

Updates need a clean Koine checkout at [`scripts/koine.lock`](../scripts/koine.lock),
resolved through `$KOINE`, a sibling `koine`, or `deps/koine`. See
[dependency setup](../docs/maintenance.md#local-dependencies). Analysis and
recording never fetch or alter a dependency checkout.

To inspect a run before recording it:

```bash
scripts/dokimasia_analyzer --cvc5 /path/to/cvc5 --no-update
scripts/append_findings scratch/new-bugs.json --dry-run
scripts/append_findings scratch/new-bugs.json
```

The append preview validates the dump and its `.run.json` sidecar, then invokes
Koine's dry run; it changes neither the database, archives nor Markdown.
The [independent assistant producer](../docs/maintenance.md#an-independent-second-producer)
uses the same format and append command after its claims are reviewed. Both
producers use the same identity space and artifact; the archive records which
producer supplied the evidence.

## Refresh the Markdown view

```bash
scripts/append_findings --render-only
scripts/append_findings --render-only --check
```

Rendering requires neither cvc5 nor Koine. The check fails if the view is stale;
CI runs it. Commit `bugs.json`, `bugs.md` and new run archives together. Do not
edit the generated table; the next render replaces it. Runtime `*.json.lock`
files are ignored.

`--db` selects another database for a trial; its archives go in an adjacent
`runs/` directory and its default view is an adjacent `bugs.md`. `--page`
overrides that view's location.

## Interpret the record

The JSON has a top-level `bugs` array. Each observation carries an `id`, `bug`,
`tool`, `owner`, `code`, `entity`, `description` and `kind`, plus Koine's
`first_seen` and `last_seen` ingestion dates. The
[analyzer guide](../docs/maintenance.md#identity-and-evidence) defines identities
and the evidence keyed by those identities in the run archives.

Koine preserves the original claim and updates `last_seen` on re-ingestion,
including when it reports a conflicting claim. Dates do not establish fresh
reproduction or confirmation. An absent observation stays in the database;
absence alone does not establish that it was fixed.

## Closing an observation

A closure is a decision about a **cvc5 change**, made by
[`prompts/close_bug_db`](../prompts/close_bug_db): it reads the commits
between the revision an observation was recorded against and the local cvc5
checkout, and marks only what a commit can be shown to have fixed. Disappearance
from a later dump closes nothing, and a database append neither closes nor
promotes a claim.

A closed entry carries `closed_on`, `closed_commit`, `closed_pr` where the
commit names one, and a one-sentence `closed_why`. Everything else about it is
untouched: the identity, the original claim and both dates. Nothing is ever
removed, so an entry re-observed after its `closed_on` is a closure to
re-assess, not a record to correct. What the change actually did is written up
in [`docs/experience.md`](../docs/experience.md), one section per pull request.

Reviewed verdicts, replies and retractions stay in the
[issue register](../docs/README.md#the-register) and the
[findings ledger](../dokimasia/README.md#what-a-finding-is); see
[assessing closure](../docs/maintenance.md#assessing-closure) for the mechanics
and what is still missing.
