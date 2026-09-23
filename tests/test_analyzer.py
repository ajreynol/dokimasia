"""Observation identity, failure isolation, provenance and the real Koine boundary."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from dokimasia_analyzer.findings import ANALYSES, DEFAULT_ANALYSES, CHECKS, collect, finding_id, observation
from dokimasia_analyzer.sanity import ExtractionError
from bug_reports import DB, PAGE, append, read_dump, read_run, render, write_json
import bug_reports
import koine
import targets

REAL_CVC5 = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else None
if REAL_CVC5:
    sys.argv.pop(1)


class AnalyzerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.tree = self.base / "cvc5"
        (self.tree / "src").mkdir(parents=True)
        self.cpp = self.tree / "src/x.cpp"
        self.cpp.write_text("void f() {\n#ifdef CVC5_SAFE_MODE\n  mutate();\n#endif\n}\n")
        self.config = self.base / "targets.json"
        write_json(self.config, {"targets": [{"id": "cvc5", "project": "cvc5",
                    "paths": ["src/**/*"], "required": ["src"]}]})
        self.dump = self.base / "dump.json"
        self.db = self.base / "bugs.json"
        self.page = self.base / "page.md"
        self.main = runpy.run_path(str(ROOT / "scripts/dokimasia_analyzer"))["main"]
        self.argv = ["--config", str(self.config), "--cvc5", str(self.tree),
                     "--analysis", "buildmode", "--dump", str(self.dump),
                     "--db", str(self.db), "--page", str(self.page)]

    def run_analyzer(self, *extra):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return self.main(self.argv + list(extra))

    def need_koine(self):
        try:
            return koine.script()
        except ValueError as e:
            self.skipTest(str(e))

    def test_line_shift_and_checkout_move_preserve_identity(self):
        before = collect(str(self.tree), ["buildmode"])
        self.cpp.write_text("\n\n" + self.cpp.read_text())
        moved = self.base / "elsewhere"
        self.tree.rename(moved)
        after = collect(str(moved), ["buildmode"])
        self.assertEqual(before.dump(), after.dump())
        self.assertNotEqual(before.evidence, after.evidence)
        self.assertTrue(before.dump()[0]["id"].startswith("dokimasia:"))

    def test_sites_are_aggregated_without_losing_evidence(self):
        self.cpp.write_text(self.cpp.read_text() + self.cpp.read_text())
        r = collect(str(self.tree), ["buildmode"])
        self.assertEqual(len(r.dump()), 1)
        self.assertEqual(len(next(iter(r.evidence.values()))), 2)

    def test_identity_helper_does_not_analyze(self):
        code = "SEAM0001"
        p = subprocess.run([sys.executable, str(ROOT / "scripts/finding_id.py"), code,
                            "SAT_REFUTATION", "--record"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout), observation(code, "SAT_REFUTATION"))
        for bad in ("/absolute/file", "../escape", "", "x\\y", None):
            with self.assertRaises(ValueError):
                finding_id(code, bad)

    def test_catalogue_covers_exact_emitted_code_set(self):
        text = (ROOT / "docs/README.md").read_text().split("## Structured observations", 1)[1]
        import re
        self.assertEqual(set(re.findall(r"^\| `([A-Z]+\d{4})`", text, re.M)), set(CHECKS))

    def test_dry_run_and_no_update_need_no_koine(self):
        with patch.dict(os.environ, {"KOINE": str(self.base / "missing")}):
            self.assertEqual(self.run_analyzer("--dry-run"), 0)
            self.assertFalse(self.dump.exists())
            self.assertFalse(self.db.exists())
            self.assertEqual(self.run_analyzer("--no-update"), 0)
            self.assertTrue(self.dump.exists())
            self.assertFalse(self.db.exists())
        bugs = read_dump(self.dump)
        run = read_run(self.dump, bugs)
        self.assertEqual(run["coverage"]["cvc5"]["read"], ["src/x.cpp"])
        self.assertNotIn(str(self.tree), json.dumps(run))

    def test_both_producers_resolve_identical_scope(self):
        common = ["--cvc5", str(self.tree), "--config", str(self.config), "--dry-run"]
        outputs = []
        for script in ("scripts/dokimasia_analyzer", "prompts/dokimasia_analyzer_agent"):
            p = subprocess.run([sys.executable, str(ROOT / script), *common], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            outputs.append(p.stdout)
        self.assertEqual(*outputs)
        self.assertEqual(set(DEFAULT_ANALYSES),
                         {"ledger", "ci", "buildmode", "modes", "rewrites",
                          "trust", "infer", "inferid", "signature", "preprocess", "proofshape"})
        self.assertIn(", ".join(DEFAULT_ANALYSES), outputs[0])
        self.assertFalse((self.base / "agent.json").exists())

    def test_census_is_an_input_only_when_selected(self):
        census = self.base / "census.json"
        census.write_text("first sweep")
        with patch.object(targets, "CENSUS", census), patch.object(targets, "ROOT", self.base):
            # Supply implementation files expected by the digest without copying
            # the repository; only the census changes between these snapshots.
            for name in ("dokimasia_analyzer/x.py", "scripts/dokimasia_analyzer", "scripts/targets.py",
                         "scripts/targets.json", "scripts/bug_reports.py", "scripts/koine.py",
                         "scripts/koine.lock"):
                path = self.base / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("implementation")
            default = targets.implementation_digest()
            latent = targets.implementation_digest(["latent"])
            census.write_text("second sweep")
            self.assertEqual(targets.implementation_digest(), default)
            self.assertNotEqual(targets.implementation_digest(["latent"]), latent)
            census.unlink()
            self.assertEqual(targets.implementation_digest(), default)

    def test_checkout_precedence_and_local_configuration(self):
        (self.base / "scripts").mkdir()
        mapping = self.base / "scripts/repos.local"
        local_config = self.base / "scripts/deps.local.json"
        env = {k: v for k, v in os.environ.items()
               if k not in ("DOKIMASIA_CVC5", "CVC5", "DOKIMASIA_REPOS_FILE")}
        with patch.object(targets, "ROOT", self.base), patch.dict(os.environ, env, clear=True):
            self.assertEqual(targets.checkout()[0], self.base / "deps/cvc5")
            write_json(local_config, {"cvc5": {"path": str(self.tree)}})
            self.assertEqual(targets.checkout(), (self.tree, str(local_config)))
            mapping.write_text("cvc5 ../mapped tree\n")
            self.assertEqual(targets.checkout()[0], self.base / "mapped tree")
            with patch.dict(os.environ, {"CVC5": str(self.base / "environment")}):
                self.assertEqual(targets.checkout()[0], self.base / "environment")
                with patch.dict(os.environ, {"DOKIMASIA_CVC5": str(self.base / "preferred")}):
                    self.assertEqual(targets.checkout()[0], self.base / "preferred")
                    self.assertEqual(targets.checkout(str(self.tree))[0], self.tree)
            mapping.write_text("cvc5\n")
            with self.assertRaisesRegex(ValueError, "needs a checkout path"):
                targets.checkout()

    def test_analysis_and_reporting_share_local_map_and_fail_on_missing_target(self):
        mapped = self.base / "source tree"
        self.tree.rename(mapped)
        mapping = self.base / "repos.local"
        mapping.write_text("cvc5 source tree\n")
        env = {k: v for k, v in os.environ.items() if k not in ("DOKIMASIA_CVC5", "CVC5")}
        env["DOKIMASIA_REPOS_FILE"] = str(mapping)
        commands = [
            [sys.executable, str(ROOT / script), "--dry-run", "--config", str(self.config)]
            for script in ("scripts/dokimasia_analyzer", "prompts/dokimasia_analyzer_agent")]
        for command in commands:
            p = subprocess.run(command, cwd=self.base, env=env, capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn(str(mapped), p.stdout)
            self.assertIn(str(mapping), p.stdout)
        # The closure launcher reads github unless it is told otherwise, so only
        # its --use-local path shares this resolver. It joins the half that is
        # pure resolution: an explicit but missing environment choice must not
        # fall back to the valid local map and accidentally analyze, or assess a
        # closure against, another tree.
        commands.append([sys.executable, str(ROOT / "prompts/close_bug_db"),
                         "--use-local", "--dry-run"])
        env["DOKIMASIA_CVC5"] = str(self.base / "missing")
        for command in commands:
            p = subprocess.run(command, cwd=self.base, env=env, capture_output=True, text=True)
            self.assertEqual(p.returncode, 2, p.stdout + p.stderr)
            self.assertIn(str(self.base / "missing"), p.stderr)

    def test_combined_report_defaults_and_optional_selection(self):
        from dokimasia_analyzer import __main__ as cli
        with patch.object(cli, "_run", return_value=(0, "")) as run, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(["report", str(self.tree)]), 0)
            self.assertEqual([call.args[0] for call in run.call_args_list], list(DEFAULT_ANALYSES))
            run.reset_mock()
            self.assertEqual(cli.main(["report", str(self.tree), "--analysis", "tcb",
                                       "--analysis", "latent"]), 0)
            self.assertEqual([call.args[0] for call in run.call_args_list], ["tcb", "latent"])

    def test_prompt_preview_has_no_side_effects(self):
        agent = self.base / "agent.json"
        p = subprocess.run([sys.executable, str(ROOT / "prompts/dokimasia_analyzer_agent"),
            "--cvc5", str(self.tree), "--config", str(self.config), "--out", str(agent),
            "--show-prompt"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("Do not run Dokimasia", p.stdout)
        self.assertIn("Do not append", p.stdout)
        self.assertNotIn("{TARGETS}", p.stdout)
        self.assertEqual(list(self.base.glob("agent*")), [])

    def test_missing_target_unknown_selection_and_empty_scope_fail(self):
        self.assertEqual(self.run_analyzer("--target", "absent", "--no-update"), 2)
        self.assertEqual(self.run_analyzer("--cvc5", str(self.base / "absent"), "--dry-run"), 2)
        self.cpp.unlink()
        self.assertEqual(self.run_analyzer("--no-update"), 2)
        self.assertFalse(self.dump.exists())

    def test_extraction_failure_preserves_previous_outputs(self):
        self.dump.write_text("previous dump")
        self.db.write_text("previous database")
        with patch.dict(self.main.__globals__, {"collect": lambda *_: (_ for _ in ()).throw(ExtractionError("anchor missing"))}):
            self.assertEqual(self.run_analyzer(), 2)
        self.assertEqual(self.dump.read_text(), "previous dump")
        self.assertEqual(self.db.read_text(), "previous database")

    def test_changed_inputs_abort_before_writes(self):
        def changing(root, analyses):
            r = collect(root, analyses)
            self.cpp.write_text(self.cpp.read_text() + "// change\n")
            return r
        with patch.dict(self.main.__globals__, {"collect": changing}):
            self.assertEqual(self.run_analyzer(), 2)
        self.assertFalse(self.dump.exists())

    def test_duplicate_and_malformed_dump_refused(self):
        self.assertEqual(self.run_analyzer("--no-update"), 0)
        bugs = read_dump(self.dump)
        for invalid in ([bugs[0], bugs[0]], [bugs[0], None], [dict(bugs[0], id="invented")],
                        [dict(bugs[0], description="")], [dict(bugs[0], code=[])],
                        [dict(bugs[0], found_at="new-commit")]):
            write_json(self.dump, invalid)
            with self.assertRaises(ValueError):
                append(self.dump, self.db, self.page)
            self.assertFalse(self.db.exists())

    def test_dump_and_evidence_must_match(self):
        self.assertEqual(self.run_analyzer("--no-update"), 0)
        self.dump.write_text(self.dump.read_text() + "\n")
        with self.assertRaisesRegex(ValueError, "does not match"):
            append(self.dump, self.db, self.page)
        self.assertFalse(self.db.exists())

    def test_real_koine_append_repeat_disappearance_and_conflict(self):
        self.need_koine()
        self.assertEqual(self.run_analyzer("--no-update"), 0)
        self.assertEqual(append(self.dump, self.db, self.page, date="2026-09-01"), 0)
        first = json.loads(self.db.read_text())["bugs"]
        self.assertEqual(len(first), 1)
        self.assertEqual(append(self.dump, self.db, self.page, date="2026-09-02"), 0)
        twice = json.loads(self.db.read_text())["bugs"]
        self.assertEqual(len(twice), 1)
        self.assertEqual(twice[0]["first_seen"], "2026-09-01")
        self.assertEqual(twice[0]["last_seen"], "2026-09-02")
        self.assertEqual(self.page.read_text(), render(self.db))
        self.assertTrue(list((self.base / "runs").glob("*.json")))
        self.cpp.write_text("void f() {}\n")
        self.assertEqual(self.run_analyzer("--no-update"), 0)
        self.assertEqual(append(self.dump, self.db, self.page), 0)
        self.assertEqual(json.loads(self.db.read_text())["bugs"], twice)
        # A second producer disputes the wording under an existing identity.
        changed = [{k: v for k, v in first[0].items() if k not in ("first_seen", "last_seen")}]
        changed[0]["description"] = "A revised claim"
        self.write_evidenced_dump(changed)
        self.assertEqual(append(self.dump, self.db, self.page), 0)
        self.assertEqual(json.loads(self.db.read_text())["bugs"][0]["description"], first[0]["description"])

    def write_evidenced_dump(self, bugs):
        write_json(self.dump, bugs)
        sidecar = Path(str(self.dump) + ".run.json")
        run = json.loads(sidecar.read_text())
        run["dump_sha256"] = hashlib.sha256(self.dump.read_bytes()).hexdigest()
        run["evidence"] = {"cvc5": {b["id"]: [{"location": "src/x.cpp", "detail": "review"}] for b in bugs}}
        write_json(sidecar, run)

    def test_koine_dry_run_never_creates_output_or_archive(self):
        self.need_koine()
        self.assertEqual(self.run_analyzer("--no-update"), 0)
        before = sorted(str(p) for p in self.base.rglob("*"))
        self.assertEqual(append(self.dump, self.db, self.page, dry_run=True), 0)
        self.assertEqual(before, sorted(str(p) for p in self.base.rglob("*")))

    def test_database_artifact_defaults_and_cli_render_check(self):
        self.need_koine()
        self.assertEqual(DB, ROOT / "bug_db/bugs.json")
        self.assertEqual(PAGE, ROOT / "bug_db/bugs.md")
        page = self.db.parent / "bugs.md"
        # Exercise real subprocesses with a deadline: taking Koine's lock
        # again while the wrapper holds it must not stall a recording command.
        command = [sys.executable, str(ROOT / "scripts/dokimasia_analyzer"), *self.argv[:-2]]
        p = subprocess.run(command, capture_output=True, text=True, timeout=10)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertEqual(page.read_text(), render(self.db, page))
        page.unlink()
        command = [sys.executable, str(ROOT / "scripts/append_findings"), "--db", str(self.db)]
        p = subprocess.run([*command, str(self.dump)], capture_output=True, text=True, timeout=10)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertEqual(page.read_text(), render(self.db, page))
        self.assertFalse((self.db.parent / "static-analysis.md").exists())
        before = self.db.read_bytes()
        env = os.environ | {"KOINE": str(self.base / "missing")}
        check = [*command, "--render-only", "--check"]
        self.assertEqual(subprocess.run(check, env=env, capture_output=True).returncode, 0)
        page.write_text("stale view\n")
        p = subprocess.run(check, env=env, capture_output=True, text=True)
        self.assertEqual(p.returncode, 1)
        self.assertIn("regenerate", p.stderr)
        self.assertEqual(page.read_text(), "stale view\n")
        p = subprocess.run([*command, "--render-only"], env=env, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(page.read_text(), render(self.db, page))
        self.assertEqual(self.db.read_bytes(), before)

    def test_render_links_follow_database_and_page_locations(self):
        db = self.base / "data set" / "observations.json"
        page = self.base / "views" / "observations.md"
        write_json(db, {"bugs": [dict(observation("SEAM0001", "SAT_REFUTATION"),
                                     description="a | b <tag> `code`\nnext line")]})
        body = render(db, page)
        self.assertIn("[bugs.json](../data%20set/observations.json)", body)
        self.assertIn("[Archived run records](../data%20set/runs/)", body)
        # The data links relocate with the artifact; the documentation is
        # named and never linked. A generated page that links a hand-written
        # document re-creates a stale cross-reference on every render.
        self.assertIn("`docs/maintenance.md`", body)
        self.assertNotIn("](docs/maintenance.md", body)
        self.assertNotIn("../docs/", body)
        self.assertIn("a &#124; b &lt;tag&gt; &#96;code&#96; next line", body)

    def test_tally_counts_experiences_by_kind_and_preserves_episodes(self):
        experience = self.base / "experience.md"
        before = "# Experience\n\nWithdrawn ids: E1–E8 and E11–E13.\n\n"
        after = """

