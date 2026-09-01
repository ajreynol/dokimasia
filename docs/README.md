# Documentation

The index of `docs/`. The front page is [`README.md`](../README.md), which says
what the analyzer is and what exists today; everything here is the reasoning
behind it.

## Start here

| | |
| --- | --- |
| [`why.md`](why.md) | **why cvc5 should care** — the three claims this repository can back, what it has not delivered, and what would show it is wrong |
| [`checks.md`](checks.md) | **the checks** — the sixteen facets, what each has returned against a checkout, and what the unfinished ones are waiting on |
| [`next-report.md`](next-report.md) | **the next thing to report, and why it is that one** — the recommendation, the runner-up, and what is explicitly not ready |
| [`reachability.md`](reachability.md) | **what the corpus actually reaches** — the static denominator against cvc5's own runtime counters, measured over `regress0` |
| [`pr-policy.md`](pr-policy.md) | **we never open a pull request** — the hard rule, what the tools may do instead, and the three errors this session caught that an automated path would have shipped |

## The stance and the subject

| | |
| --- | --- |
| [`goals.md`](goals.md) | the stance, the goal, the agility constraint, and how we would know it is working |
| [`contract.md`](contract.md) | what cvc5 promises, where, and the three ways completeness breaks |
| [`pipeline.md`](pipeline.md) | the stages of proof production and where each leaks |
| [`kernel.md`](kernel.md) | the two stretch goals: a kernel you can argue about, and a safe build that cannot be unsafe |

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
| [`workflows.md`](workflows.md) | how a candidate is carried to cvc5 and back: the conventions we share with anoieu, the two prompts, and the two scripts that run them |
| [`postmortem.md`](postmortem.md) | what working a reply taught us about the workflow itself, as opposed to what it settled about cvc5 |
| [`discussion.md`](discussion.md) | the standing channel to the rest of the ecosystem, and the gate on responding to it |

## Generated, and the landscape

| | |
| --- | --- |
| [`fragment.md`](fragment.md) | *generated* — which term kinds may appear per theory under `--safe-mode=safe`, and how the fragment is enforced |
| [`tooling.md`](tooling.md) | the C++ static-analysis landscape, our design decisions, and the posture toward murxla |
