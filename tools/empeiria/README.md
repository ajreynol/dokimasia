# empeiria

*What does a maintainer's answer teach that the issue text did not?*

**Internal.** A research project under
[anoieu's research-project rules](https://github.com/ajreynol/anoieu/blob/main/docs/policy.md),
not a project announcement. It is not linked from the root
[`README`](../../README.md), from [`docs/README.md`](../../docs/README.md), or
from either register ([`TODO.md`](../../TODO.md),
[`docs/issues.md`](../../docs/issues.md)), and it should stay that way until
there is something to show. `ajreynol/dokimasia` is a **public** remote:
unadvertised means *not pointed at*, not *not visible*. Nothing here makes a
claim about cvc5 or should be quoted as though it did.

**Read-only island.** empeiria reads dokimasia's analyses, cvc5's tree, and its
own ledger. Nothing in `dokimasia/` imports it, no test covers it, no baseline
ratchets it, no CI job runs it, and it ships no code today. Delete this
directory and the repository is exactly as functional — that is the property
that makes it safe to keep here.

## On the name

**ἐμπειρία** — *experience*: the knowledge that comes from many particular
cases rather than from being taught. Aristotle puts it exactly this way in
*Metaphysics* A.1 — memory of many instances of the same thing produces a single
experience — and that is the mechanism this project is about. It does not learn
by being given a rule; it learns by accumulating what maintainers actually did
with particular issues.

*mathesis* (learning by instruction) was the other candidate and is the wrong
one: nobody is teaching this project a rule. If it turns out that a written rule
would have worked all along, the name is wrong and that is itself the finding.

## The charter

**The question.** cvc5's issue tracker receives bug reports that a maintainer
triages, reproduces, delvers or closes. Almost none of them are proof-completeness
bugs, so almost none are dokimasia's. **Is there a front end that gets better at
addressing them by learning from how a maintainer answered the last ones?**

**The goals, in order.**

1. **Record what a response taught.** For each issue worked, capture the triage
   an assistant produced, what the maintainer actually did, and the delta. The
   delta is the whole asset; everything else is bookkeeping.
2. **Find the recurring shapes.** Across enough deltas, whether the corrections
   fall into a small number of kinds — wrong subsystem, wrong severity, already
   known, not a bug, missing a reproducer step.
3. **Make the next triage better,** and say by how much against a held-out set.
   An improvement nobody measured did not happen.

**The stretch goal.** A front end that reads a fresh cvc5 issue and produces a
triage a maintainer would not have to redo — measured against what they did, not
against whether it reads well.

**Out of scope**, explicitly, because a research project with no boundary
becomes a second tool:

- **Proof-completeness bugs.** Those are dokimasia's, and they stay in
  [`docs/issues.md`](../../docs/issues.md). If an issue turns out to be one, it
  leaves here and enters the parent's register.
- **Fixing cvc5.** This studies the triage loop; it does not patch the solver.
- **Anything sent upstream.** Rule 7 and the parent's
  [`pr-policy.md`](../../docs/pr-policy.md): nothing leaves the island by
  machine, there is no separate channel and no lighter standard. The ledger
  accumulates candidates; a person decides if any is carried.
- **Speaking for dokimasia.** Nothing here is the parent's position on anything.
- **Building a general bug-triage product.** The subject is cvc5's tracker and
  what one maintainer's answers teach, not triage in the abstract.

**Is there a paper in it?** Not yet, and probably not for a while. There is a
paper only if goal 3 produces a measured improvement against a held-out set of
issues; a project that has learned nothing measurable has nothing to write up,
and saying so now is cheaper than discovering it later.

## What it inherits from dokimasia, and where

Rule 8 — a research project runs inside a working tool's repository because that
tool has evidence, and it must cite what it takes.

| inherited | where it was established |
| --- | --- |
| the workflow that runs an assistant against a cvc5 issue and writes a `TRIAGE:` / `HUMAN RESPONSE:` block | [`scripts/check_cvc5_issue`](../../scripts/check_cvc5_issue), [`docs/workflows.md`](../../docs/workflows.md) |
| that a reply is triage and only an artifact settles anything | [`docs/findings.md`](../../docs/findings.md) |
| that a claim about behaviour is worthless until it has been run | [`docs/pr-policy.md`](../../docs/pr-policy.md) — three static arguments that read correctly and were false |
| the postmortem shape — one block per round, about the workflow rather than the subject | [`docs/postmortem.md`](../../docs/postmortem.md) |

The reason this is a child of dokimasia rather than its own repository is that
last row: the parent already runs the loop, already writes the block, and has
already learned things about it that would otherwise be re-learned.

## Status

**Started 2026-09-01**, by an explicit human instruction (rule 1), on the
occasion of cvc5
[#12905](https://github.com/cvc5/cvc5/issues/12905) — a fatal failure in
`theory_engine.cpp` on a strings-and-quantifiers benchmark, which is a theory
explanation defect and **not** a proof bug, and so is the first concrete case of
an issue this repository cannot take and should not ignore. The routing question
it raised is written up in
[`docs/cases/`](../../docs/cases/out-of-scope-bug-report.md).

Nothing has been built. There is no ledger yet, no case worked, and no result.
Rule 9 applies: this ends by graduating, being folded in, or being retired in
place with a note saying what was learned — and going quiet is not one of the
three.
