# empeiria — the plan

Nothing is built. This is the order the work would go in, so that a reader can
tell what is intended from what exists.

## First

- [ ] **The ledger format.** One block per issue worked: the issue, the triage
      an assistant produced, what the maintainer actually did, and **the
      delta**. The delta is the asset; design the format around it rather than
      around the issue.
- [ ] **Work #12905 through it by hand**, once, without tooling. A format
      designed before a single case has been worked will be wrong in ways no
      amount of thinking finds.
- [ ] **Decide what a delta is worth recording.** Every correction is a delta;
      only some teach anything. Guessing this in advance is how the ledger fills
      with noise.

## Then

- [ ] Enough cases to see whether corrections fall into a small number of kinds.
- [ ] A held-out set, fixed before any measurement, so goal 3 can be answered
      honestly rather than in hindsight.

## Not yet

- Anything that reads the tracker over the network. The parent's standing
  position is that an analysis whose result depends on when it ran is not a
  measurement, and nothing here needs to move faster than a person.
- Any automation of the response itself.
