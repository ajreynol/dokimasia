"""Regression audit fixtures and an optional cross-check against a cvc5 checkout.

Run: python3 tests/test_regression_audit.py [<cvc5>]
"""
from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from regression_audit.audit import CLI, HARNESS, read_harness, scan
from regression_audit.cli import compact_rows

SCRIPT = ROOT / "scripts/eo_cvc5_regressions_audit"
CMAKE = CLI / "CMakeLists.txt"
REAL_CHECKOUT = Path(sys.argv.pop(1)).resolve() if len(sys.argv) > 1 else (
    Path(os.environ["CVC5"]).resolve() if os.environ.get("CVC5") else None)

# The registry's constructors need not exist: the audit must never import or
# execute the target harness. Its live cascade differs when logos is present.
RUNNER = '''
raise RuntimeError("the audit must not execute this module")
g_testers = {"base": Base(), "proof": Proof(), "cpc": Cpc(), "lfsc": Lfsc()}
g_default_testers = ["base", "proof"]
def run_regression(testers, disable_tester):
    if disable_tester in testers:
        testers.remove(disable_tester)
    if disable_tester == "proof":
        if "lfsc" in testers:
            testers.remove("lfsc")
        if "cpc" in testers:
            testers.remove("cpc")
'''


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.write(HARNESS, RUNNER)
        self.write(CMAKE, '''set(regression_disabled_tests
  # times out with proof checking
  regress0/both.smt2
  regress0/suite.smt2 # platform-dependent output
  regress0/unexplained.smt2
)
''')
        self.write(CLI / "regress0/plain.smt2", "; EXPECT: unsat\n(check-sat)\n")
        self.write(CLI / "regress0/proof.smt2", '''; Proof checking is disabled because it changes the output.
; DISABLE-TESTER: proof
; DISABLE-TESTER: lfsc
; COMMAND-LINE: --global-negate
; COMMAND-LINE: --global-negate --foo
(check-sat)
''')
        self.write(CLI / "regress0/cpc.smt2", '''; EXPECT: unsat
; DISABLE-TESTER: cpc
; Disabled cpc due to overloaded constructors.
; The checker cannot handle these names.
(check-sat)
''')
        self.write(CLI / "regress0/both.smt2", '''; DISABLE-TESTER: proof
; DISABLE-TESTER: cpc
; DISABLE-TESTER: proof
; Ported from another solver's benchmark suite.
(check-sat)
''')
        self.write(CLI / "regress0/suite.smt2", "(check-sat)\n")
        self.write(CLI / "regress0/unexplained.smt2", "(check-sat)\n")

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def run_cli(self, *args, env=None):
        environment = os.environ.copy()
        for key in ("DOKIMASIA_CVC5", "CVC5", "DOKIMASIA_REPOS_FILE"):
            environment.pop(key, None)
        environment.update(env or {})
        return subprocess.run([str(SCRIPT), *args], cwd=self.root, env=environment,
                              text=True, capture_output=True)

    def rows(self, report):
        return {Path(r["path"]).name: r for r in report["regressions"]}

    def test_unique_counts_and_reason_evidence(self):
        report = scan(self.root)
        self.assertEqual(report["files_scanned"], 6)
        proof, cpc = (report["testers"][t] for t in ("proof", "cpc"))
        self.assertEqual((proof["direct"], proof["total_disabled"]), (2, 2))
        self.assertEqual((cpc["direct"], cpc["inherited_only"], cpc["total_disabled"]), (2, 1, 3))
        self.assertEqual(report["testers"]["cpc-logos"]["status"], "planned (not registered)")
        self.assertIsNone(report["testers"]["cpc-logos"]["total_disabled"])
        rows = self.rows(report)
        self.assertNotIn("plain.smt2", rows)
        directive = rows["proof.smt2"]["directives"][0]
        self.assertEqual(directive["affects"], ["proof", "cpc"])
        self.assertEqual(directive["location"], f"{CLI}/regress0/proof.smt2:2")
        self.assertEqual(directive["reason_comments"][0]["location"], f"{CLI}/regress0/proof.smt2:1")
        self.assertEqual(directive["inherited_at"]["cpc"], f"{HARNESS}:12")
        self.assertEqual(len(rows["proof.smt2"]["command_lines"]), 2)
        self.assertIn("checker cannot", rows["cpc.smt2"]["directives"][0]["reason_comments"][0]["text"])
        # General descriptions must not become fabricated explanations.
        self.assertFalse(rows["both.smt2"]["directives"][0]["reason_comments"])
        self.assertIn("Ported", rows["both.smt2"]["directives"][0]["context"][0]["text"])
        self.assertNotIn("suite.smt2", rows)
        self.assertNotIn("unexplained.smt2", rows)
        self.assertNotIn("suite_disabled", rows["both.smt2"])

    def test_harness_cascades_follow_selected_checkout(self):
        # Registering logos does not imply that proof or cpc disables it.
        runner = RUNNER.replace('"base": Base()', '"cpc-logos": Logos(), "base": Base()')
        self.write(HARNESS, runner)
        self.assertEqual(scan(self.root)["testers"]["cpc-logos"]["total_disabled"], 0)
        self.write(HARNESS, runner + '''        if "cpc-logos" in testers:
            testers.remove("cpc-logos")
''')
        self.write(CLI / "regress1/logos.smt2", "; DISABLE-TESTER: cpc-logos\n")
        logos = scan(self.root)["testers"]["cpc-logos"]
        self.assertEqual((logos["direct"], logos["inherited_only"], logos["total_disabled"]), (1, 2, 3))
        self.write(HARNESS, runner + '''    if disable_tester == "cpc":
        if "cpc-logos" in testers:
            testers.remove("cpc-logos")
''')
        proof = self.rows(scan(self.root))["proof.smt2"]["directives"][0]
        self.assertEqual(proof["affects"], ["proof", "cpc"])
        # Removing the cpc cascade is reflected immediately, without a hardcoded
        # proof -> cpc rule in the auditor.
        self.write(HARNESS, RUNNER.replace('testers.remove("cpc")', 'pass'))
        (self.root / CLI / "regress1/logos.smt2").write_text("; EXPECT: unsat\n")
        self.assertEqual(scan(self.root)["testers"]["cpc"]["inherited_only"], 0)

    def test_metadata_matches_runner_and_scans_whole_file(self):
        self.write(CLI / "regress2/metadata.sy", ''' ; DISABLE-TESTER: proof
;; DISABLE-TESTER: proof
; EXPECT: DISABLE-TESTER: proof
(check-sat)
; DISABLE-TESTER: cpc
''')
        report = scan(self.root)
        self.assertEqual(report["testers"]["proof"]["direct"], 2)
        self.assertEqual(report["testers"]["cpc"]["direct"], 3)
        self.assertEqual(self.rows(report)["metadata.sy"]["directives"][0]["location"],
                         f"{CLI}/regress2/metadata.sy:5")

    def test_bad_inputs_fail_instead_of_reporting_a_clean_zero(self):
        self.write(CLI / "regress0/invalid.smt2", "; DISABLE-TESTER: cpc ; reason\n")
        result = self.run_cli("--cvc5", str(self.root))
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid.smt2:1: unknown DISABLE-TESTER", result.stderr)
        self.assertFalse(result.stdout)
        result = self.run_cli("--cvc5", str(self.root / "missing"))
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)
        self.write(CMAKE, "set(regression_disabled_tests\nregress0/missing.smt2\n)\n")
        self.write(CLI / "regress0/invalid.smt2", "; EXPECT: sat\n")
        self.assertEqual(len(scan(self.root)["regressions"]), 3)
        with self.assertRaisesRegex(ValueError, "literal g_testers"):
            read_harness("g_testers = make_testers()")
        with self.assertRaisesRegex(ValueError, "dynamic disable cascade"):
            read_harness(RUNNER.replace('testers.remove("cpc")', 'testers.remove(other)'))

    def test_cli_works_from_another_directory_and_uses_shared_resolution(self):
        result = self.run_cli(env={"DOKIMASIA_CVC5": str(self.root)})
        self.assertEqual(result.returncode, 0, result.stderr)
        header = next(line for line in result.stdout.splitlines() if line.startswith("Regression"))
        self.assertEqual(header.split(), ["Regression", "proof", "cpc", "cpc-logos", "Note"])
        table = {line.split()[0]: line for line in result.stdout.splitlines() if line.startswith("regress0/")}
        self.assertRegex(table["regress0/proof.smt2"], r"proof\.smt2 +yes +-- +-- +")
        self.assertRegex(table["regress0/cpc.smt2"], r"cpc\.smt2 +no +yes +-- +")
        self.assertNotIn("regress0/suite.smt2", table)
        self.assertRegex(table["regress0/both.smt2"], r"both\.smt2 +yes +yes +-- +unknown")
        self.assertNotIn("suite: timeout", result.stdout)
        self.assertIn("Yes totals: proof 2 / cpc 2 / cpc-logos 0 (planned); sum 4 (3 regressions)", result.stdout)
        self.assertIn("Reasons (yes only): timeout 0 / other 2 / unknown 2", result.stdout)
        self.assertEqual(sum(line.startswith("regress0/") for line in result.stdout.splitlines()), 3)
        self.assertNotIn("COMMAND-LINE:", result.stdout)
        self.assertNotIn(str(HARNESS), result.stdout)
        self.assertNotIn("Reason comment:", result.stdout)
        self.assertIn("overloaded constructors", result.stdout)
        verbose = self.run_cli("--verbose", "--cvc5", str(self.root))
        self.assertEqual(verbose.returncode, 0, verbose.stderr)
        self.assertIn("cpc via proof", verbose.stdout)
        self.assertIn("Reason: unknown", verbose.stdout)
        self.assertIn("COMMAND-LINE: --global-negate", verbose.stdout)
        self.assertIn(f"{HARNESS}:12", verbose.stdout)
        self.assertIn("Ported from another solver", verbose.stdout)
        summary = self.run_cli("--summary", "--cvc5", str(self.root),
                               env={"DOKIMASIA_CVC5": str(self.root / "wrong")})
        self.assertEqual(summary.returncode, 0, summary.stderr)
        self.assertNotIn("proof.smt2", summary.stdout)
        mapping = self.root / "repos.local"
        mapping.write_text("cvc5 .\n")
        result = self.run_cli("--json", "--tester", "cpc", env={"DOKIMASIA_REPOS_FILE": str(mapping)})
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(list(report["testers"]), ["cpc"])
        self.assertEqual(report["resolved_via"], str(mapping))
        self.assertEqual(report["testers"]["cpc"]["total_disabled"], 3)
        self.assertEqual(report["totals"], {"yes_entries": 2, "regressions_with_directives": 2,
                                          "reasons": {"timeout": 0, "other": 1, "unknown": 1}})
        result = self.run_cli("--json", "--tester", "cpc-logos", "--cvc5", str(self.root))
        self.assertEqual(json.loads(result.stdout)["regressions"], [])
        self.assertEqual(json.loads(result.stdout)["totals"]["yes_entries"], 0)

    def test_timeout_reasons_and_filtered_totals(self):
        for comment in ("timeout", "Timeouts on debug builds", "time out", "times out",
                        "timed out", "timing out", "time-out"):
            with self.subTest(comment=comment):
                self.write(CLI / "regress0/plain.smt2", f"; DISABLE-TESTER: cpc\n; {comment}\n")
                result = self.run_cli("--json", "--tester", "cpc", "--cvc5", str(self.root))
                self.assertEqual(result.returncode, 0, result.stderr)
                report = json.loads(result.stdout)
                self.assertEqual(self.rows(report)["plain.smt2"]["directives"][0]["reason_comments"][0]["text"], comment)
                self.assertEqual(report["totals"]["reasons"]["timeout"], 1)
                self.assertEqual(sum(report["totals"]["reasons"].values()), report["totals"]["yes_entries"])
        # A cpc-only timeout must not affect the proof tally.
        result = self.run_cli("--summary", "--tester", "proof", "--cvc5", str(self.root))
        self.assertIn("Yes totals: proof 2; sum 2 (2 regressions)", result.stdout)
        self.assertIn("Reasons (yes only): timeout 0 / other 1 / unknown 1", result.stdout)
        # Keep general performance explanations; do not silently relabel slow
        # conversion as a demonstrated timeout or infer reasons from filenames.
        self.write(CLI / "regress0/plain.smt2", "; DISABLE-TESTER: cpc\n;; slow conversion\n")
        result = self.run_cli("--cvc5", str(self.root))
        self.assertIn("slow conversion", result.stdout)
        self.assertIn("Reasons (yes only): timeout 0 / other 3 / unknown 2", result.stdout)
        self.write(CLI / "regress0/plain.smt2", "; DISABLE-TESTER: cpc\n; test timeout-core generation\n")
        self.assertFalse(self.rows(scan(self.root))["plain.smt2"]["directives"][0]["reason_comments"])

    @unittest.skipUnless(REAL_CHECKOUT, "pass a cvc5 checkout or set CVC5 for the source cross-check")
    def test_real_checkout(self):
        report = scan(REAL_CHECKOUT)
        # Independent direct census: duplicates count once per file. Counts
        # move with the checkout, so this does not pin a development branch.
        direct = {t: set() for t in ("proof", "cpc", "cpc-logos")}
        files = list((REAL_CHECKOUT / CLI).rglob("*.smt2")) + list((REAL_CHECKOUT / CLI).rglob("*.sy"))
        for path in files:
            for line in path.read_text().splitlines():
                if line.startswith(";"):
                    metadata = line[1:].strip().split(":", 1)
                    if len(metadata) == 2 and metadata[0] == "DISABLE-TESTER":
                        tester = metadata[1].strip()
                        if tester in direct:
                            direct[tester].add(path)
        self.assertEqual(report["files_scanned"], len(files))
        for tester, paths in direct.items():
            self.assertEqual(report["testers"][tester]["direct"], len(paths))
            yes_paths = {REAL_CHECKOUT / CLI / r["path"]
                         for r in compact_rows(report, list(direct)) if r["cells"][tester] == "yes"}
            self.assertEqual(yes_paths, paths)
        # Every directive location must point into the selected checkout.
        for row in report["regressions"]:
            for directive in row["directives"]:
                path, number = directive["location"].rsplit(":", 1)
                self.assertEqual((REAL_CHECKOUT / path).read_text().splitlines()[int(number) - 1][1:].strip(),
                                 "DISABLE-TESTER: " + directive["tester"])


if __name__ == "__main__":
    unittest.main()
