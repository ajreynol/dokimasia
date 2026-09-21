# Dokimasia analyzer

This Python package contains thirteen static analyses of cvc5's proof-production
source. It reads a checkout without building cvc5. Nine analyses emit the
observations collected by `scripts/dokimasia_analyzer`; four provide additional
developer reports.

This page describes the modules and the standards for reviewing a finding.
For setup and commands, read `docs/maintenance.md`. The check catalogue and
issue register are in `docs/README.md`; interactions with cvc5 are recorded in
`docs/experience.md`. These paths are relative to the repository root.

## The modules

| module | answers |
| --- | --- |
| [`tcb`](tcb/) | the proof checker's dependency closure, and what each edge costs |
| [`ledger`](ledger/) | one row per `ProofRule`: produced, checked, elaborated, printed |
| [`trust`](trust/) | every `TrustId` construction site, and the preprocessing correspondence |
| [`inferid`](inferid/) | whether each `InferenceId` names one program point |
| [`infer`](infer/) | whether every inference a theory makes has a proof reconstruction |
| [`rewrites`](rewrites/) | the rewrite vocabulary, RARE vs hand-written vs applied |
| [`modes`](modes/) | what safe and stable mode change about the defaults |
| [`ci`](ci/) | whether cvc5's proof testing is still attached |
| [`signature`](signature/) | whether the Eunoia signature agrees with cvc5's account of a rule |
| [`gates`](gates/) | which option legalises each term kind, and so each rewrite rule |
| [`fragment`](fragment/) | the supported fragment per theory, and whether it is enforced |
| [`buildmode`](buildmode/) | is a safe *build* still an unrestricted build with one default flipped? |
| [`latent`](latent/) | the static inventory minus what a corpus reached |

Nine are advertised and emit observations; standalone `gates`, `fragment`,
`tcb` and `latent` reports are developer measurements that emit none.
[`findings.py`](findings.py) owns the check catalogue and the identity scheme;
[`sanity.py`](sanity.py) holds the expectations that make a scanner fail loudly
rather than return a confidently empty answer.

## What a finding is

An observation is a result from a check, stored with evidence in `bug_db/`.
A finding is a reviewed claim that meets the standards below. The issue
register in `docs/README.md` records candidates, settled claims and filed
findings.

| Kind | Purpose | Required outcome |
| --- | --- | --- |
| **A — defect** | identify an incomplete proof | an input and command that reproduce it |
| **B — adoption** | make a check part of cvc5's CI | a check and the configuration needed to run it |
| **C — pipeline change** | improve proof infrastructure or its contract | a supported argument for the change |
| **D — assertion** | enforce an invariant within cvc5 | a tested patch that can replace our external check |

Kind A directly serves the goal of complete proofs. The other kinds support
that goal. An assertion can expose a failure and retire an external check;
adding it does not by itself fix a proof gap.

## The promises

These are Dokimasia's review standards. Cite them by name. **Enforced** means a
mechanism rejects a violation; **structural** means the design helps prevent
it; **intention** means it depends on review.

| Position | Support | Mechanism or review obligation |
| --- | --- | --- |
| **Silence is never evidence** | structural | A clean run covers only the selected checks. The catalogue and archived evidence state each check's limitations. |
| **Publish a candidate; carry a finding** | structural | Raw observations stay in `bug_db/`; promoting a claim requires a separate review in the issue register. |
| **Presence is not reachability** | structural | A static gap needs runtime evidence before it is treated as a reachable defect. The corpus comparison in `docs/maintenance.md` measures that distinction. |
| **A false positive is ours — and so is anything we asked cvc5 to run** | enforced in part | Correct the analyzer and test the failure. Baseline checks detect changes in recorded results; review still has to establish whether a result is false. |
| **Every claim is re-checkable without us** | enforced for revision provenance | Measurements name their command and revision. [scripts/cvc5.lock](../scripts/cvc5.lock), `tests/test_pin.py` and CI check the baseline provenance. |
| **Closing is a verdict, not an absence** | enforced for the launcher | Database appends preserve observations. `tests/test_experience.py` checks that the closure prompt requires evidence and confirmation in current source. |
| **A reply is triage; an artifact settles it** | intention | Closing a defect requires a cvc5 change whose effect is confirmed in current source. A reply, commit message or missing row is insufficient. |

Two related standards govern the material we use:

- **Published is not available.** Reading a public tree does not remove our
  responsibility for the cost of a misleading analysis to its maintainers.
