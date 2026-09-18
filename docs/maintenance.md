# Maintaining dokimasia

Dokimasia owns analysis of cvc5's proof-production source and its
[`bug_db/`](../bug_db/README.md) data artifact: records, evidence, triage and
closure decisions. Koine maintains the shared database writer.
Kanon owns ecosystem policy; Anoieu implements the optional policy checker.

General cvc5 development belongs to
[Paideia](https://github.com/ajreynol/paideia), whose charters, plans,
protocols, launchers and ledgers are authoritative for it. This tree carries no
child project, so there is no `tools/`; the cvc5 baseline pin sits at
`scripts/cvc5.lock` alongside the other dependency pins. Proof-production
performance belongs to
[Tachyon's Elaphros](https://github.com/ajreynol/tachyon/tree/main/tools/elaphros)
and is outside Dokimasia's scope.

Keep commands and their helpers in `scripts/`, assistant launchers in `prompts/`,
and analysis implementations in `dokimasia/`. Add documents to the
[documentation index](README.md). The reporting workflow is
[deprecated](workflows.md); existing records and launchers remain available
while its [replacement](#replace-the-deprecated-reporting-workflow) is pending.

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
[`bug_db/bugs.md`](../bug_db/bugs.md), written whole by
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
read. Both analysis producers and `prompts/process_dokimasia` use the same
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
| `scripts/koine.py`, `scripts/koine.lock` | locate and verify the pinned database utility |
| `scripts/bug_reports.py` | local validation, archived evidence and Markdown rendering |
| `scripts/sweep_corpus` | run cvc5 over a corpus and record runtime counters |
| `scripts/audit_loc` | measure this repository's implementation and documentation |
| `scripts/bump_anoieu` | validate and update the pinned policy-checker revision |
| `prompts/dokimasia_analyzer_agent` | independent producer over the analyzer's targets |
| `prompts/check_dokimasia` | legacy reporting: draft a response in the project owning a finding |
| `prompts/process_dokimasia` | legacy reporting: process that reply here |
| `prompts/check_cvc5_issue` | legacy reporting: examine a cvc5 issue and draft a response |

Commands that run live in `scripts/`; launchers that spend a turn on an
assistant live in `prompts/`, so a reader can tell which is which without
opening a directory. The reporting prompts match their definitions in
`docs/workflows.md`, and `tests/test_workflow.py` checks that agreement. The
analyzer prompt is read directly from `prompts/analyzer.txt` and has no second
copy, so there is nothing there to drift.

## Pins and generated records

The Koine pin is `8efe59ca20b5d684d8d00fce330b6a6968444493`; its upstream
[`tests` check](https://github.com/ajreynol/koine/actions/runs/35383263886/job/105724207417)
completed successfully on 2026-09-18. This revision uses
`bug_db_manager/koine_append_db` and locks the database itself. Dokimasia already
holds that same lock while archiving, appending and rendering, so it invokes
Koine with `--no-lock` inside the locked section.

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
[discussion D6](discussion.md#d6--shared-dependency-and-database-mechanics).

Only `bugs.json` determines database membership. The generated page is a view,
and the content-addressed run archives preserve the source version, evidence
and original dump independently of scratch files. Do not hand-edit these to
resolve a triage disagreement. Keep that decision in the existing findings
register. See [the analyzer guide](analyzer.md) for identity, replay and conflict
semantics.

## Replace the deprecated reporting workflow

**Pending, recorded 2026-09-18.** Following Anoieu, the
[reporting workflow](workflows.md) and [reporting policy](pr-policy.md) are
deprecated. Replace them with a formal reporting lifecycle using
[Koine's shared tooling](https://github.com/ajreynol/koine/tree/main/bug_db_manager).
Koine supplies storage and update mechanics; Dokimasia owns its findings and
the evidence required for decisions about them.

The storage migration is complete: `bug_db/bugs.json`, `bug_db/bugs.md` and
`bug_db/runs/` hold the data, generated browsing view and archived evidence.
Existing records and dates are preserved, and both analysis producers use the
same append path. This does not migrate reviewed verdicts or implement closure.

Remaining work:

- Define the evidence and decision rules for triage, correction, reporting,
  closure and reopening, including how static observations become confirmed
  behavioral findings.
- Specify the shared Koine capabilities needed to preserve original findings,
  dates, claims, corrections and decision evidence. The append utility alone
  cannot perform this lifecycle.
- Assess closure only from successful, comparable runs that covered the relevant
  input and check. Use recorded source and analyzer versions, enabled analyses,
  actual coverage, skips and failures. An unmatched or changed identity needs
  an explicit assessment; disappearance from a dump cannot close a finding.
- Migrate the reviewed issue register, filed findings, replies and retractions
  without losing their meaning or history, then replace the legacy launchers
  and update their documentation and checks.

Until then, preserve decisions in [`issues.md`](issues.md) and
[`findings.md`](findings.md). Existing launchers remain usable during the
transition. Deprecation neither settles existing claims nor authorizes automatic
publication; upstream reporting remains a maintainer action.
