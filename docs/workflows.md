# A suggested AI workflow for using dokimasia

How to work a single candidate with an assistant, from [`issues.md`](issues.md)
to whoever can settle it and back.

**Little of this is ours to state.** The position — what may be published about
somebody else's code at all — is
[`reporting-policy.md`](https://github.com/ajreynol/anoieu/blob/main/docs/reports/reporting-policy.md),
shared with anoieu outright and naming this repository as a dependent. The mechanics that
implement it — what an agent following up a reply may change, the shape a reply
takes — are the conventions in
[`reporting-workflow.md`](https://github.com/ajreynol/anoieu/blob/main/docs/reports/reporting-workflow.md#the-conventions),
written to transfer. Both govern this repository, and neither is restated here.

What follows is the remainder: which of our files fill the policy's slots, what
settles a row here, where we diverge, and the two prompts. It assumes an expert
— somebody who knows the C++ being looked at, which is the audience
`reporting-policy.md` says these tools are for.

## The slots

| the slot | dokimasia's |
| --- | --- |
| **the report** | [`issues.md`](issues.md) — curated by hand, ranked, with *what would settle it* against every open row |
| **the id** | the `i-N` of the row, assigned by hand and stable across edits elsewhere in the file |
| **the catalogue** | the analyses table in [`README.md`](../README.md), and the *found by* column naming the command that produced the row |
| **re-measuring** | point the command at a cvc5 checkout at the commit the README names |
| **the regression** | `tests/test_*.py` and the `*-baseline.json` beside them |
| **the ledger** | [`findings.md`](findings.md) for what was filed and what was retracted; `upstream.md` for the history of a reply, as soon as there is one |
| **the frame** | `TRIAGE:` and `HUMAN RESPONSE:`, exactly as the policy defines them |

Closing, here, is **moving a row to *Settled*** with what settled it, or to
*Filed* if it became a finding. Both tables are already in `issues.md`.

Two slots are weak, and are a separate job rather than a caveat: nothing
restores the cvc5 commit a row was measured against ([`TODO.md`](../TODO.md)'s
`M0.5` and `A.3`), and a hand-written row has no fingerprint anybody can
reproduce — so the policy's *do not add a row by hand* is the one convention
that does not yet bind. *Every claim is re-checkable without us* is the position
behind both, and the one we are furthest from keeping.

## What settles a row

*A reply is triage; an artifact settles it* leaves each tool to name its own
artifact, and ours is usually an input: a `.smt2` file, its options, and what
`--check-proofs-complete` says settles a reachability row outright, where no
argument from the code can. A question about a stale annotation is settled by a
maintainer's sentence, and a coupling by a merged change. The half worth
repeating is the negative one — **nobody finding an input settles nothing**, and
the row stays open.

## Where we diverge

Two things, both departures from the policy's mechanics rather than from the
position, and named here because the second prompt depends on them.

**A row may be a question rather than a defect report.** `i-2` asks whether an
annotation is stale. So the triage line carries a fourth label, `answered`,
which anoieu's does not, and such a reply names no branch.

**Not every row names a file and a line.** Some name a mechanism — an option
that escapes a promise, a fragment no list of kinds can express.

## Prompt one: in cvc5

Fixed text; the id and the branch are the only things that change.
[`scripts/prompts/check_dokimasia`](../scripts/prompts/check_dokimasia) runs it
in a cvc5 checkout and fills both in. Where the script and this document disagree, this
document is right.

```text
dokimasia is a static analyzer for the proof-production code of cvc5. It asks
whether a path through the solver can produce no proof at all. It has reported
something against this project. The report is at

  https://github.com/ajreynol/dokimasia/blob/main/docs/issues.md

Start there: it says what a row is, what the "found by" column names, and what
each row would take to settle.

Find the row whose id is ID, and address that row only.
-- or, for the sweep form --
Address every open row. Work from the ids; the file is curated by hand and rows
move. Rows may share a cause -- say so, and still rule on each in its own
block. Answering ten rows with one sentence is not doing this.

A row names what we believe and the command that produced it; the analysis that
command belongs to is described in the table at the top of that repository's
README. Some rows name a file and a line, others a mechanism and no single
site. Treat a row as a claim about this project and nothing more: it does not
tell you what kind of problem to expect, and you should not assume one. Its
"what would settle it" column says what we are asking for, and sometimes that
is an answer rather than a change.

Work on branch BRANCH, creating it if it is not there. Commit to it locally and
push nothing -- pushing, and any pull request, are the maintainer's. An
uncommitted change is not a fix; the commit is what dokimasia reads. Keep
dokimasia-response.md out of it: the reply is for us, not for your history.

One row at a time, and only what the rows name:

1. Decide whether the claim is true by reading the code, not by trusting the
   row. Some of what dokimasia reports is wrong, and one of its headline
   numbers has already been retracted. Say which build you ran, if you ran one.
2. If it is true and it is a defect, make the smallest change that fixes it,
   and say in one sentence what a reader of that code would see differently.
3. If the row asks a question, answer it. An answer with a reason is a complete
   outcome and needs no change to any file.
4. If the claim is that some path can produce no proof, say what you know about
   whether that path is reachable. An input that reaches it -- a .smt2 file,
   the options it needs, and what --check-proofs-complete says -- settles the
   row outright. Not finding one settles nothing, and should be reported as
   what it is.
5. If the claim is not true, or you cannot tell, change nothing and say why. "I
   cannot tell" is the honest answer when you do not already know what that
   code was meant to guarantee, and it is more useful than a guess.

Do not fix other things you notice on the way; each is reported separately. Do
not summarize the analyzer's other results anywhere: a check that reports
nothing is not evidence that anything is complete. Touch no issue tracker --
not ours, not yours, not anybody's. Everything that reaches a person who did
not ask for it is sent by a person.

Then draft a reply for a maintainer of this project to review and send, in
dokimasia-response.md at the repository root, appending and leaving any block
already there. One per row:

  ## ID -- <what the row claims> -- <where, if the row names a site>

  TRIAGE: fixed | not a defect | answered | cannot tell, on branch BRANCH -- or
  with no branch, if nothing was changed -- pending review. <What you changed,
  what you answered, or why you changed nothing.>

  OBSERVED, NOT ACTED ON: <optional -- anything true you found and left alone.>

  HUMAN RESPONSE:

It is your triage and not a resolution: you are proposing something nobody has
reviewed, and what happened will be settled by the branch, by an input, or by a
maintainer's word.

Leave HUMAN RESPONSE: empty. It is the maintainer's, and the two labels exist
to keep what you concluded apart from what a person decided. If they ask you to
write it instead, do -- but then quote the field back to them exactly, the text
itself and not a description of it, say plainly that you are writing in their
place and it will be read under their name, and change it as many times as they
ask until they say it says what they mean. Writing that field and summarising
it back is the one thing this shape exists to prevent.

End with two sections. FEEDBACK TO DOKIMASIA: blunt is useful -- where the time
went and what would have made it fast; what a row should have carried, and
anything here that was unclear or untrue; what else is worth looking for that
dokimasia does not do.

Then WHAT THIS NEEDS FROM YOU: name BRANCH, say nothing is pushed, and say
dokimasia sees none of this until somebody pushes it and sends back where to
look. A merge is not needed to settle a row; a branch somebody can fetch is.
Then list every row you are declining and ask them to confirm each -- not
fixing something is a decision somebody signs, silence is not a signature, and
unconfirmed it is reported as "cannot tell".
```

## Prompt two: the follow-up, here

For an assistant working in a checkout of **dokimasia**.
[`scripts/prompts/process_dokimasia`](../scripts/prompts/process_dokimasia) runs
it here. This
document is written around a link — to the branch, the pull request, or wherever
the triage was written down — and the script around a checkout it has already
resolved. Below the opening the text is the same, and where it is not, this
document is right.

```text
A project we reported something to has responded:

  LINK

Read it as two things. What follows TRIAGE: is an assistant's reading, made
quickly and on our word. What follows HUMAN RESPONSE: is a maintainer's
decision. Where the two differ the decision is what counts, and a reply
carrying only a triage is a proposal rather than a result.

Process the block about ID and only that one; leave any others alone.
-- or, for every block --
Process every block in it, one at a time, leaving the record consistent after
each so that stopping partway is safe. Blocks may share a cause; each still
gets its own answer.

Working in the dokimasia repository:

1. Find the row or rows in docs/issues.md that the reply is about, by id. A row
   is in scope because the reply names it, open or not -- a reply disputing a
   verdict names a row that was already settled.
2. Establish what actually happened, which is not what the triage predicted.
   Re-run the command the row's "found by" column names against a cvc5 checkout
   at the commit the README says the numbers were measured at -- and say so if
   you cannot get that commit, rather than quietly measuring a different one.
   Then follow whatever the reply points to: a branch, to its end (merged,
   reworked, reverted, still open), or an input, by running it. Look at the
   branch rather than taking it -- a branch level with main, or a change left
   uncommitted, is not a fix. That outcome counts, not what the triage
   predicted.
3. Move only the rows the reply is about, as
   https://github.com/ajreynol/anoieu/blob/main/docs/reports/reporting-workflow.md#the-conventions
   says. A settled row moves to the Settled table with what settled it; a row
   that became a finding moves to Filed. Rows move and are never deleted, and a
   row the reply is silent about is not touched, reworded or re-sorted.
4. If our analysis was wrong, the check is what needs changing rather than the
   row: narrow it, add the case that would have caught the mistake to tests/
   and to that tool's baseline JSON, and record what we had wrongly assumed
   under Retractions in docs/findings.md.
5. Write what happened in `docs/upstream.md`, creating it if this is the first
   entry.
6. Read FEEDBACK TO DOKIMASIA and any OBSERVED, NOT ACTED ON. Act on what
   concerns the report or the checks. What concerns the prompts goes to
   docs/postmortem.md with its evidence and then to me: a person approves every
   prompt edit, and each round should leave them shorter and more procedural,
   so a proposal that adds says what it removes, and technical detail belongs
   in the documents a prompt links to rather than in the prompt.

7. Write a postmortem entry for this run, whether or not anything changed.
-- or, with --no-postm --
7. Decide whether this earned a postmortem entry. It did if handling the reply
   changed how dokimasia works -- a check, the report, a prompt. If nothing
   here changed, say so and write nothing.

   Entries go at the top of docs/postmortem.md, in the shape that file sets out
   -- short, and only what happened and what the workflow learned; the
   reasoning at length belongs in `docs/upstream.md`. Update "Where the
   workflow stands" in the same file if this round changed what is outstanding.

Leave everything staged, and commit nothing -- the diff is the review, and it
is somebody else's to approve. Touch no issue tracker, here or anywhere. Say
what you decided and why: the action you took, not a summary of what you read.
Come back to me only if you disagree with how the reply classified the
resolution, or you cannot tell whether the row is settled; leave the row where
it is and say what you would need to know.
```

### Keeping them in step

The first prompt's output is the second's input, and the shape they share is
defined in another repository — so a change to it lands in three places across
two repos, all of them or none — which the policy now says in its own words.
Anything this workflow grows that the policy does not have goes under *Where we
diverge* above; a divergence nobody wrote down is drift, and an agent reading a
format nobody produces will improvise rather than stop.

The scripts hold a copy of both prompts so that nobody has to paste one, and a
copy that has drifted is worse than no copy: the drift is invisible from the
side that matters, which is somebody in cvc5 reading a prompt they were sent.
[`tests/test_workflow.py`](../tests/test_workflow.py) compares what each script
prints under `--show-prompt` against the blocks above, in every form either can
take, and fails when they disagree. The two lines each script fills in — the
scope and the branch — are what the scripts are *for*, and are the only thing
the comparison lets differ.

### The postmortem

Step 7 writes to [`postmortem.md`](postmortem.md): what a round of this taught
us about the workflow, as opposed to what it settled about cvc5. The second
belongs in `docs/upstream.md`, and the separation is anoieu's — the two files
answer different questions, and a log that answers both answers neither.

## Not yet

The report is curated by hand and the re-measure is manual. The shared reporting
infrastructure — a generated report, reproducible ids, one command that restores
the versions — is designed separately; when it lands, the slot table here and
the URL in prompt one change together.

Issues on our own tracker are anoieu's
[arrangement](https://github.com/ajreynol/anoieu/blob/main/docs/reports/reporting-workflow.md#medium-term-issues-on-our-own-repository)
under *nothing crosses a repository boundary automatically*, and we follow both
rather than restate them. One line is ours to draw, and
[`findings.md`](findings.md) draws it: that asymmetry is about **candidates**. A confirmed kind-A finding — an
input, an option set, a quoted `--check-proofs-complete` failure — is an
ordinary bug report, belongs in cvc5's tracker, and is filed there by the human
who confirmed it.
