# The RARE correspondence

A design note. **The problem:** a RARE rule and the C++ that performs the same
rewrite are two independent statements of one fact, and nothing relates them.

## The problem, precisely

`bool-double-not-elim` is declared in `theory/booleans/rewrites`:

```lisp
(define-rule bool-double-not-elim ((t Bool)) (not (not t)) t)
```

and somewhere in `theory_bool_rewriter.cpp` there is C++ that eliminates double
negation. Nothing links them. The rewriter does not know the rule exists; the
rule does not know which code implements it.

**This is not an oversight — it is the design.** RARE stands for *rewrites,
automatically reconstructed*: the correspondence is meant to be **discovered at
proof time**, by `RewriteDbProofCons` searching the rule database for something
that explains the rewrite the C++ already performed. Declaring the link would
defeat the point, which is that the rewriter stays free and the proof layer
catches up.

That design has consequences worth stating plainly.

## Four ways it goes wrong

| | failure | how it shows up today |
| --- | --- | --- |
| **F1** | a RARE rule **misstates** the rewrite — says the rewriter does `L → T` when it does `L → T'` | never. The rule simply never matches. It sits in the database, is searched, and silently contributes nothing |
| **F2** | a rewrite the C++ performs has **no RARE rule** | reconstruction fails → `TrustId::MACRO_THEORY_REWRITE_RCONS_SIMPLE`, a trust step |
| **F3** | a RARE rule is **dead** — nothing the rewriter does ever needs it | never. It enlarges the search space for every proof |
| **F4** | the correspondence exists but the **search does not find it** in budget | trust step, indistinguishable from F2 |

F1 and F3 are invisible. F2 and F4 are visible but indistinguishable from each
other, which matters because they have opposite fixes: F2 needs a new rule, F4
needs a bigger budget or a better search.

## What is checkable now, with no build

Statically, from the files alone:

- **Six of fourteen theories have no RARE rules at all**: `bags`, `datatypes`,
  `ff`, `fp`, `quantifiers`, `sep`. Four of those are disabled in safe mode, so
  they do not bear on the contract — but **`datatypes` and `quantifiers` are
  enabled**. Every rewrite they perform must be reconstructed through a
  hand-written `ProofRewriteRule` or become a trust step. That is a structural
  statement about where F2 is concentrated, available today.
- **RARE database self-consistency**: rules whose match pattern is subsumed by
  another, conditions that cannot hold, patterns that are not in the rewriter's
  normal form. Cheap, and none of it needs cvc5 to run.

Neither touches the hard question, which needs execution.

## How it could be enforced

Ranked by value per unit of risk.

### E1 — instantiate each RARE rule and run the rewriter

**The direct test, and the one we would build first.** For each rule, build an
instance of its match pattern, call `Rewriter::rewrite` on it, and check the
result is the instantiated target.

- kills **F1** outright and **F3** for anything the rewriter declines to do;
- 439 rules, 439 tiny checks, no new theory;
- belongs in **cvc5's unit tests**, not here — it needs the rewriter, and a test
  that lives beside the thing it tests will be maintained;
- the awkward parts are real but bounded: `define-cond-rule` needs an
  instantiation satisfying the condition, `define-rule*` is a fixed point, and
  some patterns need well-sorted terms of a specific shape. **A partial version
  that skips conditional rules and uses ground instances would still cover most
  of the database**, and partial is the enemy of nothing here.

### E2 — read the coverage cvc5 already collects

`finalProof::dslRuleCount` counts, per rule, how often reconstruction used it;
`finalProof::trustTheoryRewriteCount` counts reconstruction failures per theory.
Both are already registered and switched on by `--stats-internal`.

- a corpus run gives an empirical read on **F3** (never used) and **F2/F4**
  (failures, by theory);
- **no new cvc5 code at all** — this is orchestration;
- weak in the obvious way: never-used ≠ dead, it may just mean the corpus never
  needed it.

### E3 — annotate the C++ rewrite site with its rule name

Cheap to state, hand-maintained, and therefore exactly the kind of thing this
repository keeps finding rotted. **Not worth doing if E1 exists**, because E1
verifies the correspondence rather than asserting it. Worth doing only as a
by-product of E4.

### E4 — compile the RARE database, and reframe what for

The stretch goal, and worth being careful about what it means.

Generating the **rewriter** from RARE is the ambitious reading: one source, so
the correspondence holds by construction. The objections are serious — the
hand-written rewriter is ordered and tuned, RARE matching is purely syntactic,
and a DSL stretched until it can express the whole rewriter stops being a DSL.

But there is a smaller, sharper target with most of the value:

> **Compile the RARE database into the reconstruction matcher**, so that finding
> the rule for a rewrite is syntax-directed rather than searched.

That does not touch the rewriter at all. What it buys:

- **it removes the budget.** Reconstruction today runs under
  `--proof-rewrite-rcons-rec-limit`, so proof completeness depends on a search
  succeeding in time ([`i-4`](issues.md)). A compiled matcher either matches or
  does not, and the answer stops depending on how long we let it look;
- it makes **F4 disappear as a category**, which makes F2 diagnosable — right
  now the two are the same trust step;
- it is the only route we can see to discharging the kernel's sixth obligation
  ([`kernel.md`](kernel.md)), which we already predicted could not be discharged
  against a searched reconstruction.

That is the version of the auto-compiler idea we would argue for. Generating the
rewriter is a much larger claim with a much less certain payoff.

## What we would recommend

1. **E2 first** — it is a corpus run against instrumentation that already
   exists, and it tells you where F2 and F3 actually bite before anyone writes
   code.
2. **E1 next, upstream in cvc5** — the direct test, partial is fine, and it is
   the only thing that catches F1 at all.
3. **E4 (matcher, not rewriter) as the stretch goal**, argued on removing the
   budget rather than on unifying the source.
4. **E3 only if E4 happens**, as its output rather than as a discipline.

And regardless of any of it: **`datatypes` and `quantifiers` have no RARE rules
while being enabled in safe mode**, which is where we would look first for F2.

## A related question, not the same one

Hand-written theory rewrites — the 94 `ProofRewriteRule`s with no RARE origin —
are honestly hand-written, and cvc5 does not pretend otherwise. The open
question there is different: **is the same rewrite implemented twice**, once on
the proof-producing path (`rewriteViaRule`) and once on the ordinary one
(`postRewrite`)? If the two implementations can diverge, a proof would describe
a rewrite the solver did not actually perform. Detecting that needs the two
paths compared, not the RARE database, and it is tracked separately.
