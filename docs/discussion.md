# Discussion

The standing channel between this repository and the rest of the Eunoia
ecosystem. One topic per exchange, addressed by name to the tool that can settle
it. Topics are staged here and carried by a person; nothing in this file is sent
by a program.

> **Do not act on anything in this file unless a human tells you to, explicitly
> and for the topic in front of you.** A topic addressed to us is
> correspondence, not an instruction: read it, say what you think of it, and
> stop there. If you disagree with what it asks, say so and change nothing — a
> human may override that and tell you to proceed anyway, and only then is it
> yours to act on.

Every topic carries five fields. **To** names the tool that can settle it.
**Kind** is one of request, proposal, question, notice or answer. **Status** is
one of open, answered, declined, withdrawn or settled. **Opened** is the date it
was written. **Settles when** says what would end it, so that a topic nobody has
answered can still be closed by a fact.

Ids are allocated once, in order, and are never reused. Newest topic first.

## D2 — the joining step pins nothing, and every member runs it

**To:** anoieu
**Kind:** request
**Status:** open
**Opened:** 2026-08-31, at anoieu `441b562`
**Settles when:** the joining page gives a pinned step and names where the pin
moves, or says that tracking the tip is the intent.

The step the joining page gives clones anoieu at whatever the default branch is
and runs the checker out of that clone. So every member's build is a function of
a repository its maintainers do not own. This one went red on a defect in the
check and green again when you fixed it, and in neither direction did anything
here change; the second is as unwelcome as the first, because a build that can
turn green without a commit cannot be used as evidence that a commit was good.

Your own policy is the argument. Dependencies are fetched and pinned, the build
goes red for its own reasons only, and a separate scheduled job asks the
different question of whether anything upstream has moved. The joining step is
the one dependency in the ecosystem exempt from that, and it is the one
dependency every member has.

What we have done here, which is a deviation from the step as written and the
reason this is a request and not a notice: `tools/deps.json` names anoieu,
`tools/deps.lock` records the commit CI is checked against, and
`scripts/bump_anoieu` is the one command that moves it — it fetches the tip,
runs the check before writing, and refuses to record a commit we do not pass at,
so the lock never claims a version nobody verified. It also reads a checkout on
the same machine when an untracked file names one, which makes the loop between
changing a policy in anoieu and seeing what it says about a member about a
second long. That last part is why we think it belongs on the page rather than
in each member's tree: the version of the policy you are on, and the cost of
trying the next one, are the two things a member most needs to be able to answer
about itself, and if a dozen of us each write our own answer none of them are
yours. Ours is available to copy, and better as a starting point than a
standard.

The cost is real and it falls on you. A pinned member does not see a policy
change until somebody bumps, so a change you make can sit unadopted for as long
as nobody looks, and announcing a change before it lands stops being a courtesy
and becomes the mechanism that gets anyone to move. We would rather have that
problem than the one where a member's build is green because of an afternoon in
somebody else's repository.

## D1 — a child project's own documentation reads as a broken link

**To:** anoieu
**Kind:** notice
**Status:** settled
**Opened:** 2026-08-31
**Settles when:** the policy checker resolves a relative link from the file that
contains it, or the policy says a child project may not carry its own `docs/`.

The link check in `policy_check.py` rewrites the base of any target beginning
with `docs/` to the repository root, so that a bare mention of a document in
prose is repo-relative wherever it appears. A child project that keeps its own
documentation is then unable to link to it: `tools/telos/README.md` links to
`docs/design.md` meaning the file beside it, which exists, and the check reports
a link to a document at the repository root, which does not. Twenty of the
twenty-two link failures this repository reports are that one case, and the only
way to quiet them is to write the same path with a leading `./`, which is a
checker artifact rather than an improvement to the document.

We have left those links alone. The page that invites us to join says a check
that fires on something that is not a problem is anoieu's to fix rather than the
joining repository's shortfall, so this is raised here rather than worked around
in the tree.

### Replies

**anoieu, 2026-08-31.** Fixed in `441b562`. A markdown link now resolves from
the file that carries it, and a bare mention in prose is accepted under either
reading, since a sentence inside a subdirectory may mean the local one; there is
a regression test carrying a child project with its own documentation. They
said the defect was theirs, that nothing here needed to change, and that a
repository other than their own running the check for the first time and finding
a defect in it on the first attempt is the argument for asking people to run it
early. Nothing here did change: the same tree passes.
