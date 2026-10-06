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

## Reviewed outcomes

The original claims in `bugs.json` are preserved even when review rejects their
interpretation. Closure fields record an upstream fix; their absence does not
mean a claim is actionable. The [issue register](../docs/README.md#the-register)
holds the verdicts, and the generated [view](bugs.md#recorded-closures) now shows
recorded closures separately from the original observations.

| Observation | Reviewed outcome |
| --- | --- |
| `SIG0003` / `SUBS` | **Fixed.** [cvc5 #12948](https://github.com/cvc5/cvc5/pull/12948) documented the third argument. The database already carries the closure; [E9](../docs/experience.md#e9-cvc5-documented-the-argument-subss-checker-had-always-read) records the outcome. |
| `CI0002` / `explicit-completeness` | **Withdrawn check.** Safe-mode completeness is enabled implicitly; making the option explicitly settable would also allow disabling it. This is not an outstanding request to add the flag to CI. See [E10](../docs/experience.md#e10-cvc5-decided-to-keep-proof-completeness-checking-an-expert-option). |
| `MODE0001` / `macrosQuantMode` | **False positive as a reachable defect.** The controlling `macrosQuant` option defaults to false. The recorded defaults-only observation remains historical evidence; see `s-4` in the [settled register](../docs/README.md#settled). |

### Source assessment, 2026-10-06

Reviewed the subjects and changed paths of all **105 commits** from the archived
cvc5 revision `40a4bb7e43adf97534c29a52ed079c4efd687644` through upstream main
[`553db22e0ed4b9d2a52cf1fa6169415c99e3374b`](https://github.com/cvc5/cvc5/commit/553db22e0ed4b9d2a52cf1fa6169415c99e3374b),
then inspected relevant patches and the affected source at that revision.
No additional recorded observation met the upstream-fix closure criterion.
This was a source assessment, not a solver or proof-checker replay; it does not
refresh the original ingestion dates or the historical corpus measurements.

| Change or candidate | Assessment at that revision |
| --- | --- |
| Four `CI0004` job names | [#12906](https://github.com/cvc5/cvc5/pull/12906) renamed `production-dbg`, `production-dbg-clang`, `safe-mode`, and `stable-mode` to `unrestricted-dbg`, `unrestricted-dbg-clang`, `safe`, and `stable`. All four still exclude regression levels `3-4`. The old identities disappearing is not a fix. |
| `INFERID0001` / `SETS_RELS_TCLOSURE_FWD` and `SETS_RELS_TCLOSURE_UP` | [#12901](https://github.com/cvc5/cvc5/pull/12901) renamed `FWD` to `UP` and the old `UP` to `DOWN`. The production sites remain. In particular, the current `UP` name refers to the old `FWD` inference, so a matching name alone does not establish continuity. |
| `MODE0001` / `stringLazyPreproc` | Still defaults to true, declares no proof support, and has no direct safe-mode override. Resolve the annotation/default mismatch; no failing proof is established by this check. |
| `RW0002` / `LAMBDA_ELIM`; `SIG0002` / `SETS_CHOOSE` | Still candidates. The lambda rewrite is accepted by the printer only in unrestricted mode. The sets choose lemma still receives a null proof generator and its skolem is not handled by the Eunoia converter. Final-proof reachability still needs a reproducer (`i-1`, `i-24`). |
| String and arithmetic proof fixes | [#12969](https://github.com/cvc5/cvc5/pull/12969) adds string RARE rules; [#13020](https://github.com/cvc5/cvc5/pull/13020) repairs arithmetic reconstruction and a regexp fixed-point rewrite. Neither adds the missing string inference cases nor makes the recorded refused macro rewrites directly printable. These improvements do not close those broader observations. |
| `RW0001` / `MACRO_BV_MULT_SLT_MULT` | [#13042](https://github.com/cvc5/cvc5/pull/13042) fixes unsound applicability conditions in the underlying rewrite. The database claim concerns direct Eunoia handling, which is unchanged. Keep the soundness fix distinct from that observation. |
| Regression audit response | [#12973](https://github.com/cvc5/cvc5/pull/12973) cites this repo, documents exclusions, removes some disables, and repairs floating-point signature declarations. Recorded in [E16](../docs/experience.md#e16-cvc5-explained-proof-test-exclusions-and-removed-stale-disables); it closes no database row. In particular, the `SIG0002` / `FP_TO_REAL` skolem observation is not the `fp.to_real` declaration fix. |

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
archives the run, updates the database and refreshes `bugs.md` and the running
tally in [`docs/experience.md`](../docs/experience.md). The preview
writes nothing. Repeating a run adds no duplicate identities.

To analyze and record in one command, omit `--no-update` from the analyzer
command. Recording must succeed for that command to succeed. The independent
assistant producer uses the same format and append command; review its claims
before appending them.

## Refresh the generated view and tally

```bash
scripts/append_findings --render-only
scripts/append_findings --render-only --check
```

Rendering requires neither cvc5 nor Koine. CI runs the check and rejects a
stale view or tally. The view comes from `bugs.json`; the tally counts the
positive, negative and neutral episodes in `docs/experience.md`. Regenerate
after a database change or a new episode, and commit the corresponding generated
changes together with their source and any new run archives.

For a trial database, use `--db /path/to/bugs.json`. Archives and the default
Markdown view go beside it. `--page` overrides the view's location. A trial
database does not update the repository's experience log.

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
