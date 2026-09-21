# Observation database

Browse the [recorded observations](bugs.md) without running the analyzer.
The database contains candidates, disputed claims and observations later closed
by a cvc5 change. **A recorded observation is not necessarily a confirmed bug.**

Dokimasia owns the records, evidence and review decisions.
[Koine's database tools](https://github.com/ajreynol/koine/tree/main/bug_db_manager)
provide the shared append, history-window and closure operations.

| Artifact | Contents |
| --- | --- |
| [bugs.json](bugs.json) | observation history, stable identities and ingestion dates |
| [bugs.md](bugs.md) | generated browsing view of every database entry |
| [runs/](runs/) | archived observations, evidence, source revisions and actual coverage |
| [fragment.md](fragment.md) | generated report of proof support by theory |

## Record a run

Use Python 3.10 or later and a cvc5 source checkout. From the repository root:

```bash
# Preview inputs, then save a run for inspection.
scripts/dokimasia_analyzer --cvc5 /path/to/cvc5 --dry-run
scripts/dokimasia_analyzer --cvc5 /path/to/cvc5 --no-update

# After review, preview and apply the database update.
scripts/append_findings scratch/new-bugs.json --dry-run
scripts/append_findings scratch/new-bugs.json
```

Analysis needs only cvc5's source. Appending, including its preview, also needs
a clean Koine checkout at [scripts/koine.lock](../scripts/koine.lock), found
through `$KOINE`, a sibling `koine` directory or `deps/koine`. Setup is in
**Local dependencies** in `docs/maintenance.md`. No dependency is fetched or
changed during a run.

The append command validates the dump and its `.run.json` evidence sidecar,
archives the run, updates the database and refreshes `bugs.md`. The preview
writes nothing. Repeating a run adds no duplicate identities.

To analyze and record in one command, omit `--no-update` from the analyzer
command. Recording must succeed for that command to succeed. The independent
assistant producer uses the same format and append command; review its claims
before appending them.

## Refresh the generated view

```bash
scripts/append_findings --render-only
scripts/append_findings --render-only --check
```

Rendering requires neither cvc5 nor Koine. CI runs the check and rejects a
stale view. Commit `bugs.json`, `bugs.md` and new run archives together; edit
the source data rather than the generated table.

For a trial database, use `--db /path/to/bugs.json`. Archives and the default
Markdown view go beside it. `--page` overrides the view's location.

## Interpret a record

The JSON has a top-level `bugs` array. Each observation carries an `id`, `bug`,
`tool`, `owner`, `code`, `entity`, `description` and `kind`, plus `first_seen`
and `last_seen` ingestion dates. See **Identity and evidence** in
`docs/maintenance.md` for the identity scheme and archived evidence.

Koine preserves the original claim and updates `last_seen` on re-ingestion,
including when it reports a conflicting claim. These dates do not establish
fresh reproduction. An absent observation remains in the database.

## Close an observation

`prompts/close_bug_db` launches an assessment of cvc5's history using the pinned
Koine tools. A closure requires evidence of a cvc5 change that fixed the claim;
disappearance from a later run is insufficient. See **Assessing closure** in
`docs/maintenance.md` for commands and requirements.

Closed entries keep their original identity, claim and ingestion dates, and
add `closed_on`, `closed_commit`, `closed_pr` when available, and `closed_why`.
Re-observing a closed entry produces a reopen candidate for review.

The issue register in `docs/README.md` holds reviewed verdicts and filed
findings. `docs/experience.md` records cvc5's responses and changes. All
documentation paths here are relative to the repository root.