- **Unpublished work is not material.** This includes unreleased work on a
  public personal branch. Our qualification permits answering a question we
  are asked about our own registers; it does not permit an unsolicited exercise
  on somebody else's unreleased work. The reference lock records the historical
  use of a personal fork for the reachability census as a reproducibility debt.

Both are review obligations. Nothing crosses a repository boundary
automatically, and where cvc5 adopts an invariant, success can mean deleting
our external check.

## The bar

**A human decides what goes upstream.** No program here pushes a branch, opens
an issue or pull request, posts a comment, or touches a tracker.

A candidate is ready to take upstream only when it meets all five rules:

| Rule | Requirement |
| --- | --- |
| **theirs-not-ours** | The defect is in cvc5. Fix parser bugs, stale baselines and bad assumptions here. |
| **run-it** | Back every behavioural claim with a command and its actual output. |
| **cheap-to-refute** | Supply evidence someone can check in minutes without us. |
| **falsifiable** | State what would show the claim is wrong. |
| **worth-the-attention** | The benefit justifies a maintainer's time. Bundle cleanups after substantive work. |

Each candidate receives one verdict in the issue register:

- **carry** — all five rules hold; include the evidence needed to act.
- **not yet** — name the failing rule and the work needed to meet it.
- **never** — the problem is ours or will not justify upstream attention.

A carry packet contains the claim and its severity rank, the source revision,
a reproducing command and actual output, what would falsify the claim, and any
proposed patch as a diff file. A kind A defect also needs the `.smt2` input,
options and quoted `--check-proofs-complete` failure. The evidence required for
each rank is in `docs/maintenance.md`.

An assertion is proposed only after it has been applied to a cvc5 build with
`--assertions` and the regression suite passes. Until then it is a hypothesis.

## Designing a useful check

Before adding a check, identify both who can act on its output and how to
verify a result. For example, the static `latent` inventory ships with
[scripts/sweep_corpus](../scripts/sweep_corpus) so a corpus can establish which
listed gaps are reached.

When a check produces a false positive, fix the analysis and add a regression
case. `Fragment.requires_higher_order` and `Closure.edge_use` both grew out of
such corrections. If cvc5 caught the mistake, record the interaction in
`docs/experience.md` as well.

## Answering a maintainer's question

A case study answers a specific question about cvc5. Its useful output is a
checkable invariant with a verifier and tests demonstrating that the verifier
can fail.

1. Use the requester's question as the title and describe the existing decision
   accurately.
2. State the invariant the answer depends on and enumerate the relevant sites.
3. Explain exceptions, uncertainties and what was not checked.
4. Supply the verifier and tests that exercise its failure cases.
5. Give a verdict against the five rules above, including a falsifier.

A case study may produce a finding, which then gets its own register entry.
It does not automatically recommend changing the decision that prompted it.

## What a run learned about itself

This section records lessons about the analyzer from reviewing cvc5 history,
newest first. Interactions with cvc5 belong in `docs/experience.md`.

**2026-09-19, window `40a4bb7e4..dbf176dfb`.**


- **The `ci` check's mode heuristic broke silently on a cvc5 rename.**
  `Job.mode` in `dokimasia_analyzer/ci/scan.py` keys on the literal substrings
  `safe-mode` / `stable-mode` in a matrix `config:` value; cvc5 #12899 renamed
  those values to `safe` / `stable`. The safe-mode job is still there and still
  runs `--tester proof`, but the check now classifies every job `unrestricted`,
  which silently disarms `CI0001` and makes two links of the `CI0002` chain read
  `NO` for a reason that has nothing to do with cvc5. **A check keyed on a
  spelling cvc5 is free to change will fail open, and this one did.**
- **Two of the window's four candidate closures were entity renames.** cvc5
  #12906 renamed the CI job names carrying all four `CI0004` rows, and #12901
  renamed the `InferenceId` carrying an `INFERID0001` row — in both cases the
  condition moved intact under a new name. A re-run will read both as
  disappearances. *Absence closes nothing* is the rule that caught this; what it
  cost was re-deriving each claim by hand, because nothing in the record links
  an identity to its renamed successor.
- **A claim about cvc5's history stopped being true.** Our baselines once
  named `SETS_RELS_TCLOSURE_DOWN`, and the correction said **no such id has ever
  existed in cvc5**. True when written; as of cvc5 #12901 the id exists, because
  cvc5 renamed `TCLOSURE_UP` to it. A statement of the form *cvc5 has never had
  X* is a claim about a moving tree and needs the date it was checked at.
