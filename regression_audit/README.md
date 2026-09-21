# Regression exclusion audit

`eo_cvc5_regressions_audit` reports which CLI regression files disable `proof`,
`cpc`, and `cpc-logos`, with source locations and reason comments. It needs
Python 3.10+ and a cvc5 source checkout, with no build or Python dependencies.

```bash
./scripts/eo_cvc5_regressions_audit
./scripts/eo_cvc5_regressions_audit --verbose
./scripts/eo_cvc5_regressions_audit --summary
./scripts/eo_cvc5_regressions_audit --tester cpc
./scripts/eo_cvc5_regressions_audit --cvc5 /path/to/cvc5 --json
```

The default command prints one table row per excluded regression, with separate
`proof`, `cpc`, and `cpc-logos` columns and a short note. `yes` means the file
literally contains `; DISABLE-TESTER: <column name>`. Cells show `no` for no
directive, and `--` for an inherited disable or an unregistered tester. A direct
directive takes precedence. Only regressions with relevant tester directives
are listed; suite-wide CMake exclusions are outside this tool's scope.
Paths are relative to `test/regress/cli`.
Notes are capped at 72 characters; `--verbose` (`-v`) shows full reason comments,
source locations, command lines, inheritance and checkout details. `--summary`
prints just the totals; `--tester` is repeatable; `--json` prints the report,
totals and source evidence as JSON.
The command only reads files and prints to stdout. Exit status is 0 for a
completed audit, including one that finds exclusions, and 2 for unreadable,
missing, invalid, or unsupported inputs.

Checkout selection uses `scripts/targets.py`: `--cvc5`, `$DOKIMASIA_CVC5`,
`$CVC5`, `scripts/repos.local` (or `$DOKIMASIA_REPOS_FILE`),
`scripts/deps.local.json`, then `deps/cvc5`. The report names the actual checkout,
revision and working-tree dirty status in verbose mode. It never fetches or changes a checkout;
the repository's cvc5 pin does not override that selection.

## What the counts mean

The compact report totals only **`yes` cells** in each tester column, followed
by their sum and the number of distinct files containing those directives.
Repeated directives for the same tester in one file count once. Inherited
disables do not contribute to these totals.

The reason tally also counts `yes` cells only: `timeout` if a direct directive
has a timeout reason, `other` for another explanation, and `unknown` otherwise.
Its counts sum to the number of `yes` cells. CMake comments never supply the
reason for a direct directive. Filtering testers filters all these totals.

Verbose mode breaks the tester counts down further:

- **Direct**: files with `DISABLE-TESTER: <tester>`.
- **Inherited**: files disabled through another tester, excluding files that
  already disable this tester directly. The audit reads the cascade from the
  selected `run_regression.py`; for example, `proof` currently also disables
  `cpc`. It does not assume that `cpc` disables `cpc-logos` or that the cascade
  is transitive.
- **Affected**: the union of direct and inherited disables, counted once per
  file. This is distinct from the `yes` totals.

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
checking and an explanation of a restriction is labelled **Reason comment**.
Adjacent timeout or slowness explanations are also recognized without a tester
name. Wording such as "timeouts", "times out", and "timed out" is grouped under
the common note `timeout`. Slowness alone remains a separate explanation, not
a claimed timeout. Other prose is labelled **Context** in verbose mode.
This is a conservative text heuristic,
not an independent diagnosis. Each comment has its own source location so the
attribution can be reviewed. A nearby benchmark description is not sufficient
to establish a reason. Missing explanations remain **unknown**; verbose mode
prints command lines as additional context, without inferring unsupported options.

This is a source exclusion inventory. It does not evaluate tester `applies()`
predicates, `REQUIRES`, CI matrices, build configuration, or runtime tester
selection. A file with no disable is not necessarily tested, and an exclusion
does not establish a proof defect. Python tester registries must use the
literal forms supported by the parser. The harness is parsed as
syntax, never imported or executed.

Run the fixtures and optional checkout cross-check with:

```bash
python3 tests/test_regression_audit.py
python3 tests/test_regression_audit.py /path/to/cvc5
```

[Removal candidates and validation tasks](todo.md) record the source review
of which directives might be dropped.
