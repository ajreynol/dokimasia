# Maintaining dokimasia

Dokimasia owns analysis of cvc5's proof-production source and the evidence and
interpretation of its observations. Koine maintains the accumulated JSON list.
Kanon owns ecosystem policy; Anoieu implements the optional policy checker.

Keep commands and their helpers in `scripts/`, assistant launchers in `prompts/`,
and analysis implementations in `dokimasia/`. Add documents to the
[documentation index](README.md). The existing reporting workflow and its
human review boundary remain in [workflows.md](workflows.md).

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

The policy-checker pin remains in `scripts/deps.lock`. The checker now lives at
`scripts/policy_check.py` in Anoieu. To validate and move the pin using an
existing clean checkout without contacting the remote:

```bash
scripts/bump_anoieu --local /path/to/anoieu --offline
```

Offline mode does not establish remote availability or remote CI status; those
remain separate from checking this tree against that revision. Ordinary online
mode still checks the tracked tip. Never change checks merely to get a green pin.

Only `bugs.json` determines database membership. The generated page is a view,
and the content-addressed run archives preserve the source version, evidence
and original dump independently of scratch files. Do not hand-edit these to
resolve a triage disagreement. Keep that decision in the existing findings
register. See [the analyzer guide](analyzer.md) for identity, replay and conflict
semantics.
