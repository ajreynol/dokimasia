# Maintaining dokimasia

Dokimasia owns analysis of cvc5's proof-production source and the evidence and
interpretation of its observations. Koine maintains the accumulated JSON list.
Kanon owns ecosystem policy; Anoieu implements the optional policy checker.

Keep commands and their helpers in `scripts/`, assistant launchers in `prompts/`,
and analysis implementations in `dokimasia/`. Add documents to the
[documentation index](README.md). The existing reporting workflow and its
human review boundary remain in [workflows.md](workflows.md).

Regression baselines live in `tests/baselines/<analysis>.json`; the runtime
census lives in `tests/corpus/reach-corpus.json`. Default paths resolve from the
repository location, so checks work from any working directory; baseline
`--file` and corpus-sweep `--out` accept overrides. Re-record baselines with
`python3 -m dokimasia write /path/to/cvc5` only after reviewing the change they
describe.

The analyzer and assistant default to the nine analyses in the README.
Standalone gates, fragment, TCB and latent reports are optional developer
measurements; the eight baseline ratchets and build invariant are the CI
regression suite. See [the command reference](usage.md).

Two documents are generated and neither is edited by hand:
[`fragment.md`](fragment.md), written whole by
`python3 -m dokimasia.fragment doc`, and
[`reports/static-analysis.md`](reports/static-analysis.md), written whole by
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
put a dedicated checkout at `deps/cvc5`; the revision in `tools/cvc5.lock` is
the one for baseline checks. Ordinary analysis records the revision actually
read. Both analysis producers and `prompts/process_dokimasia` use the same
resolver, in which the environment takes precedence and a `cvc5` entry in
`tools/deps.local.json` is the last fallback. No path is guessed: a checkout
this repository is not told about is not found.

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

Both generated documents are covered by that list: the observation page by
`append_findings --render-only --check`, and `fragment.md` by
`tests/test_fragment.py` when it is given the pinned checkout. Against any other
revision that one names itself as skipped rather than passing quietly, because a
diff taken elsewhere says nothing about drift.

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

Commands that run live in `scripts/`; launchers that spend a turn on an
assistant live in `prompts/`, so a reader can tell which is which without
opening a directory. The reporting prompts match their definitions in
`docs/workflows.md`, and `tests/test_workflow.py` checks that agreement. The
analyzer prompt is read directly from `prompts/analyzer.txt` and has no second
copy, so there is nothing there to drift.

## Pins and generated records

To update `scripts/koine.lock`, choose a full Koine commit SHA and inspect the
`tests` check on that exact commit in GitHub. Only replace the lock's SHA after
that check succeeds; a failed, unfinished or unavailable check leaves the pin
unchanged. Record the checked commit and CI result with the change.

Refresh the dedicated checkout using the commands under
[Local dependencies](#local-dependencies), then run the integration checks
before accepting the pin change. This pin selects the append utility and is
independent of the policy checker.

The policy-checker pin is `scripts/deps.lock`, and it names
`scripts/policy_check.py` in Anoieu. `scripts/bump_anoieu` is the one command
that moves it, and it moves it only onto a commit that passes **both** gates:
Anoieu's own CI was green at that commit, and the checker at that commit passes
against this tree.

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
[discussion D6](discussion.md#d6--shared-dependency-and-database-mechanics).

Only `bugs.json` determines database membership. The generated page is a view,
and the content-addressed run archives preserve the source version, evidence
and original dump independently of scratch files. Do not hand-edit these to
resolve a triage disagreement. Keep that decision in the existing findings
register. See [the analyzer guide](analyzer.md) for identity, replay and conflict
semantics.