## E9: cvc5 fixed documentation
| **Kind** | positive — one observation closed |
Unchanged prose.
## E10: cvc5 rejected an ask
| **Kind** | negative — our ask was rejected |
## E14: cvc5 corrected our claim
| **Kind** | negative — the mechanism was wrong |
## E15: cvc5 isolated dependencies
| **Kind** | positive — a register-only ask acted on |
## How this page is maintained
```text
## E999: a quoted example must not count
| **Kind** | positive — example |
```
"""
        experience.write_text(before + bug_reports.TALLY_BEGIN + "\nold tally\n"
                              + bug_reports.TALLY_END + after)
        # Four experiences count even though the database has only one closure.
        write_json(self.db, {"bugs": [{"owner": "cvc5", "closed_on": "2026-09-19"}]})
        body = bug_reports.render_experience(experience)
        self.assertTrue(body.startswith(before + bug_reports.TALLY_BEGIN))
        self.assertTrue(body.endswith(bug_reports.TALLY_END + after))
        self.assertIn("| cvc5 | 2 | 2 | 0 | 4 |", body)
        self.assertIn("| **total** | **2** | **2** | **0** | **4** |", body)
        experience.write_text(body)
        self.assertEqual(bug_reports.render_experience(experience), body)
        write_json(self.db, {"bugs": []})
        self.assertEqual(bug_reports.render_experience(experience), body)
        experience.write_text(body + "\n## E16: cvc5 asked a question\n| **Kind** | neutral — question |\n")
        self.assertIn("| cvc5 | 2 | 2 | 1 | 5 |", bug_reports.render_experience(experience))
        experience.write_text(before + bug_reports.TALLY_BEGIN + "\n" + bug_reports.TALLY_END)
        self.assertIn("| cvc5 | 0 | 0 | 0 | 0 |", bug_reports.render_experience(experience))
        # A relocated/trial database never reads or rewrites the real log.
        with patch.object(bug_reports, "EXPERIENCE", self.base / "missing.md"):
            self.assertEqual(set(bug_reports.render_views(self.db, self.page)), {self.page})
        with patch.object(bug_reports, "EXPERIENCE", experience):
            with self.assertRaisesRegex(ValueError, "cannot overwrite the experience log"):
                bug_reports.render_views(self.db, experience)
            with self.assertRaisesRegex(ValueError, "cannot overwrite the experience log"):
                append(self.dump, self.db, experience)

    def test_tally_cli_detects_drift_without_writing_and_refuses_broken_markers(self):
        experience = self.base / "experience.md"
        original = "Episode prose\n" + bug_reports.TALLY_BEGIN + "\nstale\n" + bug_reports.TALLY_END
        experience.write_text(original)
        write_json(self.db, {"bugs": [{"owner": "cvc5", "closed_on": "2026-09-19"}]})
        self.page.write_text(render(self.db, self.page))
        db_before = self.db.read_bytes()
        def cli(*flags):
            argv = [str(ROOT / "scripts/append_findings"), "--db", str(self.db),
                    "--page", str(self.page), "--render-only", *flags]
            with patch.object(bug_reports, "DB", self.db), \
                    patch.object(bug_reports, "EXPERIENCE", experience), \
                    patch.object(sys, "argv", argv), \
                    contextlib.redirect_stderr(io.StringIO()) as err, \
                    self.assertRaises(SystemExit) as result:
                runpy.run_path(argv[0], run_name="__main__")
            return result.exception.code, err.getvalue()
        rc, error = cli("--check")
        self.assertEqual(rc, 1)
        self.assertIn(str(experience), error)
        self.assertEqual(experience.read_text(), original)
        self.assertEqual(cli()[0], 0)
        self.assertEqual(cli("--check")[0], 0)
        self.assertEqual(self.db.read_bytes(), db_before)
        # A new negative episode invalidates the tally without any DB change.
        experience.write_text(experience.read_text()
                              + "\n## E10: cvc5 rejected an ask\n| **Kind** | negative — rejected |\n")
        self.assertEqual(cli("--check")[0], 1)
        self.assertEqual(cli()[0], 0)
        self.assertIn("| cvc5 | 0 | 1 | 0 | 1 |", experience.read_text())
        self.assertEqual(cli("--check")[0], 0)
        for broken in ("no markers", bug_reports.TALLY_END + bug_reports.TALLY_BEGIN,
                       original + bug_reports.TALLY_END,
                       original + "\n## E9: no Kind row\n",
                       original + "\n## E9: invalid Kind\n| **Kind** | unknown |\n",
                       original + "\n## E9: empty Kind\n| **Kind** |   |\n"):
            with self.subTest(markers=broken):
                experience.write_text(broken)
                self.page.write_text("stale view")
                self.assertEqual(cli()[0], 2)
                self.assertEqual(experience.read_text(), broken)
                self.assertEqual(self.page.read_text(), "stale view")

    def test_retired_koine_layouts_are_refused(self):
        (self.base / "scripts").mkdir()
        (self.base / "scripts/koine.lock").write_text("0" * 40)
        for legacy in ("koine_append_db", "bug_db/koine_append_db"):
            path = self.base / "old-koine" / legacy
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("retired entry point")
            with patch.object(koine, "ROOT", self.base), \
                    patch.dict(os.environ, {"KOINE": str(self.base / "old-koine")}):
                with self.assertRaisesRegex(ValueError, "no bug_db_manager/koine_append_db.*retired layout"):
                    koine.script()
            path.unlink()

    def test_wrong_koine_pin_refused(self):
        path = self.need_koine().parents[len(koine.SCRIPT.parts) - 1]
        with patch.object(koine, "ROOT", self.base):
            (self.base / "scripts").mkdir()
            (self.base / "scripts/koine.lock").write_text("0" * 40)
            with patch.dict(os.environ, {"KOINE": str(path)}):
                with self.assertRaisesRegex(ValueError, "pinned commit"):
                    koine.script()

    def test_same_run_comparison_and_snapshot_mismatch(self):
        self.assertEqual(self.run_analyzer("--no-update"), 0)
        compare = runpy.run_path(str(ROOT / "scripts/compare_findings"))["compare"]
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(compare(self.dump, self.dump), 0)
        self.assertIn("1 shared", out.getvalue())
        other = self.base / "other.json"
        other.write_bytes(self.dump.read_bytes())
        run = json.loads(Path(str(self.dump) + ".run.json").read_text())
        run["targets"][0]["input_sha256"] = "0" * 64
        write_json(str(other) + ".run.json", run)
        with self.assertRaisesRegex(ValueError, "different targets"):
            compare(self.dump, other)

    def test_output_aliases_are_refused_before_overwriting(self):
        self.db.write_text("original")
        self.assertEqual(self.run_analyzer("--dump", str(self.db)), 2)
        self.assertEqual(self.db.read_text(), "original")
        original = self.cpp.read_text()
        self.assertEqual(self.run_analyzer("--dump", str(self.cpp), "--no-update"), 2)
        self.assertEqual(self.cpp.read_text(), original)

    def test_incomplete_or_malformed_evidence_is_refused(self):
        self.assertEqual(self.run_analyzer("--no-update"), 0)
        sidecar = Path(str(self.dump) + ".run.json")
        original = json.loads(sidecar.read_text())
        for update in ({"evidence": []}, {"evidence": {"cvc5": []}}, {"evidence": {}},
                       {"analyses": [None]}, {"targets": [None]}, {"complete": False}):
            write_json(sidecar, original | update)
            with self.assertRaises(ValueError):
                append(self.dump, self.db, self.page)
            self.assertFalse(self.db.exists())

    def test_concurrent_wrapper_writers_are_refused(self):
        self.need_koine()
        self.assertEqual(self.run_analyzer("--no-update"), 0)
        from bug_reports import writer
        with writer(self.db):
            with self.assertRaisesRegex(ValueError, "another writer"):
                append(self.dump, self.db, self.page)
        self.assertFalse(self.db.exists())

    def test_omitted_scanner_input_is_not_accepted_as_coverage(self):
        write_json(self.config, {"targets": [{"id": "cvc5", "project": "cvc5",
                   "paths": ["src/x.cpp"], "required": ["src"]}]})
        (self.tree / "src/unlisted.cpp").write_text("void g() {}\n")
        self.assertEqual(self.run_analyzer("--no-update"), 2)
        self.assertFalse(self.dump.exists())

    @unittest.skipUnless(REAL_CVC5, "provide pinned cvc5 to check all adapters")
    def test_real_checkout_all_adapters_and_fresh_evidence(self):
        r = collect(REAL_CVC5, ANALYSES)
        self.assertTrue(r.dump())
        self.assertEqual(set(r.measurements), set(ANALYSES))
        self.assertEqual(len({b["id"] for b in r.dump()}), len(r.dump()))
        self.assertTrue(any(b["code"] == "SIG0003" and b["entity"] == "SUBS" for b in r.dump()))
        self.assertFalse(any(b["code"] == "BUILD0001" for b in r.dump()))
        self.assertEqual(r.measurements["latent"]["census_provenance"]["corpus"], "regress0")
        self.assertEqual(r.measurements["latent"]["census_provenance"]["source_record"],
                         "tests/corpus/reach-corpus.json")
        default = collect(REAL_CVC5)
        self.assertEqual(default.dump(), r.dump())
        self.assertEqual(set(default.measurements), set(DEFAULT_ANALYSES))
        p = subprocess.run([sys.executable, str(ROOT / "scripts/dokimasia_analyzer"),
                            "--cvc5", str(Path(REAL_CVC5).resolve()), "--no-update",
                            "--dump", str(self.dump)], cwd=self.base, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(read_dump(self.dump), r.dump())
        run = read_run(self.dump, r.dump())
        self.assertEqual(run["analyses"], list(DEFAULT_ANALYSES))
        self.assertEqual(set(run["measurements"]["cvc5"]), set(DEFAULT_ANALYSES))
        for rows in r.evidence.values():
            for row in rows:
                locations = row.get("locations", []) + ([row["location"]] if "location" in row else [])
                for loc in locations:
                    self.assertTrue((Path(REAL_CVC5) / loc.split(":", 1)[0]).exists(), loc)

    @unittest.skipUnless(REAL_CVC5, "provide pinned cvc5 to check baseline lookup")
    def test_baselines_work_outside_repository(self):
        p = subprocess.run([sys.executable, "-m", "dokimasia_analyzer", "check",
                            str(Path(REAL_CVC5).resolve())], cwd=self.base,
                           env=os.environ | {"PYTHONPATH": str(ROOT)}, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertFalse(list(self.base.glob("*-baseline.json")))


if __name__ == "__main__":
    unittest.main()
