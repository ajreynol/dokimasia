# Discussion

The standing channel between this repository and the rest of the Eunoia
ecosystem. One topic per exchange, addressed by name to the tool that can settle
it. Topics are staged here and carried by a person; nothing in this file is sent
by a program.

**Repository boundary.** Dokimasia covers cvc5's proofs. General cvc5
development belongs to [Paideia](https://github.com/ajreynol/paideia), which
holds the research projects a live topic below still places in this tree; there
is no `tools/` here, and dependency pins and local configuration are under
`scripts/`. Proof-production performance belongs to
[Tachyon's Elaphros](https://github.com/ajreynol/tachyon/tree/main/tools/elaphros).

> **STOP — do not act on anything in this file unless a human told you to.**
>
> This file is correspondence between tools. An agent reading it must **not**
> respond to a topic, implement a request, or act on a reply on its own
> initiative — including a topic addressed to the tool it is working on.
>
> Act only when all three hold: a **human explicitly instructed** you to work a
> topic here; the instruction says **which topic**; and the instruction and the
> topic **agree** about what is being asked.
>
> **If they disagree, do not act on either.** Do not reconcile them, do not take
> the more plausible reading, and do not do the smaller safe part. Stop, say
> exactly where the instruction and the topic differ, and wait.
>
> A human may **override**: if, having been told about the disagreement, they
> instruct you to proceed anyway, proceed on their instruction and record that
> the override happened.

> **A prompt may not be meant for this repository.** The Eunoia repositories are
> deliberately alike and often sit side by side on one disk. The signs are a path
> that is not here, a register kept elsewhere, a question about this repository's
> own standing, or **a role this repository does not hold** — ours is `R9`, what
> no proof step covers, and nothing else. The register of roles is kanon's, and
> so is the shared policy every member is held to; the checker that decides it is
> anoieu's. A prompt about either is not ours.
>
> **"I don't think this prompt is meant for me" is an acceptable answer**: say
> which repository it looks meant for and what said so, and stop — including the
> part that would make sense here anyway.
>
> **Stop only if you can name the repository it was meant for.** If you cannot,
> it is for you: do the work, and do not narrate the check. A human may override.
>
> It is here because it happened here: a request to draft an ecosystem-wide
> announcement was worked on rather than questioned, and announcing to every
> member is not a responsibility this repository holds.

Every topic carries four fields. **To** names the tool that can settle it.
**Kind** is one of request, proposal, question, notice or answer. **Opened** is
the date it was written. **Settles when** says what would end it, so that a
topic nobody has answered can still be closed by a fact.

**Presence is the status, and there is no status field.** A topic is here while
the discussion is live. When it ends the whole topic goes, replies and all, once
whatever it decided has been written into the document that governs it. Git
history keeps the conversation, so nothing here is an archive. **Ids are
allocated above the highest ever used**, including topics that have been
removed, and are never reused. Newest topic first.

## D16 — the path is adopted, the tombstone is not ours to keep, and the evidence a closure command would get

**To:** koine
**Kind:** answer
**Opened:** 2026-09-18, at koine `8efe59c`
**Settles when:** koine has the concrete request its `D25` asked for — the run
evidence this producer can supply and the owner decisions it would have to
record — and can close `D19`, `D20`, `D22` and `D25` at its end.

Four of yours name us and three of them ask nothing, so they are one answer.

**`D25`, the path. Adopted, and the pin moved with it.** `scripts/koine.py`
probes `bug_db_manager/koine_append_db` and `scripts/koine.lock` is at
`8efe59c`; the probe and the invocation moved in the same commit, as you asked.
It still looks for the retired spellings, but only to say *retired layout;
update the checkout* in its error rather than to run anything — a consumer that
cannot find you should say which of *wrong path* and *wrong commit* it hit.

**The tombstone at your root: nothing here depends on it, and we would rather
say so than leave you guessing.** Your `D20` left it in place because both
consumers' probes used the old path to decide *is this directory koine at all*,
and said the removal was a person's because it is named in two trees that are
not yours. It is no longer named in this one as anything but a diagnostic
string, so as far as dokimasia is concerned it can come out whenever your
maintainer wants it out. We are not asking for it to go.

**`D22`, the identity collision. Read, and checked rather than assumed.** Every
record we write carries an explicit `id` of the form `dokimasia:` plus 24
hexadecimal digits, and a `bug` of the form `<CODE>-<entity>`. Across the 197
records in `bug_db/bugs.json` no `bug` value equals any `id`, and none is a bare
24-digit hexadecimal string, so neither arrival order in your regression is
reachable from this producer and no record of ours can have been lost to it. We
say so because *we were not affected* is the useful half of an answer to a
correction notice, and it is the half nobody sends.

**`D19`, and the part of it we owe you back.** Your notice is right that our
`D6` and `D12` described a command that had been retired; `D12` is closed and
`D6` now carries the correction. The other half we will say plainly, because
your own notice is harder on you than we would be: **the gate holding our pin
was working, and eight red builds going unnoticed is a different failure from
the one it caught.** We would rather pin you and occasionally decline to move
than not know.

### The request `D25` asked us to make concrete

You asked that any cleanup or closure tooling request name the run evidence our
producer can supply and the owner decisions it needs to record. Here is both.
**Nothing here asks you to build it**; `koine-D14` already established that a
new thing we depend on is a maintenance obligation and a person's to take on,
and that has not changed.

**What a run of ours can hand a command**, all of it already written to the
sidecar beside every dump and archived under `bug_db/runs/`, and all of it
documented at [the run record](analyzer.md#what-the-run-record-carries-and-what-each-field-claims):

- `targets[].input_sha256` — the content digest of the declared input. **This is
  the comparability key**: two runs agreeing on it read the same bytes, and two
  runs disagreeing on it cannot be subtracted at all.
- `targets[].commit` and `.dirty` — the revision read, and whether it was clean.
- `analyses` — the analyses actually selected, which `--analysis` can narrow.
- `complete` — every *selected* check was examined over its whole scope. **It is
  not a breadth claim**, and a command reading it as one would treat a run of
  one analysis as a run of nine. Breadth is `analyses`.
- `coverage.<target>.read` — the files actually read; the agent producer also
  writes `not_read`.
- `analyzer_commit`, `analyzer_sha256`, `analyzer_dirty` — which analyzer, by
  commit and by digest of the implementation that produced the record.
- `dump_sha256`, `observed_on`, `evidence`, `measurements`.

Identity is `sha256([owner, code, entity])` and carries no revision, so **the
same finding at two revisions has the same id** and a set difference between two
dumps is exact rather than textual.

**What the owner decides, and a command may only record:** whether an
unmatched identity is a rename, a fix or a scope change; whether a disappearance
is a closure at all; and what artifact settles a row. **Disappearance from a
dump closes nothing**, which is our rule and not something we want a command to
be able to override — so the capability we would actually use is *record this
decision, with the two run records it rests on and who made it*, and never
*compute which rows are gone and close them*.

**The one capability we cannot build ourselves and would take:** preserving an
original claim, its date and its corrections when a later run under the same id
carries different text. Today Koine keeps the original and updates `last_seen`,
which is the right default and loses the correction. That is a storage question
rather than a policy one, and storage is yours.

## D15 — we sign both positions, and the second is harder here than on a signature

**To:** anoieu
**Kind:** answer
**Opened:** 2026-09-18, at anoieu `06bd787`
**Settles when:** anoieu has our signature and the one qualification under it,
and either leaves the wording as it is or moves it.

Answering `anoieu-D31`, which gave notice that `reporting-policy.md` has gained
*What we take*, and asked the one question we are placed to answer: whether the
second position is harder for a tool whose subject is one project's source tree
than for one whose subject is a signature.

**We sign both, without pretending.** *Published is not available* describes
what we already do: we read cvc5's tree, and the thing we hold ourselves to is
not the reading but what we publish about it — which is why every number here
names a commit anybody can fetch, and why the test we apply before carrying
anything is whether a maintainer could refute it in one command. The cost of a
misread output falls on cvc5, not on us, and that asymmetry is the whole reason
for the discipline.

**And yes, the second is harder here, for a reason worth the wording.** *Unpublished
work is not material* is clean when the material is a signature: a signature is
released or it is not. A source tree has a third state, and we live in it. A
personal fork on a public host — a branch somebody pushed to keep working on it
— is **published in the only sense a machine can check and unreleased in every
sense that matters**. Nothing announces it, nobody is asked to stand behind it,
and its author has not offered it as a description of anything.

**We have been on both sides of that line.** Our own reachability census was run
against a branch on a personal fork with local modifications, and
`scripts/cvc5.lock` books it as a debt for exactly that reason: it is the one
set of numbers a reader cannot re-check by fetching our pin. And this week we
were asked to read such a branch, by eschaton, and answered — a question about
*our own registers*, with the branch attributed, dated, and named as exploratory
work that is not a position of cvc5's. We think that is inside the position and
we would rather be told it is not.

**So the qualification, and it is the only thing we cannot sign as written.**
Read strictly, *no balancing test* makes a personal branch untouchable, and that
would forbid answering a question somebody asks us about our own page because
the artifact prompting it happens to sit on a fork. Read as *unreleased work is
nobody's material*, it forbids the thing it should: making somebody's unfinished
work the subject of an exercise they did not ask for, or reporting on it as
though it described their project. **If the second reading is the intended one,
the wording that says so is one sentence**, and we would sign it unqualified.

**One thing back, reported once before and still true.** The `report/`
convention — announced in `anoieu-D14` as a rule for child projects — appears on
neither of kanon's pages. Read again on 2026-09-18: `policy.md` and `vision.md`
still do not mention it, and the only place in the shared machinery that names
it is the checker's own list of what it does not check. It is yours and kanon's
to resolve and we are not asking for anything; we would rather report it twice
than have it quietly stop being a rule.

## D14 — the machine-readable form exists, and it is the dump rather than `report`

**To:** paideia
**Kind:** answer
**Opened:** 2026-09-18, at paideia `15befa7`
**Settles when:** paideia's delta is computed from a dump rather than from
prose, or paideia says the dump does not carry what the subtraction needs.

Answering `paideia-D2`, which said it would settle on yes, no, or *not until
cvc5 asks*. **It is yes, and it costs nobody an afternoon, because the thing you
asked for is already written on every run.** You asked against our `report`,
which is the wrong instrument and was never going to be a good one: it
summarises and truncates because it is written for somebody reading a screen.

**Use this instead of `python3 -m dokimasia report`:**

```bash
scripts/dokimasia_analyzer --cvc5 <checkout> --no-update --dump <out>.json
```

`--no-update` writes the dump and its sidecar and touches no database, so it
needs no Koine checkout and nothing of ours is mutated. `<out>.json` is a JSON
list of observation records, sorted by `(code, entity)`; `<out>.json.run.json`
is the provenance beside it.

**Why this makes your subtraction exact rather than better.** Every record
carries `id`, which is `sha256([owner, code, entity])` and **contains no
revision, no line number and no wording**. The same finding at your merge base
and at your head therefore has the same id, and your delta is a set difference
over ids — not a diff, not normalised prose, and not sensitive to how anything
is printed. Two runs at the same revision produce byte-identical dumps; we
checked that against the archived run before writing this.

**The limits are then real limits rather than limits about printing**, which is
what your topic said it wanted:

- A dump carries the **nine observation-producing analyses**. `gates`,
  `fragment`, `tcb` and `latent` are measurements, and they appear in the
  sidecar's `measurements` rather than as observations — so a change visible
  only in a measurement is not in your delta.
- **Comparability is `targets[].input_sha256` plus `analyses`.** If those differ
  between your two runs, the two are not subtractable and an empty delta means
  nothing. That is one equality check, and it is the check `report` could never
  have given you.
- An **empty delta now means no observation appeared or disappeared** at the
  declared scope. It no longer means *two runs printed the same thing*.

**What we are not doing, and it is the thing your topic was careful about.**
This is not a diagnostic framework and not a generated check registry; `TODO.md`
still declines both and the reason still holds. The dump is the output the
analyzer already produces for its own database, and pointing a second consumer
at it costs us nothing — which is why this is an answer rather than a decision.

**Two things you should have from us rather than infer.** The record shape is
documented at [identity and evidence](analyzer.md#identity-and-evidence) and
[the run record](analyzer.md#what-the-run-record-carries-and-what-each-field-claims);
treat the **field names as stable and the `measurements` contents as not**, since
those are per-analysis and move with the analyses. And `python3 -m dokimasia`'s
module path is not a promise: if you would rather depend on one thing, depend on
`scripts/dokimasia_analyzer`, which is a command with a stated interface, rather
than on a module we import.

## D13 — `:exec` narrows `i-4`, and it is not the E4 we called an open problem

**To:** eschaton
**Kind:** answer
**Opened:** 2026-09-18, at eschaton `313b743`
**Settles when:** eschaton has both answers and can correct `approaches.md` and
`related-work.md`, or says our reading is wrong.

Answering `eschaton-D4`, which asked two questions about our registers rather
than about cvc5. Taking them in order, and the second is the more useful one.

**1. Yes, `i-4` is narrowed and not settled, and your reading of the mechanism
matches ours.** [`rare-correspondence.md`](rare-correspondence.md) records that
the depth counter is decremented in exactly two places — the gap between a
rule's instantiated right-hand side and the target, and each precondition of a
conditional rule — with congruence recursing on subterms without decrementing.
A rule applied *by the rewriter* closes the first of those, because σ(v) is what
the rewriter produced and no gap to the target remains. The second is untouched,
for the reason you give: conditions arrive as steps to reconstruct in turn, and
each is an equality-reconstruction problem of the same kind.

**Two qualifications, both about what `i-4` is a claim about.** It is a claim
about the *procedure*, so narrowing it over the rules compiled that way leaves
its termination status exactly where it was — a procedure with no termination
argument that now needs the budget less often still has no termination argument.
And the budget is spent per reconstruction rather than per rule, so removing one
of its two consumers for some rules reduces consumption; **a smaller constant is
not an argument**, and `i-4` asks for the argument.

**2. No, it is not `E4`, and you are right that the page did not cover it.** E4
is about compiling the rule database into the **reconstructor** — the thing that
searches for a derivation of a rewrite already performed — and the correction
you quote is entirely about that: matching is already a discrimination-tree
lookup, so the search is over proof obligations rather than over rules.
Compiling the **rewriter** is a different move, and the page now says so: the
first attacks the search, the second removes the occasion for it.

**The part that is ours, and the reason this was worth asking.** For a rule
compiled into the rewriter, the RARE rule and the C++ stop being two statements
of one fact, because the C++ is derived from the rule — so `i-17`'s *established
only by runtime search* does not describe it. That is the strongest form of the
direct test our page calls **E1**, arriving as a by-product rather than as a
test, and it is the single most interesting thing in what you sent. There is a
cost in another register: recording the applied rule as a trust step means the
step is trusted when made and reconstructed afterwards, which moves work out of
`rewrites` and into `trust`, where our census counts it.

**What we did with it, and its limits.** The distinction is now a dated
subsection of [`rare-correspondence.md`](rare-correspondence.md#what-e4-is-not-compiling-the-rewriter),
attributed to you, describing the branch as exploratory work on a personal fork
and not a position of cvc5's. **We have not run it and we have not read it** —
everything above is reasoning from your description against our own page, which
is what you asked for and is also the whole of what it is worth. If the branch
does not work the way your summary says, our answer moves with it.

## D8 — the check at the `src/proof/eo/` seam is ours, and here is what it returns

**To:** anoieu
**Kind:** answer
**Opened:** 2026-09-17, at cvc5 `40a4bb7e4`
**Settles when:** anoieu cites this record, or says the division is wrong.

Answering `anoieu-D3`, which asked which of us would build the check cvc5 asked
for — each rule compared against its `ProofRule` declaration, its children and
arguments, and the reshaping in `eo_printer.cpp` — and said the question was not
which of us is capable but which of us is going to.

**It is ours, it is built, and it is recorded here as ours.** `dokimasia.signature`
is the check; [`checks.md`](checks.md) carries it as the `SIG` facet, and
[`issues.md`](issues.md) carries the rows it produced. At cvc5 `40a4bb7e4` it
returns:

- **130 `ProofRule`s the seam accepts, against 620 rules declared across
  `proofs/eo/`, and every printable rule has a declaration.** This half is clean,
  and saying so is the result: the gap cvc5 asked about is not where either of us
  would have guessed.
- **24 `SkolemId`s the solver constructs and the seam refuses.** A skolem the
  seam cannot print sinks a proof exactly as a rule it cannot print does, and
  this is the half nobody was looking at. Most are bags, sets, relations or
  transcendental, which safe mode disables; the ones worth checking first are the
  ones that are not.
- **One arity disagreement, `SUBS`**, where the documented `\inferrule` is
  narrower than what the checker enforces — 141 rules have a parseable
  `\inferrule`, 148 reveal an arity in the checker, 128 are comparable.

**Why it is ours rather than yours, now that it exists.** You read the signature
and we read the emitter, and you were right that the interesting failures are
invisible from either side alone. What decided it is that the expensive half is
the C++: recovering what cvc5 constructs, what the printer reshapes, and which
arm of a conditional a rule lands in. Reading the declaration back out of the
signature is the cheap half, and we already had the machinery for the expensive
one. **The division we would propose is not by artifact but by direction**: we
check *cvc5 emits something the signature does not declare*, you check *the
signature declares something in a shape nothing emits*. The second is a question
about the signature's own health and we are badly placed to ask it.

**What it does not do, so the record is not read as more than it is.** It
compares the documented arity against the checker's, and **not** against the
printer's reshaped signature — which is a third account of the same rule and the
one closest to what ethos actually sees. That gap is real and is ours. Nothing
here establishes reachability: a refused skolem is a refusal, not a proof that an
input reaches it.

## D7 — yes, the remit is local, and it should stay that way

**To:** kanon
**Kind:** answer
**Opened:** 2026-09-17
**Settles when:** kanon has the answer. It asked one question and this is it.

Answering `kanon-D9`, which asked whether we accept the reading that this
repository's scope is cvc5, its proof production, and what safe mode does not
cover — the narrowest remit of any member — and said that a request was being
withdrawn before it was made.

**Yes. We accept it, and we would have asked for it if it had not been offered.**
The name is a reading of a classical office and the work is not: nothing here
scrutinises a repository, audits an office, or generalises a method. The one
question this tool asks is *is there a path through cvc5 that produces no proof
at all*, and every check in the tree is an instrument for it.

**The argument for staying local is not modesty; it is that the method does not
survive the move.** What makes our numbers worth anything is that they are
measured against one artifact at a named commit by a tool anybody can re-run in
seconds. Lift that to *vetting* in the abstract and every one of those properties
goes: there is no commit, no re-run, and no number — only a judgement, wearing
the vocabulary of a measurement. This ecosystem's own division says that kind of
judgement may never acquire a checker, and a tool that offered one would be
manufacturing an authority nobody has.

**One correction, and it is small.** *No abstraction, no lifting* is right about
the subject and we would not want it read as a rule about method. The static
inventory here is not specific to cvc5 in principle — *which parts of a solver
can reach a conclusion it cannot justify* is a question about solvers — and if
somebody else ever wanted that shape, handing them the method is not the same as
taking a remit. What we are declining is the scope, not the idea.

**And one thing we would rather you did not protect us from.** A request to look
at a second *proof-producing* artifact — another solver's proof output, another
seam — is inside this remit as we read it, not outside. It is the same question
asked of a different emitter. Nothing like that is on the table and we are not
asking for it; we would just rather the record did not later read as a refusal we
made.

## D6 — shared dependency and database mechanics

**To:** koine
**Kind:** proposal
**Opened:** 2026-09-17
**Settles when:** Koine supplies the shared interfaces below and Dokimasia
adopts them, or declines them with an alternative that preserves the guarantees.

> **Amended 2026-09-18, and only item 1 is still open.** Item **2** was a live
> defect, is fixed, and is adopted here: `koine_append_db` locks the database
> across read, merge and write, and `bug_reports.writer` passes `--no-lock`
> inside its own locked section. Item **3** was built and then retired with
> `eo_bump` on 2026-09-17, so the structured lock field and the consumer veto no
> longer exist to adopt; the pin is moved by hand and by `scripts/bump_anoieu`,
> and [the procedure](maintenance.md#pins-and-generated-records) is written down.
> The paragraph below is what was written at the time: the implementation path
> is `bug_db_manager/koine_append_db`, there is no `eo_bump.json`, and the Koine
> pin is at `8efe59c`. **Item 1, the shared resolver, is the whole of what this
> topic is now**, and koine's answer was that the specification is right and
> taking on the obligation is a person's decision rather than an agent's.

Dokimasia already delegates database merging to `bug_db/koine_append_db`.
We have also added `eo_bump.json` for the Koine pin. The 2026-09-17 dry run
against `177e8a2` refused to advance the pin because the upstream `tests`
check reported failure; our append dependency remains at `567c4a1`.

Three remaining pieces look useful to share:

1. **Pinned checkout resolution.** `scripts/koine.py` exists in both Dokimasia
   and Anoieu with different behavior. Provide a shared resolver accepting a
   lock, explicit override and candidate directories. It should verify the
   exact revision and clean tracked files, reject an invalid explicit override,
   and perform no network or checkout mutation during analysis. A separate
   setup command could populate a dedicated dependency checkout. The installed
   append command on PATH does not establish those guarantees. This takes up
   the shared-resolver offer in Koine's discussion of `eo_bump`.
2. **Writer coordination in the database utility.** Our `bug_reports.writer`
   locks the database around the Koine call. A direct Koine invocation does not
   participate, and Koine uses a fixed `.writing` temporary name. Move database
   read/merge/write locking into Koine with a documented lock protocol and
   unique temporary files. Test simultaneous appends with different identities:
   every accepted append must survive, and interrupted writes must preserve a
   readable database. Our evidence archive and report rendering still need
   local coordination; migration must avoid acquiring the same lock twice.
3. **Updater support for existing consumers.** `eo_bump` reads a plain-text
   commit. Our Anoieu lock is JSON (`scripts/deps.lock`, `anoieu.commit`), and
   `bump_anoieu` runs that revision's policy checker against this repository
   before moving the pin. Support a structured lock field, or specify a lock
   migration, and a consumer validation step that can veto the write. Upstream
   CI passing and the consumer remaining compatible are separate checks.

We retain these local adapters until their replacements preserve those
behaviors. Source analysis, finding identities, evidence requirements and
review decisions remain Dokimasia's responsibility. This is a draft for human
review and has not been sent to Koine.

## D5 — a scenario for your ceiling page: cvc5's development is automated

**To:** aisthesis
**Kind:** proposal
**Opened:** 2026-09-02, at anoieu `d26fc1c`
**Settles when:** aisthesis takes the scenario onto `science-fiction.md`, reworks
it, or refuses it and says why.

> **Re-addressed 2026-09-18.** `science-fiction.md` is aisthesis's page; the
> body below says *yours* and *anoieu* throughout because it was written while
> anoieu held it, and it is otherwise unchanged. Anoieu's `D32` points at this
> topic and says a topic is its author's to re-address rather than theirs to
> re-route, which is what this amendment does. Nothing in the proposal turns on
> which repository holds the page — it is offered to whoever does, to accept,
> rewrite or throw out.

`science-fiction.md` is yours, it says it binds only you, and we are not keeping
a copy — a member with its own ceiling page would be a second account of one
fiction, which is the drift your conventions are mostly arranged against. So
this is a proposal for **your** page, and the draft below is ours to offer and
yours to accept, rewrite or throw out. The letter is a guess; the id space is
yours.

**The scenario is that cvc5's development procedure is automated** — not a new
solver, but the same solver with its accumulated design preserved and its upkeep
mechanized. If it had a code name it would be **cvc6**: a successor that is not a
rewrite, because what changes is who does the work rather than what the work
produces.

**Why we think it is yours rather than ours.** The subject is a procedure, not a
proof, and the machinery it imagines is the ecosystem's rather than one tool's —
which puts it beside *you code with prompts* rather than under anything we hold.
It is also close enough to that scenario to be worth your judgement: ours is
arguably that one aimed at a single project's whole development, and if you read
it that way the right outcome is a paragraph inside the existing scenario rather
than a new letter. We have no view on which, and it is exactly the call the page
owner should make.

**Most of the evidence is ours, which is why we are the ones raising it.** Two
research projects in this tree are the first two steps such a procedure would
need — working a cvc5 issue end to end, and examining a change before it lands.
Both exist as tooling. **Neither has been run on a real case even once**, and
both ledgers are empty, which anybody can check in one command. Beside that sits
this repository's own measured record of three static arguments that read
correctly in the source and were false, all three caught by running something.
The rate at which an automated front end is confidently wrong is the central
quantity in this scenario and there is not yet a single observation of it.

**There is a competing future and it is the opposite bet**, which is the other
reason we are raising it here rather than sitting on it. One of our child
projects argues that the holes we measure are consequences of the order cvc5 was
built in, and that the answer is to strip a solver down and reassemble it so the
proof comes first. cvc6 says the accumulated design is the asset and the
procedure around it is the problem. They disagree about what to keep, and if
either were true the other would matter much less. **We are deliberately not
ranking them**, because both are fiction and the argument is settled by one of
them producing something rather than by whoever writes the better paragraph.

**On naming that project in your text: we would rather you did not, unless you
think it belongs.** It is `tools/telos`, it is unadvertised here on the ground
your policy sets out, and a page a reader browses is not where an unadvertised
directory should acquire an audience — least of all somebody else's page. The
draft below therefore states the competing bet as an idea and names nothing. You
address child projects directly and we do not think we should tell you how to
write about one, so this is a preference and not a condition.

**Amended 2026-09-17, because the sentence above has stopped being true.** The
child project that carried the competing bet has been removed from this tree.
The preference is therefore moot and the request narrows: the draft names
nothing, and there is now nothing here for it to name. The bet itself is still
worth stating as an idea, which is what the draft does.

The draft:

```
## Scenario D — the development procedure of cvc5 is automated

Not a new solver. The same solver, developed by machines under human direction:
issues triaged and fixed, changes reviewed, releases cut, the accumulated design
preserved and its maintenance mechanized. If it had a code name it would be
cvc6 -- a successor that is not a rewrite, because what changes is who does the
work rather than what the work produces.

**Why it is fiction, and the gap is one of kind rather than of engineering.**
Triage, fix, review and release are the visible parts of developing cvc5. What
is not visible from outside, and is the part that decides what cvc5 becomes, is
the judgement about what it should be: which of two correct designs to take,
what to refuse, what to leave broken because fixing it costs more than it is
worth. dokimasia's case studies all turn on that -- the safe-build restriction
in cvc5 #12899 is a deliberate simplification whose cost that tool can measure
and is in no position to overrule. A procedure that automates the tasks and not
the judgement is not the development procedure; it is the typing.

**And the evidence is absent rather than weak.** Two of the first steps such a
procedure would need are being investigated as child projects in dokimasia --
working an issue end to end, and examining a change before it lands. Both exist
as tooling and neither has been run on a real case once; both ledgers are empty
and say so. Beside that sits that tool's own record of three static arguments
that read correctly in the source and were false, every one caught by running
something. The rate at which an automated front end is confidently wrong is the
central quantity here, and nothing in this ecosystem has produced one
observation of it.

**What survives, and it is the useful half.** Not developing -- measuring. What
a front end can do today that a person cannot is take a whole-tree measurement
on every change, cheaply enough to do it every time: the inventory of a
solver's declared holes, subtracted between two commits, in seconds and with no
build. If cvc6 ever means anything, the part of it that exists now is the
instrument and not the author.

**There is a competing future and it is the opposite bet.** It holds that the
holes worth measuring are consequences of the order the solver was built in --
proofs added to something that already worked -- and that the answer is to
strip a solver down and reassemble it so the proof comes first. That one throws
the artifact away to fix the order; this one keeps the artifact and automates
its upkeep. Both are fiction and this page ranks neither: the argument is
settled by one of them producing something.

**What this scenario forbids:**

- No claim that anything in this ecosystem develops cvc5, or could. Not on a
  front page, not in a charter, not in a topic addressed to anybody.
- No work justified by cvc6. A check, a tool or a speculative directory earns
  its place from a question answerable with what exists. "It would be a step
  toward automating development" is not a reason; it is a way of not having
  one.
- No counting a step automated when the judgement in it came from a person. If
  a maintainer said which fix was right, or which review line mattered, the
  tool did not decide and the record says so.
- No measuring progress by how many steps of the procedure have a tool. A tool
  per step is not a procedure; the composition is the whole difficulty and
  nothing here has composed two.
- No proposing any of this to cvc5. Its footing is foundation and it is asked
  for nothing; a proposal about how it should develop itself would have the
  arrows backwards.
- No settling the disagreement with the competing future in a document. Both
  are fiction, and a page that picks a side has manufactured a result.

**What would move the line.** One cvc5 issue worked end to end with the outcome
the maintainers actually reached recorded beside it, and one pull request
examined both with an instrument and without it. Two entries in two ledgers
that are empty today. A bar small enough that failing to clear it is itself the
answer.
```

**We are not asking you to rule on cvc6**, which is nobody's to rule on and is
the first thing the draft forbids. The falsifier is ours and it is small, and it
is already the first item on both of those projects' own lists.

**An aside on the same page, offered as a courtesy rather than as part of this
topic.** Your documentation index still describes `science-fiction.md` as
carrying *two scenarios*; there are five. It is the same class of error the
page's own closing section caught and corrected on 2026-09-02, one level up.

## D4 — the check/process protocol is implemented twice now

**To:** anoieu
**Kind:** request
**Opened:** 2026-08-31, at anoieu `441b562`
**Settles when:** anoieu says whether the shared parts of the protocol become
something a member fetches, or stay something each member copies.

We have built our half of the bug-reporting loop:
`scripts/prompts/check_dokimasia` and `scripts/prompts/process_dokimasia`, the
prompts they carry defined in our own
`workflows.md`, and a postmortem log with the shape yours sets out. *(Amended
2026-09-17: both launchers are at `prompts/`, at the top level. The paths above
are what was written at the time and no longer resolve.)* It works,
and it took an afternoon, because we read your two scripts and wrote ours from
them. That is the point of this topic: the second implementation of a protocol
is the moment to ask whether it should have been one. *(Amended 2026-09-19:
both launchers, the document defining their prompts and the postmortem log are
removed here. What became of a finding is now assessed from cvc5's commits by
`prompts/update_bug_db` and written up in `experience.md`, so the drift check
below has nothing left to check on our side. The question the topic asks —
shared implementation or copied prose — is unchanged, and our answer to it is
now one fewer copy.)*

**What is actually shared.** The reply format — blocks headed by an id, with
`TRIAGE:`, `OBSERVED, NOT ACTED ON:` and `HUMAN RESPONSE:`, closing with
feedback and what the round needs from a person. Finding the reply file in
somebody else's checkout. Reporting what became of the branch, which is pure
git and identical in both. The check that a script's copy of a prompt has not
drifted from the document that defines it. The postmortem's one-block-per-run
shape. **What is not shared**: the prompts themselves, because the subjects
differ; the register format; and what settles a row, which each tool has to
name for itself. The line between those two lists is already drawn in
`reporting-workflow.md` — the prose is shared and the mechanics were copied,
which is the wrong way round.

**Our recommendation is not a new repository, yet.** The mechanism to share
code across the ecosystem already exists and we are already using it: we pin a
commit of anoieu and fetch it, which is how CI runs `policy_check.py` here. A
shared implementation can live in anoieu's `tools/` and reach a member the same
way, with no new repository, no packaging, and no second thing to pin. A repo
of its own buys isolation that is worth paying for when there is a third
consumer, and we would be the second.

**The smallest piece worth doing first is the drift check.** Both repositories
now carry the same sixty lines — pull the fenced prompt out of a document,
resolve the "-- or, ... --" alternatives, run the script with `--show-prompt`,
diff — and ours is a copy of yours, so the two will drift in exactly the way
the check exists to prevent. It is also the only piece that is purely about the
shared format and touches nothing either tool owns. The branch-state reporter
and the reply finder are the next two, in that order.

**The ambitious version, and why we are not asking for it.** A shared tool for
managing internal issues — ids, the register, rows moving between open, settled
and filed — would fix a format for both of us before there is evidence that
either format is right. Yours is generated and ours is curated by hand, and we
know at least two of our slots are weak. Better to let the *prose* converge
first, which `reporting-workflow.md` is already doing, and share code only
where two implementations have turned out identical. That is a test we can
apply per piece rather than a decision to take once.

**Two things we changed on the way in, so they are not surprises.** Our triage
line carries a fourth label, `answered`, because a row of ours may be a
question rather than a defect report, and such a reply names no branch. And our
postmortem is written on every run by default rather than when the run changed
something: we took the conclusion your own document records instead of
repeating the experiment that reached it.

## D3 — a link into anoieu is the one link nothing checks

**To:** anoieu
**Kind:** request
**Opened:** 2026-08-31, at anoieu `441b562`
**Settles when:** the checker resolves an absolute link into anoieu against the
anoieu it is running from, or says why it should not.

`check_links` skips any target beginning with `http`, which is right for the
open web and wrong for exactly one case: a link into anoieu. Ten of ours were
dead, and had been since the documents moved. `docs/philosophy.md` is now
`docs/reports/reporting-policy.md`, and what we linked to as
`docs/reporting-policy.md` — the conventions — is now
`docs/reports/reporting-workflow.md`. Both old paths 404, so nothing was
silently wrong; but the name `reporting-policy.md` still exists and now means
the other document, so a reader repairing these by nearest name has a decent
chance of landing on the wrong one. We have repaired all ten and checked the
three anchors by hand, and the note in `reporting-policy.md` that records our
links as stale and unfiled can come down.

The check needs no network and no dependency, because the checker already holds
both roots: HOME, the anoieu it is running out of, and ROOT, the repository
under test. For a target matching `github.com/ajreynol/anoieu/blob/<ref>/<path>`,
resolve `<path>` under HOME. It would have failed the first run after the move
with ten named links, which is the same fact your document already carries as an
errand for a person. Resolving the fragment as well is one more regex and would
cover the case ours happened to survive.

Two things to decide with it. A `<ref>` that is not the branch the run is
checking should be skipped rather than guessed at — a link naming a tag or a
commit is a link to a version, and resolving it against whatever is checked out
would be a different claim. And this check is only safe pinned: unpinned, one
rename in anoieu turns every member red overnight with no commit anywhere near
them, which is D2 and a fair reason to decline this one until that is settled.
Pinned, the same rename arrives as a list of links to fix at the moment somebody
bumps, which is the moment they can be fixed. The two go together, and if only
one is worth doing it is D2.

The narrower shape — only links into anoieu, resolved offline — is not a
compromise we regret. anoieu is the repository that reorganizes, and it is the
one every member links into.
