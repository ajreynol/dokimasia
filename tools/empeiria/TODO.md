# empeiria — the plan

Nothing is built. This is the order the work would go in, so that a reader can
tell what is intended from what exists.

## First

- [x] **`run_empeiria`** — the interface. Run it from a cvc5 checkout with an
      issue number; it guards the tree, makes the branch, and hands a
      fix-first prompt to an assistant. `--record` and `--list` close the loop
      afterwards. Fixing is never gated on the ledger.
- [ ] **Work #12905 end to end with it.** Reproduce it,
      locate it, attempt a fix and a regression test. A ledger format designed
      before a single issue has been worked will be wrong in ways no amount of
      thinking finds — and an executor that has never executed does not know
      what it needs to record.
- [ ] **Revisit the ledger format after two or three real issues.** The shape
      `run_empeiria` writes today is a first guess made before any issue was
      worked, which is exactly the condition under which a format is wrong.
- [ ] **Decide what a delta is worth recording.** Every correction is a delta;
      only some teach anything. Guessing this in advance is how the ledger fills
      with noise.
- [ ] **Decide what "a fix" has to include** before one is offered to anybody:
      the patch, the regression test, the reproducer run before and after, and
      the build it was checked against. That is `run-it` applied to a diff, and
      it is the standing precondition rather than a per-case judgement.

## Then

- [ ] Enough cases to see whether corrections fall into a small number of kinds.
- [ ] A held-out set, fixed before any measurement, so goal 3 can be answered
      honestly rather than in hindsight.

## Not yet

- **Anything that delivers.** No branch pushed, no PR, no issue comment — see
  the charter. The artifact is a patch in a tree a person is driving.
- Anything that reads the tracker over the network. The parent's standing
  position is that an analysis whose result depends on when it ran is not a
  measurement, and nothing here needs to move faster than a person.
- Any automation of the response itself.
