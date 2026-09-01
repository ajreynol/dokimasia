# We do not open pull requests

**This repository never opens a pull request against cvc5, and never will. No
program here pushes a branch, opens an issue, posts a comment, or touches a
tracker. A human does that, or it does not happen.**

That is a hard rule, not a default, and it is not conditional on how confident
an analysis is or how mechanical a fix looks.

**It is a rule about the *act*, not about the judgment.** Deciding what deserves
to go upstream is this repository's job; putting it there is a person's. Those
are different things and the next section separates them, because conflating
them produced a worse version of both.

## Who decides what

| | owns | changes |
| --- | --- | --- |
| **standing guidance** — the goal, the ranks, the bar below, the reporting promises | the human maintainer | rarely, and deliberately |
| **the verdict on each candidate** — is this worth someone's time, and is it ready | **this repository** | continuously, as evidence arrives |
| **the act of sending** — the branch, the PR, the issue, the comment | the human maintainer | every time, by hand |

The middle row is the change worth stating plainly: **dokimasia decides what is
worthy, and records why.** It is not a queue of suggestions awaiting per-item
approval. A maintainer who had to re-derive every verdict would be doing the
analysis twice, and the throughput of the whole thing would be one person's
attention — which is the bottleneck this repository exists to remove.

What the maintainer keeps is the guidance and the act. Guidance is how the
judgment gets steered; the act is where a human is unavoidably accountable for
what lands in somebody else's project. Spot-checking the verdicts is the review
that matters, and [`next-report.md`](next-report.md) exists so that is possible
without reading everything: it is the standing decision record, with reasons.

## The bar this repository applies

If nobody is filtering per item, the filter has to be written down and it has to
be strict. A candidate is **worth carrying** only when all of these hold:

1. **It is about cvc5, not about us.** A parser bug, a stale baseline or a bad
   assumption of ours is fixed here and logged, never reported.
2. **It has been run, not only read.** Every claim about behaviour is backed by
   a command and its actual output. Static reasoning alone is a hypothesis, and
   hypotheses stay in [`issues.md`](issues.md).
3. **A maintainer can refute it cheaply.** The evidence is a command, a
   reproducer, or a named line — something checkable in minutes without us.
4. **We have said what would falsify it.** A claim with no stated falsifier is
   not finished being thought about.
5. **It is worth the attention it costs.** Volume is the failure mode of an
   automated analysis pointed at someone else's project. A cleanup that is
   individually harmless still spends credit, so cleanups are bundled and go
   *after* something substantive lands, never before.

Anything failing one of these is **not yet**, and the register says which one it
failed. That is a verdict too, and it is the one we issue most.

## What the tools may do

| | |
| --- | --- |
| **may** | read a cvc5 checkout; compute; print; write files inside *this* repository |
| **may** | draft a patch, a reproducer, or a report **as a local artifact**, for a person to read |
| **may** | run an assistant in a cvc5 checkout that edits a working tree the person is driving |
| **never** | `git push`, `gh pr create`, `gh issue create`, or any network call to a tracker |
| **never** | commit to a cvc5 branch on its own initiative |

`scripts/check_dokimasia` and `scripts/check_cvc5_issue` run assistants inside a
cvc5 checkout. They make **no network calls**: they build a prompt, hand it to an
assistant, and the assistant works in a tree a person is watching. Anything that
crosses between the two repositories is carried by that person.

## Why

**Because the cost of a wrong report is paid by someone else.** A maintainer who
reads a bad finding has lost the time either way, and we can generate them far
faster than anyone can refute them.

The rate limit that matters is therefore the bar's demand that **nothing about
behaviour is claimed until it has been run.** Three things this repository
produced, in order, are the argument for it:

1. A confident static chain — `SET_FILTER` is ungated in safe mode, its proof
   rules are refused by the seam unless unrestricted, so a `set.filter`
   benchmark should fail `--check-proofs-complete`. Every link checked out in
   the source. **It is wrong**: `set.filter` needs a function term, function
   terms need higher-order logic, and safe mode refuses it. One command showed
   that; no amount of reading would have.
2. An ask, `R2`, that read *"pass `--check-proofs-complete` in the tester, it
   costs one line."* **The flag cannot be passed there at all** — it is an expert
   option and safe mode rejects it. We had proposed a one-line patch that does
   not compile as an instruction.
3. Baselines naming an `InferenceId` cvc5 has never had, which would have been
   reported as cvc5 drift.

Every one read correctly in the source, and every one was caught by running
something — not by review, and not by the analysis noticing its own error. That
is why the bar names execution specifically. It is also the honest limit on how
much weight the judgment above can carry: this repository is capable of being
confidently wrong three times in one sitting, and the only thing that reliably
caught it was a command.

The act stays with a person for a different reason: not because the judgment
needs a second opinion, but because somebody has to be accountable to the cvc5
maintainers for what arrives in their tracker, and that cannot be a program.

## What we produce instead

A **carry packet**, which is what a person needs in order to decide, and no
more:

- the claim, in one sentence, and the rank it is filed at;
- the command that reproduces it, against a stated commit;
- the reproducer where the claim is about behaviour — a `.smt2` file, the option
  set, and the quoted output;
- what would falsify it;
- the patch as a diff in a file, if there is one, never as a branch.

The workflow that carries it, and reads the answer back, is
[`workflows.md`](workflows.md). What counts as a finding at all is
[`findings.md`](findings.md). The promise that a false positive is ours is
[`reporting-policy.md`](https://github.com/ajreynol/anoieu/blob/main/docs/reports/reporting-policy.md),
shared with anoieu.

## For an assistant working in this repository

If you are an agent reading this: you may draft anything and you may run
anything that reads. **You may not push, and you may not open a PR or an issue,
even when explicitly convenient and even when a human seems to have approved the
underlying change.** Approval to *make* a change is not approval to *send* it.

You are, however, expected to *decide*. Apply the bar above, write the verdict
and the reason into [`next-report.md`](next-report.md), and say plainly what you
think is worth carrying and what is not. Handing back an unranked list of
candidates for a human to sort is not neutrality — it is the work, left undone.
