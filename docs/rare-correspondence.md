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

**This is not an oversight — it is the design, and the design is argued for in
print.** RARE stands for *rewrites, automatically reconstructed*, and the
approach is set out in [Nötzli et al., FMCAD 2022, *Reconstructing Fine-Grained
Proofs of Rewrites Using a Domain-Specific
Language*](https://homepage.divms.uiowa.edu/~ajreynol/fmcad2022.pdf). Its
opening move is exactly the thing we noticed:

> *"we propose an alternative approach that does not rely on instrumenting the
> original rewriter. Instead, our approach treats the rewriter as a black
> box"* — §I

Instrumenting the rewriter is what the paper set out to avoid, because
*"instrumenting this code to additionally produce proofs makes it even more
complex and makes it harder to add new rewrite rules."* So the link is absent on
purpose: the rewriter stays free, and a **post-processing reconstructor**
searches the rule database for something that explains what the rewriter already
did. Recording the correspondence would reintroduce the coupling the design
exists to avoid.

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

### E4 — "compile RARE" — and why this is an open problem

**We had this wrong in an earlier draft**, and the correction is the most
useful thing in this note. We proposed compiling the rule database into a
syntax-directed matcher so that reconstruction became lookup rather than search,
and claimed that would remove the budget. Both halves are mistaken.

**Matching is already compiled.** The paper's DSL compiler builds a
*discrimination tree* indexing every rule's conclusion, and rule conclusions are
normalised so variables are drawn from a global list left-to-right. Finding
which rules *might* apply to a term is already an indexed lookup. That is not
where the cost is.

**The search is over proof obligations, not over rules.** Look at what happens
when a candidate rule fires, in the paper's algorithm `rc(t ≈ s, d)` (Fig. 3,
lines 14–18). For a rule `p⃗ ≈ q⃗ ⇒ u ≈ v` and a match `t = σ(u)`, it recurses
**twice**:

- `rc(σ(v) ≈ s, d−1)` — the instantiated right-hand side is usually *not*
  syntactically the target. The remaining gap is a fresh
  equality-reconstruction problem. cvc5's implementation calls this out in a
  comment: *"the missing transitivity link is a subgoal to prove"*
  (`rewrite_db_proof_cons.cpp`).
- `rc(σ(p) ≈ q, d−1)` for **every precondition** of a `define-cond-rule`. Each
  is a fresh equality-reconstruction problem of its own.

So applying one rule spawns sub-problems of the same kind. **A rule that looks
trivial can be arbitrarily deep**, because its preconditions and its
right-hand-side gap are themselves rewriting problems. The paper's own
`concat-clash` example makes the point: its precondition `|s₁| ≈ |t₁|` *"does
not require the evaluation of |s₁| and |t₁|. Instead, it just requires some
proof that they are equal. In practice, we prove the precondition by applying
additional rewrite rules."*

**And there is no termination guarantee.** The paper says so directly:

> *"The rationale behind the depth limit on the search is that there is no
> guarantee that preconditions are simpler than the current equality to be
> proved, and so there is no guarantee of termination in general."* — §IV-A

That is the whole answer to why `--proof-rewrite-rcons-rec-limit` exists. It is
not a performance knob bolted onto a decidable procedure; it is what makes a
possibly-non-terminating search halt. Note `d` is decremented **only** on
conditional-rule premises and the RHS gap — congruence recurses on subterms
without decrementing, relying on term size for termination — so the entire depth
budget is spent on exactly the two sources above.

**Four further reasons a compiled procedure is not close to hand:**

1. **Commutativity is not built in.** *"the matching does not automatically take
   into consideration the commutativity of operators. Instead, the algorithm
   relies on the commutativity of operators being expressed as additional
   rewrite rules."* Any compilation must either enumerate orientations or bake
   in AC reasoning.
2. **Some rewriting is not rules at all.** Arithmetic *"boils down to
   normalizing polynomials"*, handled by a single built-in tactic plus 25
   ordinary rules. cvc5 today carries a whole family of such tactics —
   `ARITH_POLY_NORM`, `ACI_NORM`, `ABSORB`, `FLATTEN`, `CONG_EVAL` — which are
   not RARE rules and never will be.
3. **Fixed-point rules already trade completeness for speed.** `define-rule*`
   rules are applied to a fixed point *"without considering possible
   interleavings of other rules... at the cost of not considering some possible
   reconstructions. Thus, there is a trade-off, and this feature must be used
   carefully."*
4. **Not every rewrite is expressible.** The string rewriter is *"over 3,000
   lines of C++ code and distinguishes over 200 different rewrite rules.
   Moreover, not all of those rules can be expressed as a single rewrite rule in
   RARE."* The database was grown *"on demand to fill in missing subproofs"* —
   40 string rules, 22 Boolean rules at publication.

**What the paper measured**, and the number that matters most to us: fine-grained
proofs were reconstructed for **95% of rewrite steps** on the industrial set and
**92%** on SMT-LIB — but only **20% of industrial benchmarks (5 of 25)** and
**22% of SMT-LIB proofs containing rewrite steps (5,945 of 26,418)** were
*fully* fine-grained. A per-step success rate of 92% is a per-proof rate of 22%,
because one unreconstructed step makes the whole proof coarse. Cost was a
**3.14× slowdown** overall.

So: **compiling RARE is an open research problem**, and it is the right one to
be interested in. Removing the depth bound means giving the recursion a
termination argument that does not exist today — an ordering on
equality-reconstruction sub-problems under which preconditions and RHS gaps are
provably smaller. Nothing in the current design provides one, and the paper is
explicit that none is known.

That is also why this is *the* lever on [`i-4`](issues.md): while reconstruction
is a bounded search, proof completeness is a function of a budget rather than of
the code, and no static analysis — ours or anyone's — can discharge it.

## What we would recommend

1. **E2 first** — it is a corpus run against instrumentation that already
   exists, and it tells you where F2 and F3 actually bite before anyone writes
   code.
2. **E1 next, upstream in cvc5** — the direct test, partial is fine, and it is
   the only thing that catches F1 at all.
3. **E4 as research, not engineering.** The tractable sub-question is not
   "compile the database" but **"can the recursion be given a termination
   argument?"** — for instance by restricting preconditions to a fragment
   provably simpler than the goal, which would make the depth bound
   unnecessary *for rules in that fragment* while leaving the rest as they are.
   A classification of the 439 rules by whether their preconditions and RHS gaps
   are structurally decreasing would say how much of the database such a
   restriction could cover. **That is a static analysis, and it is one we could
   do.**
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
