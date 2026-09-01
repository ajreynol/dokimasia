# Case studies

**A cvc5 developer asks a design question. We answer it with a check.**

That is the decision this directory records, and it is a standing one: these
requests will keep arriving, and answering them well is the highest-value thing
this repository does per hour spent.

## Why a check and not an answer

A design question from a maintainer — *why can't safe mode have debug symbols?*,
*is this restriction still needed?*, *does this flag still do anything?* — has
three possible answers, and only one of them is worth the exchange.

| answer | worth |
| --- | --- |
| an opinion | nothing. They know the code better than we do |
| a reading of the source | something, once. It is stale the next time somebody edits |
| **an invariant, verified, with the verifier attached** | the answer, *and* the guarantee it stays the answer |

The third is the only one that survives contact with a codebase under
development. It also inverts the usual burden: instead of us asserting something
about their code, they get a thing that will tell them when it stops being true.

## The shape

Every case follows it, and a new one should:

1. **State the question as the requester asked it**, not as we would rather
   answer it — and state the existing decision as what it is. A deliberate
   simplification is not an oversight, and reading it as one gets the whole case
   wrong. Ask what the decision *costs*, not why it was made.
2. **Find the invariant the answer rests on.** *"Forbidding safe + debug costs
   almost nothing"* rests on *"a safe build differs only in defaults, text and
   reporting"*. The second is checkable; the first is not.
3. **Enumerate exhaustively.** Eight sites, all eight classified. A case that
   says "we looked at the main ones" has not answered anything.
4. **Say where the invariant is imperfect**, in its own section. Every one of
   these has an *almost*, and the almost is usually the interesting part — for
   #12899 it is that the divergence is real but lives in message text the
   regression testers read, so the restriction bites only when debugging a
   safe-mode skip.
5. **Ship the verifier**, with tests that show it firing on each way the
   invariant can break.
6. **Give a verdict** against [the bar](../pr-policy.md#the-bar), including what
   would falsify it and what we are *not* claiming.

## Why this suits us

We are a static analyzer over cvc5's proof-production code that builds nothing
and runs in seconds. That makes us badly suited to answering *what should we
do*, and well suited to answering *what is currently true, exhaustively, and is
it still true today*. A design question is usually the second thing wearing the
first thing's clothes.

It is also the cheapest work we do that a maintainer can act on immediately: no
reproducer to construct, no benchmark to find, no waiting on a corpus. The
question arrives already scoped.

## Standing rules

- **The requester's question is the title.** If the case study cannot be named
  by the question it answers, it has drifted.
- **A case study is not a finding.** It is an answer to something asked. It may
  *produce* a finding — an adoption, or a defect discovered on the way — and
  those go in [`issues.md`](../issues.md) with an id, as usual.
- **The verifier is the deliverable, and it must have failed in a test.** A
  checker nobody has seen fail is a checker nobody should trust.
- **We never open the PR.** Same as everything else:
  [`pr-policy.md`](../pr-policy.md).
- **Say what we did not check.** For #12899 we did not build a safe build and
  diff the binaries; the case says so.
- **We are usually not asking for the decision to change.** The useful output is
  what a decision costs and what keeps that cost stable. Arguing for a different
  choice is the requester's prerogative to invite, not our default.

## The register

| case | question | check | verdict |
| --- | --- | --- | --- |
| [safe-build-vs-safe-mode](safe-build-vs-safe-mode.md) | cvc5 [#12899](https://github.com/cvc5/cvc5/pull/12899) — the configure script deliberately forbids safe + debug for simplicity. **Is that actually a restriction?** | `BUILD0001`, [`dokimasia.buildmode`](../../dokimasia/buildmode/) | **carry** — it costs one thing only (safe-build diagnostics on a debug binary), and an invariant nothing maintains is what keeps the cost that low |
