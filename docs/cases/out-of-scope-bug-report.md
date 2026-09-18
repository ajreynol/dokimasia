# A real bug report arrives that is not a proof bug

**The request.** cvc5 [#12905](https://github.com/cvc5/cvc5/issues/12905) — a
fatal failure at `theory_engine.cpp:2030` on a strings-and-quantifiers
benchmark:

```
(declare-const x Int)
(assert (exists ((s String) (t Int))
  (and (= 1 (str.len (str.++ (str.substr s 0 1) (str.at s t))))
       (not (str.suffixof (ite (str.in_re "/" (str.to_re s))
                               (str.substr s 0 x)
                               (str.replace "/" s "")) s)))))
(check-sat)
```

> *wasn't sent to you, so why are you explaining it trivially, for fact
> `(not (= (+ (str.len @quantifiers_skolemize_2) (* (- 1) (str.len @purify_4))) 0))`*

**This is not a proof bug.** It is a theory-explanation defect: a fact reached
the explanation machinery that the engine did not think it had sent. Nothing in
it concerns whether a step can produce a proof, which is the whole of what this
repository is for.

**Two questions follow, and they have different answers.**

## 1. What does this repository do with it?

**Nothing, and it says so.** dokimasia holds one role — *what no proof step
covers* — and an assertion failure in theory combination is not it. Taking it
would be the most ordinary failure mode available to a tool with a working
analysis and spare attention: scope creep dressed as helpfulness.

The register stays clean: #12905 gets no `i-` id, because
[`issues.md`](../issues.md) is *things we are asking cvc5 to act on*, and we are
asking nothing. cvc5 already has the report; a second opinion from us is not a
contribution.

**The one thing worth checking is whether the classification is right.** "Not a
proof bug" is a claim, and the cheap version is: does the reproducer produce a
proof hole? If it did, the issue would be partly ours after all. That check is
[the corpus sweep](../reachability.md) pointed at one file, and it costs a
minute.

## 2. Where does the *learning* live?

This is the question worth a case study, because the answer is not "nowhere".

The maintainer will answer #12905 — reproduce it, locate it, fix it or explain
why it is not a bug. **That answer is evidence about how cvc5 issues get
addressed**, and it is evidence this repository is well placed to collect and
badly placed to act on. We run assistants against cvc5 issues already
([`prompts/check_cvc5_issue`](../../prompts/check_cvc5_issue));
what we have
never done is record what the human answer taught that the assistant missed.

**The current home is [Paideia](https://github.com/ajreynol/paideia).** The
original decision was to start `empeiria` as a child project under Dokimasia's
`tools/`, using the existing issue workflow and reporting discipline. On
2026-09-18, the maintainer moved it and `anakrisis` to Paideia. That repository
is now the source of truth for their charters, plans, protocols and ledgers.

[Empeiria's charter](https://github.com/ajreynol/paideia/blob/main/tools/empeiria/README.md)
owns the question of **working a cvc5 bug and learning from how the maintainers
answered**. General cvc5 development belongs there. Dokimasia keeps the proof
question: if an issue exposes a proof-completeness gap, that gap enters this
repository's register. Performance, including proof-production overhead,
belongs to
[Tachyon's Elaphros](https://github.com/ajreynol/tachyon/tree/main/tools/elaphros)
and is outside this repository's scope.

## What the original decision sought to change

The maintainer's side of the loop was already defined —
[`prompts/check_cvc5_issue`](../../prompts/check_cvc5_issue)
writes a `TRIAGE:`
block and leaves `HUMAN RESPONSE:` empty for a person. What was missing is what
happened **after** the response arrived: the answer was read and the file was
forgotten.

The change is small and is the whole point: **the response is an artifact, and
the delta between it and the triage is the thing worth keeping.** Not the
issue, not the fix — the difference between what an assistant concluded and what
a maintainer did. The work to record and learn from it now lives in Paideia;
its current status is recorded there.

## Verdict

| | |
| --- | --- |
| **never** — for the issue itself | #12905 is not ours. No id, no register row, no report. The only work it earns is confirming it produces no proof hole |
| **carry — to ourselves** | the routing decision; [Empeiria in Paideia](https://github.com/ajreynol/paideia/tree/main/tools/empeiria) now holds the general bug-work question |
| what would change it | the reproducer turning out to produce a trust step or an unhandled rule, which would make it partly a proof bug and partly ours |

**What we are not claiming.** We have not run the reproducer. The
classification rests on reading the assertion message, which names theory
explanation and not proof production — good enough to decline the issue, not
good enough to assert there is no proof hole behind it. That check is queued,
not done.

## A note on scope, since more of these will arrive

The generalisable part is the second question, not the first. Declining
out-of-scope work is easy and this repository should keep doing it. The harder
discipline is **noticing that the out-of-scope thing still produced evidence**,
and putting the evidence somewhere with a boundary around it rather than either
absorbing it or throwing it away.

The routing test, for the next one:

1. **Is it ours?** If it is about whether a step can produce a proof, it is a
   normal candidate and goes in the register.
2. **Is it about performance?** Time and memory overhead, including that of
   producing proofs, belong to
   [Tachyon's Elaphros](https://github.com/ajreynol/tachyon/tree/main/tools/elaphros).
3. **Is it general cvc5 development or learning from that work?** Route it to
   [Paideia](https://github.com/ajreynol/paideia); its project charters determine
   what work it takes on.
4. **If none applies, decline it and say why in one line.** Silence reads as
   agreement, and a tool that quietly collects other people's problems has
   stopped having a role.
