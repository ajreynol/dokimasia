# Regression exclusion audit

`eo_cvc5_regressions_audit` reports which CLI regression files disable `proof`,
`cpc`, and `cpc-logos`, with source locations and reason comments. It needs
Python 3.10+ and a cvc5 source checkout, with no build or Python dependencies.

```bash
./scripts/eo_cvc5_regressions_audit
./scripts/eo_cvc5_regressions_audit --summary
./scripts/eo_cvc5_regressions_audit --tester cpc
./scripts/eo_cvc5_regressions_audit --cvc5 /path/to/cvc5 --json
```

The default command prints tester availability and counts, followed by every
excluded regression and its evidence. `--summary` prints just the status;
`--tester` is repeatable; `--json` prints the report and source evidence as JSON.
The command only reads files and prints to stdout. Exit status is 0 for a
completed audit, including one that finds exclusions, and 2 for unreadable,
missing, invalid, or unsupported inputs.

Checkout selection uses `scripts/targets.py`: `--cvc5`, `$DOKIMASIA_CVC5`,
`$CVC5`, `scripts/repos.local` (or `$DOKIMASIA_REPOS_FILE`),
`scripts/deps.local.json`, then `deps/cvc5`. The report names the actual checkout,
revision and working-tree dirty status. It never fetches or changes a checkout;
the repository's cvc5 pin does not override that selection.

## What the counts mean

- **Direct**: files with `DISABLE-TESTER: <tester>`.
- **Inherited**: files disabled through another tester, excluding files that
  already disable this tester directly. The audit reads the cascade from the
  selected `run_regression.py`; for example, `proof` currently also disables
  `cpc`. It does not assume that `cpc` disables `cpc-logos` or that the cascade
  is transitive.
- **Suite**: files in CMake's `regression_disabled_tests` list, which are
  excluded from the regression suite as a whole.
- **Total**: the union of those sets. Each file counts once, even if it has
  repeated directives or is both individually and globally disabled.

Every `.smt2` and `.sy` file under `test/regress/cli` is scanned, including
unregistered files. Counts describe files, not command-line variants. As in the
runner, directives must start with a semicolon in column zero; indented and
double-commented directives are ignored. Unknown tester names are errors.

Tester registration and default selection are read from the harness. When
`cpc-logos` is absent, it is shown as **planned (not registered)**, with no total
disabled count. If a selected checkout registers it, its direct and inherited
exclusions are audited using that checkout's rules.

## Reasons and limits

For each directive, the report retains adjacent prose comments on either side
of its consecutive block of disable directives. A comment that mentions proof
checking and an explanation of a restriction is labelled **Reason comment**;
other prose is labelled **Context**. This is a conservative text heuristic,
not an independent diagnosis. Each comment has its own source location so the
attribution can be reviewed. A nearby benchmark description is not sufficient
to establish a reason. Missing explanations remain **unknown**; command lines
are printed as additional context, without inferring unsupported options.

For CMake exclusions, comments immediately before an entry and inline comments
are shown as reasons. A preceding comment attaches only to the next entry;
the audit does not guess whether it describes a whole group of tests.

This is a source exclusion inventory. It does not evaluate tester `applies()`
predicates, `REQUIRES`, CI matrices, build configuration, or runtime tester
selection. A file with no disable is not necessarily tested, and an exclusion
does not establish a proof defect. CMake lists and Python tester registries
must use the literal forms supported by the parser. The harness is parsed as
syntax, never imported or executed.

Run the fixtures and optional checkout cross-check with:

```bash
python3 tests/test_regression_audit.py
python3 tests/test_regression_audit.py /path/to/cvc5
```
