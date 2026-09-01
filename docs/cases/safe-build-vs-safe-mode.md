# Is refusing `--safe-mode` with debug symbols actually a restriction?

**The design decision.** cvc5's configure script does not allow a safe build to
be combined with debug symbols. This is **deliberate and for clarity**: the
build already carries a large configuration space, and every combination
permitted is one more thing to explain, test and keep working. Forbidding a
combination nobody has needed is a reasonable simplification, and
[#12899](https://github.com/cvc5/cvc5/pull/12899) flattening the build system is
the natural moment to ask whether it is still the right one.

**The research question is not why it is forbidden.** It is: **does forbidding
it actually deny anyone anything?**

**Our answer:** almost nothing, and we can say exactly what the *almost* is. A
safe build differs from an ordinary build in one semantic respect — the default
value of a runtime option — so an unrestricted debug build run with
`--safe-mode=safe` reproduces a safe build's *behaviour* exactly. What it does
not reproduce is the diagnostic text, and that text is read by the regression
testers.

**So the simplification is currently free, and the reason it is free is an
invariant that nothing in cvc5 maintains.** That is what this case is really
about, and what
[`dokimasia.buildmode`](../../dokimasia/buildmode/) exists to protect.

*Measured against cvc5 `40a4bb7e4`.*

## What a safe build actually is

`ENABLE_SAFE_MODE` does three things in `CMakeLists.txt`: defines
`-DCVC5_SAFE_MODE`, turns off `USE_POLY` / `USE_COCOA` / `USE_NORMALIZ`, and
changes the printed build profile. The macro is referenced in **eight places in
all of `src/`**, and every one falls into one of three categories:

| where | what it does | category |
| --- | --- | --- |
| `options/options_template.cpp` | `d_base->safeMode = options::SafeMode::SAFE` in the `Options` constructor | **an option default** |
| `base/configuration_private.h` | `#define IS_SAFE_BUILD true` | build self-report |
| `smt/logic_exception.h` | prepends `"Logic restricted in safe mode. "` | message text |
| `theory/theory_rewriter.cpp` | omits `" Try --ff."`-style hints | message text |
| `smt/illegal_checker.cpp` | omits `" Try --arrays-exp."`-style hints | message text |

Two further facts complete the picture:

- **No source file is excluded.** `src/CMakeLists.txt` never mentions
  `ENABLE_SAFE_MODE`; a safe build compiles the same translation units.
- **Nothing branches on the build.** `Configuration::isSafeBuild()` has exactly
  one caller — `options_handler.cpp`, printing `--show-config`. It is reported,
  never acted on.

The safe build's only semantic act is to change the *starting value* of a
runtime option, which is exactly what `--safe-mode=safe` does.

## What the restriction costs

Three things a safe build gives you, and whether a debug build with
`--safe-mode=safe` gives them too:

| | reproduced by `--safe-mode=safe`? |
| --- | --- |
| the solver's behaviour — what is accepted, rewritten, proved | **yes, exactly.** It is the same option, set the same way |
| the three optional libraries being absent from the binary | **no** — they are linked and simply not reached |
| the diagnostic text, including the `"in safe mode"` prefix | **no** — that is decided at compile time |

Only the third is a cost to a developer, and it is a real one:

**The exception text is load-bearing for CI.** `SafeLogicException` prepends
`"Logic restricted in safe mode. "` at compile time, and
`smt/logic_exception.h` says why that matters:

> *The regression testers will consider any exception having text "in safe mode"
> or "in stable mode" as an admissible failure, and skip the benchmark.*

Verified on an unrestricted binary at `--safe-mode=safe`:

```
$ cvc5 --safe-mode=safe cos.smt2
(error "Cannot handle assertion with term of kind cos in this configuration.")
```

No `"in safe mode"` prefix — a safe build emits one. The same run also *keeps* a
hint a safe build drops:

```
$ cvc5 --safe-mode=safe ff.smt2
(error "Cannot handle assertion with term of kind CONST_FINITE_FIELD in this
        configuration. Try --ff.")
```

**Consequence:** a benchmark that a safe build *skips*, an unrestricted build at
`--safe-mode=safe` *fails*. So the restriction bites in exactly one situation —
**debugging a safe-mode regression skip** — where you would want a debug binary
that produces safe-build diagnostics, and cannot have one. Whether anybody has
wanted that is a question for cvc5, not for us. Our contribution is that the
list is this short, and that we can keep it this short.

## The invariant, and why it is the real subject

> **A safe build differs from an unrestricted build only in (a) the default
> value of the `safeMode` option, (b) the text of diagnostics, and (c) what the
> build reports about itself. No solver behaviour is gated on the build macro.**

**This invariant is what makes the configure restriction cheap.** While it
holds, refusing safe + debug denies a developer only the diagnostic text, and
the simplification pays for itself. If it ever stops holding — if some behaviour
becomes reachable in a safe build and not under `--safe-mode=safe` — then the
same configure line stops being a simplification and becomes a genuine
restriction, because no runtime flag substitutes for the build any more.

Nothing in cvc5 currently maintains it. It holds today by accident, and the
natural way to add a safe-mode restriction is `#ifdef CVC5_SAFE_MODE` around the
restriction, which would break it on the first use. **The invariant is worth
maintaining deliberately, and it is cheap to maintain**: it is a property of
eight lines that a check can read in a tenth of a second.

Keeping it also has a benefit beyond this question: while it holds, "safe mode"
is unambiguous. Every claim anyone makes about safe mode — ours included — is
true of both the build and the flag, and nobody has to say which.

## The check

```bash
python3 -m dokimasia.buildmode check <cvc5>    # BUILD0001
python3 -m dokimasia.buildmode sites <cvc5>    # every conditional, classified
```

It enumerates every `CVC5_SAFE_MODE` / `CVC5_STABLE_MODE` conditional and
classifies each as an option default, a diagnostic, or a build self-report. The
classifier is **closed**: anything it does not positively recognise is reported,
so a new conditional has to argue for itself rather than slip through. It also
fails if a source file becomes excluded from a safe build, or if anything starts
branching on `isSafeBuild()`.

One block — the hint selection in `illegal_checker.cpp` — is message-only but
computes *which* hint to print, which the classifier is too strict to see. It is
allowlisted with a hash of its contents, so editing it re-triggers review rather
than silently staying approved.

`tests/test_buildmode.py` checks that the verifier fires on each way the
invariant can break, because a checker nobody has seen fail is a checker nobody
should trust.

## What we would ask of cvc5

**Not a change to the configure script.** The restriction is a reasonable
simplification and we are not arguing against it; whether the one lost
capability — a debug binary with safe-build diagnostics — is worth a
combination in the build matrix is cvc5's call, and depends on whether anyone
has ever wanted it.

**What we would ask for is the invariant, maintained.** Run `BUILD0001` as a
[kind B](../findings.md) adoption: seconds, no build, no dependencies. Its value
is not the eight sites it finds today — it is that the ninth gets noticed, and
that the configure simplification keeps being free.

Better still if cvc5 owns it rather than us. The same property could be a
build-time test or an assertion in their tree, at which point our check retires.
That is the [kind D](../findings.md) outcome and we prefer it.

## Verdict

| | |
| --- | --- |
| **carry** | the answer to the question #12899 raised, with the check as evidence |
| rules it clears | `theirs-not-ours`, `run-it` (the diagnostic divergence is demonstrated, not argued), `cheap-to-refute`, `falsifiable`, `worth-the-attention` |
| falsified by | a `CVC5_SAFE_MODE` conditional that gates behaviour — which is what the check looks for; or a developer naming a use for safe + debug that the flag does not cover, which would make the restriction a real cost after all |

**What we are not claiming.** We have not built a safe build and compared
binaries. The equivalence argument is static and exhaustive over the eight
sites; the divergence we demonstrate empirically is the diagnostic text. A
direct A/B of a safe build against `--safe-mode=safe` over the regression suite
would settle it completely, and needs a build we do not have.
