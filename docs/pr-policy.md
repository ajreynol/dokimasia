# We do not open pull requests

**This repository never opens a pull request against cvc5, and never will. No
program here pushes a branch, opens an issue, posts a comment, or touches a
tracker. A human does that, or it does not happen.**

That is a hard rule, not a default, and it is not conditional on how confident
an analysis is or how mechanical a fix looks.

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
reads a bad finding has lost the time either way; the asymmetry is that we can
generate them far faster than anyone can refute them. Volume is the failure mode
of an automated analysis pointed at somebody else's project, and the rate limit
that matters is a human deciding each one is worth sending.

This session is the argument. Three things it produced, in order:

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

Each was caught before it left this repository, by a person's process rather
than by the analysis noticing its own error. An automated PR path would have
shipped all three.

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
If you believe something should go upstream, write the carry packet and say so.
