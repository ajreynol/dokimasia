# Running and comparing the analyzer

`scripts/dokimasia_analyzer` runs the existing analyses in one process, writes
this run's observations and evidence, then passes the observations to Koine.
It needs Python 3.10+ and a cvc5 source checkout. It builds nothing.

```bash
scripts/dokimasia_analyzer --cvc5 /path/to/cvc5 --dry-run
scripts/dokimasia_analyzer --cvc5 /path/to/cvc5 --no-update
scripts/dokimasia_analyzer --cvc5 /path/to/cvc5
scripts/dokimasia_analyzer --analysis ledger --analysis ci
```

The last command selects analyses explicitly; omitting `--analysis` runs the
nine [advertised analyses](../README.md#what-the-analyzer-checks): `ledger`,
`ci`, `buildmode`, `modes`, `rewrites`, `trust`, `infer`, `inferid`, and `signature`.
The program and assistant launcher share this default. Standalone `gates`,
`fragment`, `tcb`, and `latent` measurements are developer tools, included only
when explicitly selected with `--analysis`. Explicit selections replace the
default list. Gate reasoning needed by rewrite checks still runs as part of
those checks.

`--target` selects a named target from
[`targets.json`](../scripts/targets.json); initially there is one, `cvc5`.
`--config` supplies an alternative target manifest.

Checkout resolution is: `--cvc5`, `$DOKIMASIA_CVC5`, `$CVC5`, an entry in
`scripts/repos.local`, a `cvc5.path` in `scripts/deps.local.json`, then
`deps/cvc5`. The ignored local map contains lines
like `cvc5 /path/to/cvc5`; relative paths are relative to the map. Override its
location with `$DOKIMASIA_REPOS_FILE`. An explicitly selected missing checkout
fails; it never silently switches to another. These commands never fetch,
build, or change the target checkout.

The analyzer does not use [`scripts/cvc5.lock`](../scripts/cvc5.lock) to select
or reject a checkout. That file fixes the regression-test reference; analyzing
the latest cvc5 records the revision and source contents actually read.

`prompts/close_bug_db` reads cvc5's published history and needs no checkout at
all; its `--use-local` option uses this same resolver when one is worth reading. Write new configurations in `scripts/repos.local`; the
JSON entry is the last fallback. **No path is guessed**, including `~/cvc5`: a
checkout this repository is not told about is not found, because a resolver that
guesses can measure a tree nobody named.

`--dry-run` lists the input scope and missing required paths, without running
checks or creating output files. Each scanner may read only part of that scope;
the run record lists the files actually read. Missing inputs and extraction
errors abort the run before writing a new dump or updating the database. An
existing dump is left untouched after failure, so check the command's exit code.
Input content is hashed before and after analysis to reject a changing checkout.

## The artifacts

| file | meaning |
| --- | --- |
| `scratch/new-bugs.json` | this run's stable observation records; `--dump` changes the path |
| `scratch/new-bugs.json.run.json` | matching evidence, actual coverage, measurements, target revision and input content digest |
| [bug_db/bugs.json](../bug_db/bugs.json) | Dokimasia's accumulated observation history, recorded through Koine's writer |
| [bug_db/bugs.md](../bug_db/bugs.md) | generated Markdown view of that database |
| `bug_db/runs/*.json` | archived observations and run records, named by their content digest |

[`bug_db/`](../bug_db/README.md) is this repository's data artifact.

Archives are saved before the database append, so a database entry never depends
on an overwritten scratch file. An archive may also exist for an append that
failed afterward; database membership is determined by `bugs.json`. The database
and page are separate replacements: if rendering is interrupted, regenerate the
page with `scripts/append_findings --render-only`. `--render-only --check`
checks it without writing. `--db` and `--page` redirect both outputs for trials;
archives live beside the selected database, as does the default `bugs.md` view.

The database contains **static observations**, including candidates and hygiene
or instrumentation gaps. It carries no current verdict. Supporting measurements
such as dead entities remain in the run record. TCB size, standalone gate and
fragment reports, and historical corpus measurements appear only when selected.
Baseline changes remain the job of `python3 -m dokimasia check`.

The optional latent analysis uses [the recorded corpus](../tests/corpus/reach-corpus.json)
and preserves its build provenance and limitations. It does not rerun that
corpus or establish that its runtime results hold at the current source revision.
The default run does not read the historical census.

## Identity and evidence

Every stable record has `id`, `bug`, `tool`, `owner`, `code`, `entity`,
`description` and `kind`. Obtain that shape with:

```bash
python3 scripts/finding_id.py SEAM0001 SAT_REFUTATION --record
```

The id is `dokimasia:` followed by 24 hexadecimal digits of SHA-256 over the
compact JSON array `[owner, code, entity]`. The owner is `cvc5`. Line numbers,
checkout paths, producer, commit, dates and wording do not enter the identity.
This namespace matters because Koine treats an explicit `id` as a global key.

| codes | entity convention |
| --- | --- |
| `RULE0001`, `RULE0002`, `ELAB0001`, `SEAM0001`, `SIG0001`, `SIG0003` | the `ProofRule` enum name |
| `RW0001`, `RW0002` | the `ProofRewriteRule` enum name |
| `SIG0002` | the `SkolemId` enum name |
| `MODE0001` | the option's internal name |
| `INFER0002` | `theory:InferenceId` |
| `INFERID0001` | the `InferenceId` enum name |
| `INFERID0002` | `src/relative/file.cpp#SENTINEL_NAME` |
| `TRUST0001` | the project-relative source filename, including `src/` |
| `BUILD0001` | `src/relative/file#conditional`, `src/relative/file#reader`, or `CMakeLists.txt: excluded/file.cpp` as reported by the scanner |
| `CI0001`, `CI0004` | `workflow.yml#matrix-job-name` |
| `CI0002` | one of `safe-job`, `safe-job-proof-tester`, `check-proofs`, `no-granularity`, `explicit-completeness` |
| `CI0003` | `proof` |

File-based observations aggregate all matching sites in that file. Repeated
sites add evidence, not duplicate records. Renaming the affected entity or file
creates a new identity; relating it to the old one is a review decision.

### What the run record carries, and what each field claims

The sidecar beside a dump is the provenance, and these are the fields a decision
about a record has to read. Both producers write the same shape.

| field | what it claims |
| --- | --- |
| `producer` | `program` or `agent` — which of the two producers wrote this |
| `analyses` | the analyses actually selected. A run narrowed with `--analysis` says so here, and nowhere else |
| `complete` | every **selected** check was examined over its whole scope. It is not a claim that every analysis ran; read `analyses` for that |
| `targets[].commit`, `.dirty` | the revision read, and whether the tree was clean at the time |
| `targets[].input_sha256` | the content digest of the declared input. **Two runs agreeing here read the same bytes**, which is what makes them comparable |
| `targets[].files` | the declared input scope at that revision |
| `coverage.<target>.read` | the files actually read. The agent also writes `not_read` |
| `analyzer_commit`, `analyzer_sha256`, `analyzer_dirty` | which analyzer produced it, by commit and by digest of the implementation |
| `dump_sha256` | the exact dump bytes these fields describe |
| `observed_on` | the date of the run |
| `evidence` | locations and excerpts, keyed by target and finding id |
| `measurements` | the per-analysis numbers behind the observations |

**`complete` is about honesty, not breadth**, and reading it as breadth is the
error to avoid: a program run of one analysis is `complete` and covers a ninth
of the catalogue. **Comparability is `input_sha256` plus `analyses`**: without
both equal, a record present in one run and absent from the other says nothing
about cvc5.

Locations, source excerpts, changing mode restrictions and measurements belong
in the sidecar's `evidence`, keyed by target and finding id. This keeps a line
shift or a new source commit from generating a Koine conflict. A changed claim
under the same id still produces a conflict: Koine keeps the original claim
and updates `last_seen`, even on a conflict. It returns success for conflicts;
read its diagnostic output. A later sighting does not mean the original claim
was reconfirmed. Absent observations remain in the database unchanged.

## Koine

[`scripts/koine.lock`](../scripts/koine.lock) pins the utility. The resolver tries
`$KOINE` if explicitly set, otherwise a sibling `koine` checkout and then
`deps/koine`. It requires the exact pinned commit and a clean tracked tree. It
does not clone or change a checkout. Set up that dependency before updating the
database; `--dry-run` and analyzer `--no-update` do not require Koine.
The [maintenance guide](maintenance.md#local-dependencies) describes setup;
[pin updates](maintenance.md#pins-and-generated-records) require a successful
upstream check at the selected commit and local integration checks.

```bash
scripts/append_findings scratch/new-bugs.json --dry-run
scripts/append_findings scratch/new-bugs.json
```

The wrapper validates both files and the dump's content hash before calling
[`bug_db_manager/koine_append_db`](https://github.com/ajreynol/koine/tree/main/bug_db_manager).
Malformed records or duplicate ids apply nothing. The wrapper holds the
database's `.lock` across archiving, appending and rendering, and passes
`--no-lock` to Koine to avoid acquiring the same lock twice. Direct Koine calls
use that same lock by default, but do not archive evidence or refresh the page;
use the wrapper to keep the complete artifact together.
`--date YYYY-MM-DD` is for deliberate replay, not for inventing historical
discovery dates.

## An independent second producer

```bash
prompts/dokimasia_analyzer_agent --cvc5 /path/to/cvc5 --dry-run
prompts/dokimasia_analyzer_agent --cvc5 /path/to/cvc5 --show-prompt
prompts/dokimasia_analyzer_agent --cvc5 /path/to/cvc5
scripts/compare_findings scratch/new-bugs.json scratch/agent-bugs.json
scripts/append_findings scratch/agent-bugs.json --dry-run
```

The launcher uses the same target resolver and writes an input snapshot before
starting an assistant. The canonical prompt is [analyzer.txt](../prompts/analyzer.txt).
It asks for an independent source reading, uses only the emitted catalogue,
forbids reading program results, and writes a dump plus evidence and honest
coverage. The identity helper formats a claim; it does not establish that claim.
`--codex` selects the alternative assistant and `--print` runs noninteractively.

Comparison refuses different input snapshots or analysis selections. It reports
shared identities, different claims and observations unique to each producer.
Partial agent coverage is displayed, so absence is not treated as a miss. The
separate Koine dry run compares against accumulated history, which is a different
question from agreement on this run. Review new agent claims before appending.

## The existing record

The initial database is a fresh run at the source revision in
[`scripts/cvc5.lock`](../scripts/cvc5.lock), not an import of old prose. The archived
run records its date, source digest, analyzer content digest and revision; a dirty analyzer flag
means the implementation was still under review when the run was made.

[`issues.md`](issues.md) remains the register for all `i-*` candidates, `R*`
requests, process items, settled `s-*` hypotheses and filed `f-*` entries.
[`findings.md`](findings.md) retains the reporting kinds, filed record and
retractions. Nothing is closed, reopened or promoted by a database append;
closure is [its own assessment](maintenance.md#assessing-closure).

Useful correspondences are `SEAM0001` with `i-7`, `INFER0002` with `i-22`,
`SIG0003` for `SUBS` with `i-21`, and `MODE0001` for `stringLazyPreproc` with
`i-2`. The `MODE0001` observation for `macrosQuantMode` still describes the
defaults-only scanner's result; `s-4` records why interpreting it as a reachable
defect was wrong. These are links between records, not new verdicts.

[Closure](maintenance.md#assessing-closure) is assessed separately, from cvc5's
own history rather than from a run: `prompts/close_bug_db` marks an entry only
where a named commit can be shown to have made its claim false, and
[`experience.md`](experience.md) records what that change did. To carry a
structured observation into the reviewed register instead, review its claim and
archived evidence first. In the corresponding `issues.md` row, record the
`dokimasia:*` identity, link the archived run, and state what would settle the
claim. Reuse an existing row for the same question; a database id alone is not a
reviewed report. Keep replies and resolutions in the register and findings
ledger.
