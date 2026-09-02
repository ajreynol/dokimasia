# The two wishues

Both are *progressive*: they improve by degrees, every degree is worth
having, and neither has a finish line. Neither is a claim about
verification tools.

A **wishue** is a goal you would take if the work went unusually well and are
not committing to — a wish written down as an issue. The word is cvc5's own:
it keeps a `cvc5-wishues` tracker and its source carries seventeen
`TODO (wishue #N)` comments, at `40a4bb7e4`. This repository used to call these
two *stretch goals*, and stopped because *stretch* now names something else
across the Eunoia ecosystem — the span between two announcements. Same two
goals, one less collision.


## A kernel you can argue about

The arc of this project is to stop reporting holes and start being able to say
which part of cvc5 is its proof kernel.

**This is not a claim about verification tools.** "Verified kernel" here does not
mean a machine-checked theorem, and treating it that way sets the bar somewhere
useless — nothing available today verifies a contract like this over cvc5's C++,
and waiting for something that does means delivering nothing. The goal is softer
and much more achievable:

> **Make it easier to argue what cvc5's proof-producing kernel is.**

An argument, made to a person, that this set of code is what has to be right.
That goal is *progressive*: it improves by degrees, every degree is worth
having on its own, and no step is the last one. The axes it improves along:

| axis | the question | today |
| --- | --- | --- |
| **nameable** | can you enumerate the kernel at all? | partly — `--safe-mode=safe` names a configuration, not a set of code |
| **closed** | does the boundary hold — does nothing inside reach out? | unknown, and [`tcb-001`](findings/tcb-001.md) is one place it does not |
| **small** | how much is inside? | the internal checker compiles against 41,446 lines, 8.0% of `src/` |
| **local** | can a reader check one obligation by reading one function? | rarely |
| **mechanized** | is any part machine-checked? | no, and that is the *last* axis, not the first |

Progress on any row is real progress. A kernel that is nameable and closed but
unverified is worth far more than one nobody can point at, and the measure that
matters is **how long the argument is and how much of it a reader can check** —
not whether a tool printed `QED`.

### Hygiene comes first, because you cannot bound what you cannot name

Every such argument is made out of entities — inferences, rules, trust steps —
and is only as sharp as those entities are. If an `InferenceId` is emitted at
eight places, "the inferences theory X can make" is not an enumerable set, and
nothing quantified over it means anything.

So the warm-up project is a **proof hygiene standard** for cvc5:
[`docs/hygiene.md`](hygiene.md). Naming conventions, calling conventions,
checker registration, and the discipline around inference ids — which are cvc5's
existing *informal* proof markers, and the natural spine for all of this. Ten
rules, each with a measurement behind it, most of them ratifying what cvc5
already does. The chain the whole project runs on:

**hygiene → nameable entities → a drawable boundary → an argument someone can
check → (eventually, in places) mechanization.**

### Measuring the kernel: the checker's TCB

The internal proof checker is the natural kernel candidate — it is the component
that decides whether a cvc5 proof is valid — and its value is inversely
proportional to how much of cvc5 it needs. That is measurable today, so it is
the first thing this repository actually built:

```bash
python3 -m dokimasia.tcb measure <cvc5>   # 179 files, 41,446 lines, 8.0% of src/
python3 -m dokimasia.tcb cuts    <cvc5>   # what each dependency edge costs
python3 -m dokimasia.tcb why     <cvc5> theory/strings/core_solver.h
python3 -m dokimasia.tcb baseline <cvc5> --check   # the ratchet, for CI
```

The first finding came out of it:
[**`tcb-001`**](findings/tcb-001.md) — 12 of 13 rule checkers are clean,
but six include the headers of the theory solvers they check, to reach `static`
helpers parked on the solver classes. The refactoring is mechanical and the
report names it per site.

That number going down *is* the kernel argument getting shorter. It needs no
verification tool, no build, and nobody's agreement to start.



## A safe build that cannot be unsafe

Safe mode promises "no feature that does not have full proof and model support."
Today that promise is kept **at runtime**, by `SetDefaults::setDefaultsPre`
turning things off by name, and by `NoOpTheoryRewriter` throwing
`SafeLogicException` when a disabled theory is reached anyway. The unsafe code is
still compiled, still linked, still one missed guard away.

There is already a build-time safe mode — `cvc5_option(ENABLE_SAFE_MODE)` sets
`-DCVC5_SAFE_MODE` — but it prunes almost nothing of cvc5's own code. **Five
files in `src/` mention it**, and two of those only reword an error message
("suggested options only in non-safe builds"). What it genuinely excludes is
third-party: LibPoly and CoCoA.

So the goal, in the same spirit as the kernel and sharing its tooling:

> **Make the safe build not contain the unsafe code.**

Progressive, exactly like the kernel argument, and with the same measure — the
dependency closure of the safe binary, which
[`dokimasia.tcb`](../dokimasia/tcb/) already computes. Each feature moved from
"disabled at runtime" to "not compiled" is a class of proof hole converted into
a **link error**, which is the cheapest possible latency: the compiler finds it,
instantly, without an input.

And there is a consistency check available *right now*, statically, with no
build: **the runtime disable list and the build-time exclusion list must agree.**
Today they plainly do not — `setDefaultsPre` disables `sep`, `bags`, `ff` and
`fp`; `CVC5_SAFE_MODE` excludes LibPoly and CoCoA. Every feature that is disabled
at runtime but present in the safe build is a feature that a missed guard makes
reachable.

### Tracking the mode delta

[`dokimasia.modes`](../dokimasia/modes/) extracts every option change in
`set_defaults.cpp` with its guards, renders the per-mode delta, and ratchets
it. Its `check` subcommand cross-references the machine-readable
`no_support = ["proofs"]` annotations against what safe mode actually
disables. Usage in [the README](../README.md#what-exists-today).
