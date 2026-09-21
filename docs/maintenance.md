# Maintaining dokimasia

Dokimasia owns analysis of cvc5's proof-production source and its
`bug_db/` data artifact: records, evidence, triage and
closure decisions. Koine maintains the shared append, closure and history-window scripts.
Kanon owns ecosystem policy; Anoieu implements the optional policy checker.

General cvc5 development belongs to
[Paideia](https://github.com/ajreynol/paideia). Exploratory research on proof
support lives in `tools/ydoki/`; dependency pins and local configuration live
in `scripts/`. Proof-production performance belongs to
[Tachyon's Elaphros](https://github.com/ajreynol/tachyon/tree/main/tools/elaphros)
and is outside Dokimasia's scope.

Keep commands and their helpers in `scripts/`, assistant launchers in `prompts/`,
and analysis implementations in `dokimasia_analyzer/`. Add documents to the
documentation index (`docs/README.md`). Observations are recorded by the analyzer and
closed by an assessment of cvc5's history; what a closure
meant is written up in `docs/experience.md`.

For setup, start with **Local dependencies**. **Running the analyzer** explains
inputs and outputs; **The command reference** covers individual reports.
Contributors should use **Checks before handing off a change**. Paths in this
guide are relative to the repository root.

Regression baselines live in `tests/baselines/<analysis>.json`; the runtime
census lives in `tests/corpus/reach-corpus.json`. Default paths resolve from the
repository location, so checks work from any working directory; baseline
`--file` and corpus-sweep `--out` accept overrides. Re-record baselines with
`python3 -m dokimasia_analyzer write /path/to/cvc5` only after reviewing the change they
describe.

The analyzer and assistant default to the nine analyses in the README.
Standalone gates, fragment, TCB and latent reports are optional developer
measurements; the eight baseline ratchets and build invariant are the CI
regression suite. See the command reference.

Two documents are generated and neither is edited by hand:
`bug_db/fragment.md`, written whole by
`python3 -m dokimasia_analyzer.fragment doc`, and
`bug_db/bugs.md`, written whole by
`scripts/append_findings --render-only`. Both are regenerated and diffed by the
checks below, so neither can drift from the code beside it.

## Local dependencies

Use a dedicated `deps/koine` checkout at `scripts/koine.lock`. The analyzer
also accepts a clean sibling checkout at that exact revision, but a sibling
under active development will usually differ. `$KOINE` explicitly selects a
checkout and disables fallback. The analyzer never repairs dependencies during
a run.

For a new local installation, from this repository's root:

```bash
git clone https://github.com/ajreynol/koine.git deps/koine
git -C deps/koine checkout --detach "$(cat scripts/koine.lock)"
```

To refresh an existing clean, dedicated dependency checkout after a pin change:

```bash
git -C deps/koine fetch origin "$(cat scripts/koine.lock)"
git -C deps/koine checkout --detach "$(cat scripts/koine.lock)"
```

For cvc5, use an existing source checkout with `--cvc5`, `DOKIMASIA_CVC5`, or
an ignored `scripts/repos.local` containing `cvc5 /path/to/cvc5`. Alternatively,
put a dedicated checkout at `deps/cvc5`; the revision in `scripts/cvc5.lock` is
the one for baseline checks. Ordinary analysis records the revision actually
read. Both analysis producers, and `prompts/close_bug_db --use-local`, use the same
resolver, in which the environment takes precedence and a `cvc5` entry in
`scripts/deps.local.json` is the last fallback. No path is guessed: a checkout
this repository is not told about is not found.

**What a second pinned repository costs, measured on the Koine one:** a lock, a
resolver that refuses anything but the exact pinned commit in a clean checkout,
two extra checkout steps in CI and about two dozen lines of documentation —
cheaper than keeping a copy over the same period. The cost that is not obvious in
advance is that **every consumer's resolver becomes a small compatibility layer
the moment the provider reorganises**, and each consumer writes that layer
separately. `scripts/koine.py` probes the retired path only to say so in its
error, which is the whole of what that layer is worth.

The cvc5 lock keeps tests that assert exact counts reproducible and separates
analyzer changes from upstream changes. It is not a version requirement for
analysis: use the latest upstream `main`, a development branch, or another
explicitly selected revision. Updating that checkout is a separate action;
the analyzer records what it reads and never updates it automatically.

Local dependency JSON, if used, belongs in `scripts/deps.local.json`. For a
cvc5 configuration, prefer `scripts/repos.local`.

Check the setup and try a run before appending:

```bash
scripts/dokimasia_analyzer --dry-run
scripts/dokimasia_analyzer --no-update
scripts/append_findings scratch/new-bugs.json --dry-run
```

To update the database after reviewing that run, omit `--dry-run` from the last
command. `prompts/dokimasia_analyzer_agent` produces an independent dump;
the analyzer guide covers comparison.

## Checks before handing off a change

```bash
for test in tests/test_*.py; do python3 "$test" || exit; done
python3 -m dokimasia_analyzer check /path/to/pinned-cvc5 --verbose
for test in tests/test_*.py; do python3 "$test" /path/to/pinned-cvc5 || exit; done
scripts/append_findings --render-only --check
scripts/bump_anoieu --local /path/to/anoieu --offline --check
```

Both generated documents are covered by that list: the observation page by
`append_findings --render-only --check`, and `bug_db/fragment.md` by
`tests/test_fragment.py` when it is given the pinned checkout. Against any other
revision that one names itself as skipped rather than passing quietly, because a
diff taken elsewhere says nothing about drift.

Use the revision in `scripts/cvc5.lock` for the real-checkout tests. Do not move a
working checkout to satisfy a test. The analyzer integration tests use temporary
databases, never the committed record. CI provides the Koine revision from
`scripts/koine.lock`; locally the Koine-specific tests skip with an explanation
if that dependency is unavailable. Complete those tests before changing the
database integration.

## Commands and launchers

| command | purpose |
| --- | --- |
| `scripts/dokimasia_analyzer` | collect observations and evidence; optionally append via Koine |
| `scripts/append_findings` | validate a dump and evidence, append, or regenerate/check the page |
| `scripts/compare_findings` | compare producers on an identical source snapshot |
| `scripts/finding_id.py` | format a stable record or compute its identity without analysis |
| `scripts/targets.py`, `scripts/targets.json` | shared checkout resolution and declared input scope |
| `scripts/koine.py`, `scripts/koine.lock` | locate and verify the pinned Koine scripts |
| `scripts/closure.json`, `scripts/closure_baseline.py` | closure configuration and archived cvc5 baseline |
| `scripts/bug_reports.py` | local validation, archived evidence and Markdown rendering |
| `scripts/sweep_corpus` | run cvc5 over a corpus and record runtime counters |
| `scripts/audit_loc` | measure this repository's implementation and documentation |
| `scripts/bump_anoieu` | validate and update the pinned policy-checker revision |
| `prompts/dokimasia_analyzer_agent` | independent producer over the analyzer's targets |
| `prompts/close_bug_db` | assess which observations recent cvc5 commits closed, and write up what they did |

Commands that run live in `scripts/`; launchers that spend a turn on an
assistant live in `prompts/`, so a reader can tell which is which without
opening a directory. Neither prompt has a second copy to drift from: the
analyzer's is read from `prompts/analyzer.txt`; Koine assembles the closure
prompt from its shared discipline and the owner sections in `prompts/closure/`.
`tests/test_experience.py` checks the experience log's structure, and
`scripts/append_findings --render-only --check` checks the database view's.

## Pins and generated records

The Koine pin is `e4e4e2e760197429ff182826ed9b7a90fea11633`; its upstream
[`tests` check](https://github.com/ajreynol/koine/actions/runs/35463151942/job/105950505607)
completed successfully, verified on 2026-09-19. It supplies `koine_append_db`,
`koine_close_db`, `koine_window` and `koine_check_db` from `bug_db_manager/`.
Dokimasia holds the database lock across archiving, appending and rendering,
and invokes the append script with `--no-lock` inside that section.

To update `scripts/koine.lock`, choose a full Koine commit SHA and inspect the
`tests` check on that exact commit in GitHub. Only replace the lock's SHA after
that check succeeds; a failed, unfinished or unavailable check leaves the pin
unchanged. Record the checked commit and CI result with the change.

Refresh the dedicated checkout using the commands under
Local dependencies, then run the integration checks
before accepting the pin change. This pin selects the append utility and is
independent of the policy checker.

The policy-checker pin is `scripts/deps.lock`, and it names
`scripts/policy_check.py` in Anoieu. `scripts/bump_anoieu` is the one command
that moves it, and it moves it only onto a commit that passes **both** gates:
Anoieu's own CI was green at that commit, and the checker at that commit passes
against this tree.

**Dokimasia runs the `anoieu / policy` job on a checker pin, and that is a
decision rather than a default.** The shared policy offers two forms: a commit a
repository pins and moves itself, or a named policy contract checked by Anoieu's
shared workflow against current Anoieu. Both satisfy the joining requirement, and
what differs is what may move underneath a red build. On a pin, nothing moves
until this repository moves it; the price is that a correction to the checker is
not adopted until somebody runs `bump_anoieu`. On the contract form there is no
pin, and a checker correction can start reporting a violation already in the tree
— a build turning red with nothing committed here, which is what a pin exists to
prevent. Anoieu's requirement that a pin move only onto a green commit is a rule
about *moving* a pin, so it does not reach the contract form, and holding the pin
is what keeps `bump_anoieu` the place that rule is enforced.

```bash
scripts/bump_anoieu --show                             # pinned, local, upstream
scripts/bump_anoieu --local /path/to/anoieu --offline --check
scripts/bump_anoieu                                    # ask, check, then move
```

**Unknown is not green.** No network, an unfinished run, or a commit GitHub
reports nothing about all refuse, and a refusal for that reason exits `2` rather
than `1` so a run can log which of the two it hit. `--offline` asks nothing, so
it can check but cannot bump; `--force` is the way past either gate and is a
person's decision. This never runs in CI, because it reads a remote. Never
change a check merely to get a green pin.

`bump_anoieu` owns the JSON checker lock and the compatibility check described
above. The remaining shared dependency work is recorded in
discussion D6 (`docs/discussion.md`).

Only `bugs.json` determines database membership. The generated page is a view,
and the content-addressed run archives preserve the source version, evidence
and original dump independently of scratch files. Do not hand-edit these to
resolve a triage disagreement. Keep that decision in the existing findings
register. See the analyzer guide for identity, replay and conflict
semantics.

## Assessing closure

`prompts/close_bug_db` delegates to the pinned `koine_close_db`, configured by
`scripts/closure.json`. Koine supplies the history window, closure discipline,
assistant invocation and `koine_check_db` command in the prompt. Dokimasia keeps
baseline selection, local cvc5 validation, the empty-window guard, and its
owner sections in `prompts/closure/`. All closure modes, including previews,
require the pinned Koine checkout; cvc5 remains optional.

An observation is closed by **a change in cvc5 that somebody can point at**,
never by a later run failing to see it. The
bug database (`bug_db/README.md`) and the
analyzer guide both say so; the mechanics
here are what make it hold. The question the assessment asks is *what did this
commit change*, not *is this row still there*, so every closure arrives with a
commit attached and most commits close nothing.

```bash
prompts/close_bug_db --dry-run                  # the window, and nothing else
prompts/close_bug_db                            # assess it with an assistant
prompts/close_bug_db --use-local /path/to/cvc5  # from a checkout, if one has moved
prompts/close_bug_db --since <rev>              # against a different baseline
prompts/close_bug_db --show-prompt              # the text, running nothing
```

The baseline is the cvc5 revision of the newest archived run — the revision the
recorded claims actually describe — and the window runs from there to cvc5's
`main`. `scripts/cvc5.lock` is the fallback baseline rather than the default: it
pins what the regression checks reproduce, which is a different question and is
usually older. `scripts/closure_baseline.py` supplies that selection to Koine;
`--since` overrides it. Koine considers only observations without `closed_*` fields.

**cvc5 is not a dependency of this command.** The prompt names
`compare/<baseline>...main` and the assistant reads the history where it is
public, so a run needs no checkout, no clone and no fetch. This is not only
convenience: a dedicated `deps/cvc5` sits at the pinned revision, the pinned
revision is normally the baseline itself, and a window computed against it is
empty by construction. The launcher makes no network call of its own — the
reading is the assistant's — so `--show-prompt` is reproducible anywhere.

**`--use-local` is the optimisation.** Given a path it reads that tree; given no
value it resolves one the way the analyzer does, through `$DOKIMASIA_CVC5` or
`scripts/repos.local`. The window is then `baseline..HEAD` there, the prompt
lists it, and the tree is read and never written. A local window with nothing in
it starts no assistant and reports which refs in that checkout are already ahead
of its `HEAD`, because history fetched and left on a remote-tracking ref is the
usual reason for an empty one. Koine refuses shallow checkouts and warns when
the baseline is not an ancestor of the local HEAD.

A closure adds four fields to an entry in `bug_db/bugs.json` and changes nothing
else about it:

| field | what it holds |
| --- | --- |
| `closed_on` | the date the assessment was made |
| `closed_commit` | the cvc5 commit that closed it, in full |
| `closed_pr` | the pull request the commit subject names, where it names one |
| `closed_why` | what that commit changed, and what was re-read to confirm the claim is now false |

Koine's writer keeps fields it does not know about and never removes an entry,
so a marked observation survives later appends unchanged. It also keeps moving
`last_seen`: an analyzer run that re-observes a closed identity puts a sighting
after its `closed_on`, and that contradiction is exactly the signal that the
closure may be wrong. Koine reports it as a reopen candidate. Re-assess it —
do not tidy the record. The generated page
renders the original claim and is unaffected either way, which
`scripts/append_findings --render-only --check` confirms. The closure prompt also
requires `koine_check_db`: against the committed database, it rejects changed
claims, missing or reordered entries, and edits to existing closures. Start a
closure assessment from a committed database so that comparison isolates the
closure edits.

Each pull request is then written up in `experience.md`, whose
shape `tests/test_experience.py` holds. The run leaves both files uncommitted:
reading that diff is the review. Deciding what is worth carrying upstream, and
the rule that no program here sends anything to anybody, are unchanged and live
with the bar (`dokimasia_analyzer/README.md`).

### Remaining work

- **A curated row still has no fingerprint anybody can recompute.** Rows in
  the register (`docs/README.md`) are written by hand, so a closure assessed against
  the database cannot settle the register entry that quotes it. Settles when a
  row carries the `dokimasia:*` identity the analyzer already emits.
- **Corrections and reopening have no shared mechanics.** Koine's writer
  appends; preserving a corrected claim, a retraction or a reopening is
  specified nowhere. Until it is, those decisions stay in
  the register (`docs/README.md`) and the promises (`dokimasia_analyzer/README.md`), and a closure that
  turns out to be wrong is re-assessed in place.
- **A rejected claim changes nothing today.** Where cvc5 declines a row, no rule
  says whether that touches the bar or only the row.

## Running the analyzer

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
nine advertised analyses (`README.md`): `ledger`,
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

### The artifacts

| file | meaning |
| --- | --- |
| `scratch/new-bugs.json` | this run's stable observation records; `--dump` changes the path |
| `scratch/new-bugs.json.run.json` | matching evidence, actual coverage, measurements, target revision and input content digest |
| [bug_db/bugs.json](../bug_db/bugs.json) | Dokimasia's accumulated observation history, recorded through Koine's writer |
| bug_db/bugs.md | generated Markdown view of that database |
| `bug_db/runs/*.json` | archived observations and run records, named by their content digest |

`bug_db/` is this repository's data artifact.

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
Baseline changes remain the job of `python3 -m dokimasia_analyzer check`.

The optional latent analysis uses [the recorded corpus](../tests/corpus/reach-corpus.json)
and preserves its build provenance and limitations. It does not rerun that
corpus or establish that its runtime results hold at the current source revision.
The default run does not read the historical census.

### Identity and evidence

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
| `CI0002` | one of `safe-job`, `safe-job-proof-tester`, `check-proofs`, `no-granularity` |
| `CI0003` | `proof` |

File-based observations aggregate all matching sites in that file. Repeated
sites add evidence, not duplicate records. Renaming the affected entity or file
creates a new identity; relating it to the old one is a review decision.

#### What the run record carries, and what each field claims

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

### Koine

[`scripts/koine.lock`](../scripts/koine.lock) pins the utility. The resolver tries
`$KOINE` if explicitly set, otherwise a sibling `koine` checkout and then
`deps/koine`. It requires the exact pinned commit and a clean tracked tree. It
does not clone or change a checkout. Set up that dependency before updating the
database; `--dry-run` and analyzer `--no-update` do not require Koine.
The maintenance guide describes setup;
pin updates require a successful
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

### An independent second producer

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

### The existing record

The initial database is a fresh run at the source revision in
[`scripts/cvc5.lock`](../scripts/cvc5.lock), not an import of old prose. The archived
run records its date, source digest, analyzer content digest and revision; a dirty analyzer flag
means the implementation was still under review when the run was made.

The register (`docs/README.md`) holds all `i-*` candidates, `R*`
requests, process items, settled `s-*` hypotheses and filed `f-*` entries.
`dokimasia_analyzer/README.md` defines finding kinds and review standards;
`docs/experience.md` records cvc5's responses and changes. Nothing is closed,
reopened or promoted by a database append; closure is its own assessment.

Useful correspondences are `SEAM0001` with `i-7`, `INFER0002` with `i-22`,
`SIG0003` for `SUBS` with `i-21`, and `MODE0001` for `stringLazyPreproc` with
`i-2`. The `MODE0001` observation for `macrosQuantMode` still describes the
defaults-only scanner's result; `s-4` records why interpreting it as a reachable
defect was wrong. These are links between records, not new verdicts.

Closure is assessed separately, from cvc5's
own history rather than from a run: `prompts/close_bug_db` marks an entry only
where a named commit can be shown to have made its claim false, and
`experience.md` records what that change did. To carry a
structured observation into the reviewed register instead, review its claim and
archived evidence first. In the corresponding the register row, record the
`dokimasia:*` identity, link the archived run, and state what would settle the
claim. Reuse an existing row for the same question; a database id alone is not a
reviewed report. Keep replies and resolutions in the register and findings
ledger.

## The command reference

These examples describe the measurements at cvc5 `40a4bb7e4`, the revision in
[`scripts/cvc5.lock`](../scripts/cvc5.lock). Run a command to measure another
tree; the comments are recorded examples, not assertions about current upstream.


The advertised interface is `scripts/dokimasia_analyzer`, with the nine analyses
listed in the README (`README.md`). The commands below
expose their implementation details and optional measurements for development.
Standalone `gates`, `fragment`, `tcb`, and `latent` reports are opt-in; none
emits observation records. The TCB baseline remains part of the CI checks.

No dependencies; Python 3.10+; reads a checkout, needs no build.

```bash
python3 -m dokimasia_analyzer check  <cvc5>   # eight baseline ratchets and one invariant
python3 -m dokimasia_analyzer report <cvc5>   # the nine advertised analyses, printed
python3 -m dokimasia_analyzer report <cvc5> --analysis tcb --analysis latent  # explicit selection
```

**[`dokimasia_analyzer.buildmode`](../dokimasia_analyzer/buildmode/)** — is a safe *build* still an
unrestricted build with one option default flipped? That invariant is what keeps
cvc5's deliberate refusal to combine safe mode with debug symbols nearly
costless; the check examines the restriction discussed in cvc5
[#12899](https://github.com/cvc5/cvc5/pull/12899).

```bash
python3 -m dokimasia_analyzer.buildmode check <cvc5>       # 8 conditionals, all benign
python3 -m dokimasia_analyzer.buildmode sites <cvc5>       # each one, classified
```

**[`dokimasia_analyzer.latent`](../dokimasia_analyzer/latent/)** — optional comparison of the static
inventory with the historical runtime census in `tests/corpus/reach-corpus.json`.
Its runtime evidence applies to the recorded build and corpus.

```bash
python3 -m dokimasia_analyzer.latent census <cvc5>          # 182 of 203 latent, 0 in safe mode
python3 -m dokimasia_analyzer.latent list   <cvc5> --kind seam-rule
scripts/sweep_corpus --cvc5 <binary> --corpus <dir>  # regenerate the census
```

**[`dokimasia_analyzer.tcb`](../dokimasia_analyzer/tcb/)** — optional measurement of the trusted computing base of the
internal proof checker, the natural kernel candidate.

```bash
python3 -m dokimasia_analyzer.tcb measure  <cvc5>   # 179 files, 41,446 lines, 8.0% of src/
python3 -m dokimasia_analyzer.tcb cuts     <cvc5>   # what each dependency edge costs
python3 -m dokimasia_analyzer.tcb why      <cvc5> theory/strings/core_solver.h
python3 -m dokimasia_analyzer.tcb baseline <cvc5> --check    # ratchet, for CI
```

**[`dokimasia_analyzer.modes`](../dokimasia_analyzer/modes/)** — what safe and stable mode change
about the defaults, from all 172 option-setting sites in `set_defaults.cpp`.

```bash
python3 -m dokimasia_analyzer.modes delta    <cvc5>          # safe mode: 27 rows, 24 distinct settings
python3 -m dokimasia_analyzer.modes check    <cvc5>          # options that escape the promise
python3 -m dokimasia_analyzer.modes baseline <cvc5> --check  # ratchet, for CI
```

**[`dokimasia_analyzer.inferid`](../dokimasia_analyzer/inferid/)** — whether each `InferenceId` names
a single program point.

```bash
python3 -m dokimasia_analyzer.inferid check <cvc5>          # 51 ids produced at more than one site
python3 -m dokimasia_analyzer.inferid show  <cvc5> STRINGS_CODE_PROXY
python3 -m dokimasia_analyzer.inferid dead  <cvc5>          # 14 declared, produced nowhere
python3 -m dokimasia_analyzer.inferid stats <cvc5>
```

**[`dokimasia_analyzer.ledger`](../dokimasia_analyzer/ledger/)** — one row per `ProofRule`, four
columns: produced, checked, elaborated, printed.

```bash
python3 -m dokimasia_analyzer.ledger holes <cvc5>          # 14 rules the Eunoia seam cannot print
python3 -m dokimasia_analyzer.ledger rule  <cvc5> ARITH_POW2_INIT
python3 -m dokimasia_analyzer.ledger table <cvc5> --produced-only
```

**[`dokimasia_analyzer.trust`](../dokimasia_analyzer/trust/)** — the census of cvc5's declared holes:
every `TrustId`, where it is constructed, and the preprocessing correspondence.

```bash
python3 -m dokimasia_analyzer.trust census <cvc5>          # 75 ids: 70 live, 4 dead
python3 -m dokimasia_analyzer.trust passes <cvc5>          # which passes declare a hole
python3 -m dokimasia_analyzer.trust show   <cvc5> THEORY_LEMMA
```

**[`dokimasia_analyzer.ci`](../dokimasia_analyzer/ci/)** — an independent check that cvc5's proof
testing is still attached. CI is the safety net today, and one that quietly
stops being attached looks exactly like one that works.

```bash
python3 -m dokimasia_analyzer.ci proofs  <cvc5>            # the completeness chain
python3 -m dokimasia_analyzer.ci matrix  <cvc5>            # job x tester
python3 -m dokimasia_analyzer.ci testers <cvc5>            # what each tester passes
```

**[`dokimasia_analyzer.rewrites`](../dokimasia_analyzer/rewrites/)** — coverage of the 533-rule
rewrite vocabulary at the Eunoia seam.

```bash
python3 -m dokimasia_analyzer.rewrites coverage <cvc5>     # RARE vs hand-written vs applied
python3 -m dokimasia_analyzer.rewrites gaps     <cvc5>     # applied, and unprintable
```

**[`dokimasia_analyzer.fragment`](../dokimasia_analyzer/fragment/)** — optional report of the logical fragment cvc5
supports, per theory, and whether it is enforced. `doc` generates
`bug_db/fragment.md`, rewriting it whole;
`tests/test_fragment.py` regenerates and diffs it at the pinned commit.

```bash
python3 -m dokimasia_analyzer.fragment theories <cvc5>     # 341 kinds over 14 theories
python3 -m dokimasia_analyzer.fragment check    <cvc5>     # is the fragment enforced?
python3 -m dokimasia_analyzer.fragment doc      <cvc5> --out bug_db/fragment.md
```

**[`dokimasia_analyzer.infer`](../dokimasia_analyzer/infer/)** — does every inference a theory makes
have a proof reconstruction? The completeness core.

```bash
python3 -m dokimasia_analyzer.infer coverage  <cvc5>          # per theory
python3 -m dokimasia_analyzer.infer unhandled <cvc5> strings  # the ids that fall through
```

**[`dokimasia_analyzer.signature`](../dokimasia_analyzer/signature/)** — does the Eunoia signature
agree with cvc5's own account of a rule?

```bash
python3 -m dokimasia_analyzer.signature rules   <cvc5>     # 0 printable rules undeclared
python3 -m dokimasia_analyzer.signature skolems <cvc5>     # 24 constructed but unprintable
python3 -m dokimasia_analyzer.signature checker <cvc5>     # documented arity vs what the checker enforces
```

**[`dokimasia_analyzer.gates`](../dokimasia_analyzer/gates/)** — optional standalone reports of which
option legalises each term kind, and whether a rule can fire under
`--safe-mode=safe`. The rewrite analysis also uses this machinery for evidence.

```bash
python3 -m dokimasia_analyzer.gates kinds    <cvc5>        # 59 kinds carry an option gate
python3 -m dokimasia_analyzer.gates rule     <cvc5> LAMBDA_ELIM
python3 -m dokimasia_analyzer.gates verdicts <cvc5>        # blocked / partial / open
```


The low-level commands keep their existing output and exit conventions.
A candidate needs the option gate and a reproducer before it becomes a
proof-completeness defect. See the checks (`docs/README.md`) and the register (`docs/README.md`).

## What the corpus reaches

The static inventory says how many holes exist. This says how many any input has
touched, over all 2,608 `regress0` benchmarks, and the difference between them
is the number this repository should be judged on.


| | benchmarks producing a proof | benchmarks reaching **any** proof hole |
| --- | --- | --- |
| `--safe-mode=safe` | 1,061 | **0** |
| unrestricted (default) | 1,236 | **129** (10.4%) |

Both runs used `--produce-proofs --check-proofs --stats-internal`, which is what
switches on `d_checkProofHoles`; a hole is any non-empty
`finalProof::ruleUnhandledEoCount`, `trustCount`, `trustTheoryLemmaCount`,
`trustTheoryRewriteCount` or `theoryRewriteRuleUnhandledEoCount`.

**Safe mode reaches no hole at all on this corpus, and unrestricted reaches one
in ten.** That is the first quantified statement we have seen of what safe mode
buys, and it is a measurement rather than a reading of the option list.

It also sets the honest bound on this repository: **on regress0, safe mode is
clean.** A safe-mode completeness defect, if one exists, is not in this corpus —
which is exactly the population our static analysis claims to be for, and
exactly why finding one is hard.

### The subtraction, as a number


`dokimasia_analyzer.latent` performs it, and it is the count worth watching:

```
$ python3 -m dokimasia_analyzer.latent census <cvc5>
               safe  latent  unres   total
  inference       0      79      0      79
  rewrite         0      38      2      40
  seam-rule       0       5      9      14
  trust-id        0      60     10      70
  all             0     182     21     203
```

**182 of 203 declared holes have never been reached by any input we have run.**
That is the population cvc5's runtime oracle structurally cannot see, and the
number this repository should be judged on: it must move, in either direction.
An input promotes a hole to a finding; an unreachability argument removes it
from the inventory. A hole that resists both is the most interesting object
here.

*Latent is not unreachable.* It is the absence of evidence either way, and
`latent census` says so on every run.

The census this subtracts is recorded in
[`../tests/corpus/reach-corpus.json`](../tests/corpus/reach-corpus.json) with its provenance — binary
version, corpus, commit, and the exact counters queried — and is regenerated by
[`scripts/sweep_corpus`](../scripts/sweep_corpus).

### What this validates, and what it corrects


**The static seam analysis is sound against the runtime oracle.** cvc5's
completeness check is literally `!EoPrinter::isHandled(...)`
(`smt/proof_final_callback.cpp`), which is the predicate `dokimasia_analyzer.ledger`
computes without building. Every rule the corpus reported unhandled is in our
static gap list or in an argument-dependent arm we classify as *conditional*.
**Nine of the fourteen gaps we predicted were hit; none of the hits was outside
our prediction.** That is the strongest evidence we have that the tier is
measuring what it claims.

**The denominator is mostly untouched.** 10 of 70 live `TrustId`s and 2 of 40
unprintable rewrites were reached — 14% and 5%. The remaining 86% and 95% are
holes this corpus has never exercised. That is the population the repository
exists for, and it is now measured rather than assumed.

**Safe mode is doing real work, on identical inputs.**
`test/regress/cli/regress0/uf/cnf_abc.smt2` answers `unsat` in both modes; it
produces a `THEORY_UF` trust lemma in unrestricted and **none** in safe mode.
The same holds for `iso_icl_repgen004` and `SEQ032_size2`. Safe mode is not
merely refusing inputs — it changes the strategy so the hole is not taken.

### Limits, stated


- **One corpus, one level.** `regress0` only, 10s timeout, single-threaded
  defaults. `regress1`–`4` and the SMT-LIB benchmarks are not covered, and the
  692 benchmarks that produced no proof (parse errors, `sat`, timeouts) tell us
  nothing either way.
- **A binary from a branch.** Built at `95bef9bc44` on a feature branch with
  local modifications, not a release. The numbers should be reproduced on a
  clean build before any of them is quoted upstream.
- **Zero is not proof of absence.** Safe mode reaching no hole on regress0 says
  regress0 does not reach one. It is precisely the silence this repository
  refuses to read as coverage.
- **We got the stat names wrong first.** The initial sweep grepped for
  `trustIds` and `ruleEouCount` — the C++ *member* names — and reported zero
  holes in both modes. The registered names are `trustCount` and
  `ruleUnhandledEoCount`. A clean-looking zero from a query that cannot match is
  the most dangerous result an experiment can return, and it survived one round
  of interpretation before a spot check caught it.

### Reproducing


```bash
cvc5 --safe-mode=safe --produce-proofs --check-proofs --stats-internal b.smt2 \
  | grep -E '^finalProof::(trustCount|ruleUnhandledEoCount|trustTheoryLemmaCount)'
```

Note that `--check-proofs-complete` **cannot** be added in safe or stable mode:
it is `category = "expert"` and both modes refuse expert options — and it should
not be, since the same change would permit `--no-check-proofs-complete`. See
`R2` (`docs/README.md`). `--stats-internal` sets the same internal flag, so
the counters are available where the option is not.

## The static-analysis landscape

**No general-purpose analyzer can ask our question, and that is not a deficiency
in them.** Domain-independent tools look for *language-level* defects —
undefined behaviour, null dereference, leaks. Every finding here is **perfectly
well-formed C++** that violates a contract only cvc5 states: an `InferenceId`
with no reconstruction case, a `ProofRule` the Eunoia seam cannot print, a
technique reachable in safe mode with no proof support. So the tools are
**infrastructure, not analyzers** — clang gives an AST and a fix-it mechanism,
CodeQL gives a call graph, and the value is entirely in knowing which invariant
to state.

### D1 — Three artifacts, by what each question needs

| tier | question | artifact | cost to run |
| --- | --- | --- | --- |
| **0 — ledger** | is this table consistent with that table? | standalone Python, reads a checkout | **seconds, no build** |
| **1 — local** | does this call site attach a proof? | `cvc5-proof-*` checks in `contrib/tidy-checks/` | one clang-tidy pass |
| **2 — closure** | what can safe mode reach? | `.ql` queries in `contrib/codeql/` | one CodeQL DB build |

Tier 0 is deliberately not a clang tool: the ledger, the trust census, the
safe-mode delta and the seam coverage are all *table against table*, which needs
a bracket matcher rather than a compiler, runs on every push rather than
nightly, and produces findings before anyone configures a build. Tiers 1 and 2
belong **upstream in cvc5's tree** — a tool cvc5 has to install and schedule
will not be run; a check in `contrib/tidy-checks/` is already built and enforced
by a job that exists.

**D2 — recommend SARIF regardless of anything we write.** `run-clang-tidy` →
SARIF → `upload-sarif`, so findings annotate pull requests inline and get a
baseline and dismissal-with-reason. That is the difference between a nightly
that fails loudly and a nightly whose output somebody reads (`R11`, `p-1`).

### D3 — Where an invariant should live

Not every finding should become a check here. The cheapest enforcement that
actually holds is the right one, and the order is:

| if the invariant is… | it belongs as… | who maintains it |
| --- | --- | --- |
| decidable from types or constants at compile time | `static_assert` | cvc5, free, forever |
| decidable from cvc5's own tables at startup | an **assertion** in the registry that builds the table | cvc5, free, forever |
| a property of one function's AST | a `cvc5-proof-*` tidy check | cvc5, one nightly pass |
| a property of the whole call graph | a CodeQL query feeding a tidy check | cvc5, one nightly pass |
| only observable on an input | a corpus run with `--check-proofs-complete` | us |

**A check here that could have been an assertion in cvc5 is a design failure**,
not a feature. If `ProofChecker` can assert at registration time that every
`ProofRule` it is asked about has a checker, that invariant is enforced on every
developer's machine forever, and dokimasia should delete the corresponding
check and keep only the patch that introduced it.

Two facts make assertions more attractive here than they look. cvc5's `Assert`
compiles out unless `CVC5_ASSERTIONS` — but **the nightly static-analysis build
and the functional CI builds both configure `--assertions`**, so a recommended
`Assert` is genuinely enforced across cvc5's test suite. And `AlwaysAssert`
exists for the handful of invariants cheap enough to hold in production.

### D5 — Safe mode first, and the reproducer is the deliverable

`--safe-mode=safe` is the only configuration cvc5 promises complete proofs in,
so it is the only one where an incomplete proof is a **contract violation**
rather than a known gap.

See the contract (`docs/README.md`). `--safe-mode=safe` is the only
configuration cvc5 promises complete proofs in, so it is the only configuration
where an incomplete proof is a **contract violation** rather than a known gap.

Findings are ranked accordingly, and the rank is part of the finding:

| rank | what it is | evidence required |
| --- | --- | --- |
| **1** | safe mode produces an incomplete proof | **an input.** `.smt2` file, option set, quoted `--check-proofs-complete` failure |
| **2** | a hole reachable in safe mode, no input yet | the static argument, plus what fragment an input would need |
| **3** | a gap in stable or unrestricted | the static argument; filed as a roadmap item, not a bug |

Rank 1 is what we are for. The static analysis exists to make the search for
rank-1 inputs *targeted* — without it, finding these is running benchmarks and
hoping.

### D6 — The reproducer pipeline

Static hypothesis → corpus run under
`--safe-mode=safe --produce-proofs --check-proofs` → minimize with
[`ddsmt`](https://github.com/ddsmt/ddsmt) → attribute the failure back to the
site the analysis predicted → file with the input attached.

The last step is the one that closes the loop and the one worth measuring: **a
prediction that was confirmed by an input is the only evidence that a check is
worth running.** The headline number for this project is how many rank-1 inputs
it produced that cvc5's regression suite does not already contain.

**D7 — performance budget.** Tier 0 must stay under a few seconds so it can run
per-push as a lint; tiers 1 and 2 inherit the nightly's budget, which already
absorbs a CodeQL database build. Nothing here needs a new machine.

### Posture toward murxla

[murxla](https://github.com/murxla/murxla) is an end-to-end, black-box fuzzer
for SMT solvers. It is already an `ExternalProject` in cvc5's build
(`cmake/fuzzing-murxla.cmake`), pinned and maintained by people who are good at
it. **It is a separate project and we should keep it that way.**

The division is not about quality, it is about method:

| | murxla | dokimasia |
| --- | --- | --- |
| **method** | black box — generate inputs, run the solver, check an oracle | white box — read the C++ |
| **finds a hole by** | *hitting* it | *reading* it |
| **needs** | a build, and time | a checkout, and seconds |
| **can say** | "this input breaks it" | "this code path has no proof, and nothing has ever run it" |
| **cannot say** | anything about a path its inputs never reach | with certainty that a path is reachable |

Those last two rows are the whole relationship, and they are complementary
rather than competitive. Safe mode already has almost no proof holes on SMT-LIB,
so the holes that remain are the ones **no input has reached** — which is
exactly what a black-box tool cannot find and a white-box tool can. Symmetrically,
we can point at a suspicious path and be wrong about whether anything reaches it;
an input settles that and we cannot manufacture one by reading.

**So we do not build, wrap, drive or vendor a fuzzer.** Concretely:

- no fuzzing harness in this repository, and no dependency on murxla;
- we do not measure ourselves in bugs-found-by-fuzzing;
- when a static finding needs a witness input, the honest options are to
  construct one by hand or to hand the *fragment description* to whoever runs
  the fuzzing — "this hole needs a formula with these features" is a useful
  thing to give someone, and it is the right size of contribution;
- if murxla finds a proof hole, it lands in our `holes/` corpus as a regression
  and as evidence about a code site, which is data we consume, not work we did.

The one thing we should actively want from that direction is the *negative*
information: a hole murxla has never produced, in code we believe is reachable,
is the most interesting object either tool produces.
