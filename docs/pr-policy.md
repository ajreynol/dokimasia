# What we send, and what we build

*First draft. The rules below are applied today; the reasoning is still being
argued with, and the [open questions](#open-questions) at the end say where.*

**This repository never opens a pull request against cvc5. No program here
pushes a branch, opens an issue, posts a comment, or touches a tracker. A human
does that, or it does not happen.**

Hard rule, not a default — not conditional on how confident an analysis is or
how mechanical a fix looks. **But it is a rule about the *act*, not the
judgment.** Deciding what deserves to go upstream is this repository's job.

## Who decides what

| | owns | changes |
| --- | --- | --- |
| **standing guidance** — the goal, the ranks, the bar, the reporting promises | the maintainer | rarely, deliberately |
| **the verdict on each candidate** — worth someone's time, and ready | **this repository** | continuously, as evidence arrives |
| **the act of sending** — branch, PR, issue, comment | the maintainer | every time, by hand |

**dokimasia decides what is worthy, and records why.** Not a queue of
suggestions awaiting per-item approval: a maintainer re-deriving every verdict
would be doing the analysis twice, and throughput would collapse to one person's
attention — the bottleneck this repository exists to remove. Spot-checking the
verdicts is the review that matters, and [`next-report.md`](next-report.md) is
the standing decision record that makes it possible without reading everything.

The act stays with a person because somebody has to be accountable to the cvc5
maintainers for what arrives in their tracker, and that cannot be a program.

## The bar

Five rules, by name so they can be cited. A candidate is **worth carrying** only
when all five hold.

| rule | it means |
| --- | --- |
| **theirs-not-ours** | it is a defect in cvc5. A parser bug, a stale baseline or a bad assumption of ours is fixed here and logged, never reported |
| **run-it** | every claim about behaviour is backed by a command and its actual output. Static reasoning alone is a hypothesis |
| **cheap-to-refute** | the evidence is a command, a reproducer, or a named line — checkable in minutes, without us |
| **falsifiable** | we have said what would show it is wrong. A claim with no stated falsifier is not finished being thought about |
| **worth-the-attention** | it earns the time it costs. Cleanups are bundled and go *after* something substantive lands, never before |

## Three verdicts

Every candidate carries exactly one, and every one is recorded.

| verdict | means | lives in |
| --- | --- | --- |
| **carry** | all five hold; a person can take it upstream today | [`next-report.md`](next-report.md), with the packet |
| **not yet** | one or more fail — **name which** | [`issues.md`](issues.md), rank and blocking rule on the row |
| **never** | it is ours, or it will never earn the attention | [`issues.md`](issues.md#settled) or the retraction log |

*"Not yet"* is the verdict we issue most, and naming the failing rule is what
makes it actionable: it says exactly what work would change the answer.

## The bar is also a design constraint

This is the part that connects the policy to our own development, and it is the
half that was missing.

**Before building a check, ask what its output would be worth.** If everything a
check can produce would come back *not yet — worth-the-attention*, the check is
not worth building. That single question retires more work than any other test
we have, and it is why [`TODO.md`](../TODO.md) declines a SARIF framework, a
generated check registry, and a `holes/` corpus with no holes in it.

**Design every check with its verification path.** A check that can only ever
produce hypotheses fails **run-it** by construction, and will sit in the
register forever. This is why `dokimasia.latent` ships with
[`scripts/sweep_corpus`](../scripts/sweep_corpus): the static half alone could
never clear the bar, so the runtime half is not an extra, it is what makes the
analysis reportable at all.

**Let the failing rule set the queue.** A work item earns its place by moving a
candidate across the bar. `i-1` fails **run-it**, so *get an input for `i-1`* is
the first thing in the queue — not because lambdas are interesting, but because
that is the one move that changes its verdict.

**Fix at the source, not in the report.** When a candidate dies because we were
wrong, the deliverable is a corrected *analysis*, not a retraction. `SET_FILTER`
did not just get struck from the register; `Fragment.requires_higher_order` now
recovers the logic-level gate, so the whole class of mistake is gone. A
retraction with no code change behind it means the analysis will make the same
error again.

**Our own errors go through the same pipeline, inverted.** A false positive is
ours by promise, so it is filed against us: fixed, tested against the case that
produced it, and logged in [`findings.md`](findings.md#retractions). The
retraction log is the internal counterpart to the decision record.

## What the tools may do

| | |
| --- | --- |
| **may** | read a cvc5 checkout; compute; print; write files inside *this* repository |
| **may** | draft a patch, a reproducer, or a report **as a local artifact** |
| **may** | run an assistant in a cvc5 checkout that edits a working tree a person is driving |
| **never** | `git push`, `gh pr create`, `gh issue create`, or any network call to a tracker |
| **never** | commit to a cvc5 branch on its own initiative |

`scripts/check_dokimasia` and `scripts/check_cvc5_issue` make **no network
calls**: they build a prompt and hand it to an assistant working in a tree a
person is watching. Anything crossing between the repositories is carried by
that person.

## Why the bar names execution

Three things this repository produced, in order:

1. `SET_FILTER` is ungated in safe mode and its proof rules are refused by the
   seam, so a `set.filter` benchmark should fail `--check-proofs-complete`.
   Every link checked out in the source. **Wrong** — `set.filter` needs a
   function term, which needs higher-order logic, which safe mode refuses.
2. An ask reading *"pass `--check-proofs-complete` in the tester, one line."*
   **The flag cannot be passed there at all**: it is an expert option and safe
   mode rejects it. A one-line patch that does not compile as an instruction.
3. Baselines naming an `InferenceId` cvc5 has never had, which would have been
   reported as cvc5 drift.

Each read correctly in the source. Each was caught by running something — not by
review, and not by the analysis noticing its own error. **This repository is
capable of being confidently wrong three times in one sitting**, which is the
honest limit on how much weight its judgment carries, and the reason **run-it**
is not negotiable.

## The carry packet

What a person needs in order to act, and no more:

- the claim in one sentence, and its rank;
- the command that reproduces it, against a stated commit;
- the reproducer, where the claim is about behaviour — a `.smt2` file, the
  option set, the quoted output;
- what would falsify it;
- the patch as a diff in a file, never as a branch.

Carried by [`workflows.md`](workflows.md); what counts as a finding is
[`findings.md`](findings.md); the promise that a false positive is ours is
[`reporting-policy.md`](https://github.com/ajreynol/anoieu/blob/main/docs/reports/reporting-policy.md),
shared with anoieu.

## For an assistant working here

You may draft anything and run anything that reads. **You may not push, and you
may not open a PR or an issue — even when convenient, and even when a human
seems to have approved the underlying change.** Approval to *make* a change is
not approval to *send* it.

You are expected to **decide**. Apply the bar, write the verdict and the failing
rule, and say plainly what is worth carrying. Handing back an unranked list for
a human to sort is not neutrality — it is the work, left undone.

## Open questions

Named because this is a first draft and these are not settled.

- **What licenses a `never`.** *Worth-the-attention* is the only rule that is a
  judgement about someone else's priorities rather than about evidence, and we
  have no way to check it against what cvc5 actually wants. The cheapest fix is
  to stop guessing and ask.
- **Who reviews the verdicts, and how often.** Spot-checking is the stated
  control, but nothing sets a rate or says what a disagreement does to the rows
  already carried.
- **Whether a bundle needs its own verdict.** Cleanups defer individually and
  then travel together; the bundle is never assessed as the thing that actually
  costs attention.
- **What happens when a carried row is rejected upstream.** The workflow reads
  the answer back, but no rule says whether a rejection should change the bar or
  only the row.
