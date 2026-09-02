# Postmortem log

A living log of what working a reply has taught dokimasia about **its own
workflow**. One section per **run** — one reply worked — with what changed here
listed under it: a check narrowed, the report reshaped, a prompt rewritten.
Newest first.

**This is not where a reply is written up.** That is `docs/upstream.md`, which
carries the reasoning, the commits and the evidence at whatever length they
need. Entries here are short and point there. The two files answer different
questions: *what happened to this row* is the log in `docs/upstream.md`; *what
this run taught us about working rows* is here.

The separation is anoieu's, and so is the shape below.

## The procedure

**Whose job.** Whoever processes a reply here — step 7 of prompt two in
[`workflows.md`](workflows.md#prompt-two-the-follow-up-here), which is what
[`scripts/prompts/process_dokimasia`](../scripts/prompts/process_dokimasia)
runs. Not cvc5:
they send feedback, and what it changed on this side is ours to decide.

**When.** Every run, by default.

    scripts/prompts/process_dokimasia [DIR] [ID]              # an entry is written
    scripts/prompts/process_dokimasia --no-postm [DIR] [ID]   # the agent decides

`--no-postm` asks for a test to be applied instead — did working this reply
change how dokimasia works — and for the answer either way. anoieu ran that test
as its default and stopped: a round that changes nothing here is still a round
whose *reasoning* about why it changed nothing is worth having, and the
judgement call cost more than the entry. We start where they ended up rather
than repeat the experiment.

**The shape of an entry.** One heading per run — one reply worked — and **one**
`Tool:` / `Summary:` / `Resolution:` block under it, describing the run. A run
usually touches several rows; those are sections beneath, and they carry detail
rather than fields of their own.

```text
## <date> — <project>: <what this run was>

**Tool:** the project the rows were reported to. This is what was passed to
`scripts/prompts/process_dokimasia`, so it is never a judgement call.

**Summary:** **what the nature of the rows was**, most important first — what
was actually wrong with the software, not what the exchange consisted of.
Written for somebody who works on neither project: no ids, no counts, no
procedure. **Two sentences, 250 characters at most.**

**Resolution:** how it came out, as a breakdown — how many were real defects
and of what kind, how many were deliberate and declined, how many were ours to
fix — and what changed here as a result. Counts and links belong in this field,
not in the summary.

### <row id, or a phrase for a group of them> — <what it was>

<What happened — only enough to make the resolution make sense.>
```

[`tests/test_workflow.py`](../tests/test_workflow.py) checks that much of the
shape a reader cannot enforce by reading: one field block per run, none on the
sections beneath it, and a summary short enough to still be one.

## Where the workflow stands

**Nothing has been worked yet.** Nothing has been carried to cvc5 through this
pair of scripts, so the log below is empty because there is nothing in it, not
because nobody wrote it up. The first run writes the first entry.

Two things are known to be missing before then, and both are named in
[`workflows.md`](workflows.md): nothing restores the cvc5 commit a row was
measured against, and a curated row has no fingerprint anybody can reproduce.
Either could be what the first postmortem is about.

## The log
