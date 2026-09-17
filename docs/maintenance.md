# Maintaining dokimasia

Dokimasia owns analysis of cvc5's proof-production source and the evidence and
interpretation of its observations. Koine maintains the accumulated JSON list.
Kanon owns ecosystem policy; Anoieu implements the optional policy checker.

Keep commands and their helpers in `scripts/`, assistant launchers in `prompts/`,
and analysis implementations in `dokimasia/`. Add documents to the
[documentation index](README.md). The existing reporting workflow and its
human review boundary remain in [workflows.md](workflows.md).

Regression baselines live in `tests/baselines/<analysis>.json`; the historical
runtime census lives in `tests/corpus/reach-corpus.json`. These used to sit at
the repository root because the commands used bare filenames. Default paths
now resolve from the repository location, so checks work from other working
directories. Baseline `--file` and corpus-sweep `--out` still accept overrides.
Re-record baselines with `python3 -m dokimasia write /path/to/cvc5` only after
reviewing the change they describe.

The analyzer and assistant default to the nine analyses in the README.
Standalone gates, fragment, TCB and latent reports are optional developer
measurements; the eight baseline ratchets and build invariant remain the CI
regression suite. See [the command reference](usage.md).

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
put a dedicated checkout at `deps/cvc5`; the revision in `tools/cvc5.lock` is
the one for baseline checks. Ordinary analysis records the revision actually
read. Both analysis producers and `prompts/process_dokimasia` use the same
resolver, including a fallback to the legacy `tools/deps.local.json` cvc5 entry.
The environment now takes precedence in the reporting launcher too. If you
previously relied on `~/cvc5`, add it to the local map.

Check the setup and try a run before appending:

```bash
scripts/dokimasia_analyzer --dry-run
scripts/dokimasia_analyzer --no-update
scripts/append_findings scratch/new-bugs.json --dry-run
```

To update the database after reviewing that run, omit `--dry-run` from the last
command. `prompts/dokimasia_analyzer_agent` produces an independent dump;
the [analyzer guide](analyzer.md#an-independent-second-producer) covers comparison.

## Checks before handing off a change

```bash
for test in tests/test_*.py; do python3 "$test" || exit; done
python3 -m dokimasia check /path/to/pinned-cvc5 --verbose
for test in tests/test_*.py; do python3 "$test" /path/to/pinned-cvc5 || exit; done
scripts/append_findings --render-only --check
scripts/bump_anoieu --local /path/to/anoieu --offline --check
```

Use the revision in `tools/cvc5.lock` for the real-checkout tests. Do not move a
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
| `scripts/koine.py`, `scripts/koine.lock` | locate and verify the pinned database utility |
| `scripts/bug_reports.py` | local validation, archived evidence and Markdown rendering |
| `scripts/sweep_corpus` | run cvc5 over a corpus and record runtime counters |
| `scripts/audit_loc` | measure this repository's implementation and documentation |
| `scripts/bump_anoieu` | validate and update the pinned policy-checker revision |
| `prompts/dokimasia_analyzer_agent` | independent producer over the analyzer's targets |
| `prompts/check_dokimasia` | draft a response in the project owning a finding |
| `prompts/process_dokimasia` | process that reply here |
| `prompts/check_cvc5_issue` | examine a cvc5 issue and draft a response |

The assistant launchers previously lived in `scripts/prompts/`. Update local
aliases to the paths above. The reporting prompts still match their definitions
in `docs/workflows.md`; `tests/test_workflow.py` checks that agreement. The new
analyzer prompt is read directly from `prompts/analyzer.txt` and has no second copy.

## Pins and generated records

[`eo_bump.json`](../eo_bump.json) configures Koine's shared `eo_bump` to update
`scripts/koine.lock` only when the upstream `tests` check passes. From this
repository's root, use an installed `eo_bump`, or run it from a current Koine
checkout:

```bash
python3 ../koine/eo_cmd/eo_bump --show
python3 ../koine/eo_cmd/eo_bump --dry-run
python3 ../koine/eo_cmd/eo_bump
```

This maintenance command is provided separately from the pinned append utility;
the current database pin predates `eo_bump`. After a successful bump, refresh
the dedicated checkout as above and run the integration checks. A failed or
unknown upstream check leaves the pin unchanged. The configuration's `tests`
value names Koine's test job, which is the check name the current updater reads.

The policy-checker pin remains in `scripts/deps.lock`. The checker now lives at
`scripts/policy_check.py` in Anoieu. To validate and move the pin using an
existing clean checkout without contacting the remote:

```bash
scripts/bump_anoieu --local /path/to/anoieu --offline
```

Offline mode does not establish remote availability or remote CI status; those
remain separate from checking this tree against that revision. Ordinary online
mode still checks the tracked tip. Never change checks merely to get a green pin.
`eo_bump` currently handles plain-text pins and checks upstream CI; it does not
handle this JSON lock or run our compatibility check. Keep `bump_anoieu` until
those requirements are supported. The proposed shared work is recorded in
[discussion D6](discussion.md#d6--shared-dependency-and-database-mechanics).

Only `bugs.json` determines database membership. The generated page is a view,
and the content-addressed run archives preserve the source version, evidence
and original dump independently of scratch files. Do not hand-edit these to
resolve a triage disagreement. Keep that decision in the existing findings
register. See [the analyzer guide](analyzer.md) for identity, replay and conflict
semantics.
