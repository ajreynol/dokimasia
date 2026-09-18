# Documentation

The index of `docs/`. The front page is [`README.md`](../README.md), which says
what the analyzer is and which checks it runs; everything here is the reasoning
behind it.

The scope is cvc5's proofs. General cvc5 development and the former child
projects are maintained in [Paideia](https://github.com/ajreynol/paideia), which
is their source of truth. Performance, including proof-production overhead,
belongs to [Tachyon's Elaphros](https://github.com/ajreynol/tachyon/tree/main/tools/elaphros).

## Start here

| | |
| --- | --- |
| [`analyzer.md`](analyzer.md) | run the structured analyzer, append through Koine, and compare an independent producer |
| [`usage.md`](usage.md) | developer reports, optional measurements and examples at the pinned cvc5 revision |
| [`maintenance.md`](maintenance.md) | development checks, dependency pins and the script catalogue |
| [`bug_db/README.md`](../bug_db/README.md) | Dokimasia's bug database artifact: setup, recording and interpretation |
| [`bug_db/bugs.md`](../bug_db/bugs.md) | browse every recorded observation in Markdown; evidence is archived under `bug_db/runs/` |
| [`why.md`](why.md) | **why cvc5 should care** — the three claims this repository can back, what it has not delivered, and what would show it is wrong |
| [`checks.md`](checks.md) | **the checks** — the sixteen facets, what each has returned against a checkout, and what the unfinished ones are waiting on |
| [`cases/`](cases/) | **case studies** — a cvc5 design question, answered with a verifier rather than an opinion. The standing decision, and the register |
| [`cases/out-of-scope-bug-report.md`](cases/out-of-scope-bug-report.md) | cvc5 [#12905](https://github.com/cvc5/cvc5/issues/12905) — a real bug report that is not a proof bug. What we do with it, where the learning lives, and the routing test for the next one |
| [`cases/safe-build-vs-safe-mode.md`](cases/safe-build-vs-safe-mode.md) | cvc5 [#12899](https://github.com/cvc5/cvc5/pull/12899) — is deliberately forbidding safe mode with debug symbols actually a restriction? What it costs, and the invariant that keeps the cost that low |
| [`next-report.md`](next-report.md) | **the next thing to report, and why it is that one** — the recommendation, the runner-up, and what is explicitly not ready |
| [`reachability.md`](reachability.md) | **what the corpus actually reaches** — the static denominator against cvc5's own runtime counters, measured over `regress0` |
| [`pr-policy.md`](pr-policy.md) | **DEPRECATED (2026-09-18)** — historical reporting policy; [replacement pending](maintenance.md#replace-the-deprecated-reporting-workflow) |

## The stance and the subject

| | |
| --- | --- |
| [`goals.md`](goals.md) | the stance, the goal, the agility constraint, how we would know it is working, and whether there is a paper in it |
| [`contract.md`](contract.md) | what cvc5 promises, where, and the three ways completeness breaks |
| [`pipeline.md`](pipeline.md) | the stages of proof production and where each leaks |
| [`kernel.md`](kernel.md) | the two wishues: a kernel you can argue about, and a safe build that cannot be unsafe |

## What we ask of cvc5

| | |
| --- | --- |
| [`hygiene.md`](hygiene.md) | proof hygiene for cvc5 — ten rules, each with a measurement |
| [`issues.md`](issues.md) | everything we are asking cvc5 to act on, in one register with one id space |
| [`coupling.md`](coupling.md) | what we ask of cvc5, and what we parse that could break |
| [`rare-correspondence.md`](rare-correspondence.md) | a design note: a RARE rule and the C++ that performs the same rewrite are two statements of one fact, and nothing relates them |

## Reporting, and how work is carried

| | |
| --- | --- |
| [`findings.md`](findings.md) | what a finding is, what we promise about it, and the log — including retractions |
| [`findings/`](findings/) | one file per filed finding; today that is [`tcb-001.md`](findings/tcb-001.md) |
| [`workflows.md`](workflows.md) | **DEPRECATED (2026-09-18)** — historical reporting workflow and retained launchers; [replacement pending](maintenance.md#replace-the-deprecated-reporting-workflow) |
| [`postmortem.md`](postmortem.md) | what working a reply taught us about the workflow itself, as opposed to what it settled about cvc5 |
| [`discussion.md`](discussion.md) | the standing channel to the rest of the ecosystem, and the gate on responding to it |

## Generated, and the landscape

| | |
| --- | --- |
| [`fragment.md`](fragment.md) | *generated* — which term kinds may appear per theory under `--safe-mode=safe`, and how the fragment is enforced |
| [`reports/static-analysis.md`](reports/static-analysis.md) | old report location; redirects readers to the Markdown view in `bug_db/` |
| [`tooling.md`](tooling.md) | the C++ static-analysis landscape, our design decisions, and the posture toward murxla |
