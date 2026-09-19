"""Exercise Dokimasia's configuration and CLI against the real pinned Koine."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import closure_baseline
import koine


class ClosureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)

    def need_koine(self):
        try:
            return koine.script("koine_close_db")
        except ValueError as e:
            self.skipTest(str(e))

    def launch(self, *args, **env):
        return subprocess.run([sys.executable, str(ROOT / "prompts/close_bug_db"), *args],
                              cwd=self.base, env=os.environ | env,
                              capture_output=True, text=True, timeout=10)

    def test_baseline_uses_latest_cvc5_archive_then_lock_and_explicit_override(self):
        (self.base / "scripts").mkdir()
        (self.base / "scripts/cvc5.lock").write_text(json.dumps({"cvc5": {"commit": "pinned"}}))
        with patch.object(closure_baseline, "ROOT", self.base), \
                patch.object(closure_baseline, "DB", self.base / "bugs.json"):
            self.assertEqual(closure_baseline.baseline(), ("pinned", "scripts/cvc5.lock"))
            (self.base / "runs").mkdir()
            for day, project, commit in (("01", "cvc5", "old"), ("02", "cvc5", "new"),
                                         ("03", "elsewhere", "irrelevant")):
                (self.base / "runs" / (day + ".json")).write_text(json.dumps({
                    "observed_on": "2026-09-" + day,
                    "targets": [{"project": project, "commit": commit}]}))
            self.assertEqual(closure_baseline.baseline()[0], "new")
            self.assertEqual(closure_baseline.baseline("override"), ("override", "--since"))

    def assistants(self):
        capture = self.base / "invocation.json"
        for name in ("codex", "claude"):
            script = self.base / name
            script.write_text("#!/usr/bin/env python3\nimport json, os, sys\n"
                              "from pathlib import Path\n"
                              "Path(os.environ['CAPTURE']).write_text(json.dumps("
                              "[os.getcwd(), sys.argv[1:]]))\nsys.exit(7)\n")
            script.chmod(0o755)
        return capture, {"PATH": str(self.base) + os.pathsep + os.environ["PATH"], "CAPTURE": str(capture)}

    def test_assistant_arguments_date_baseline_and_exit_status(self):
        self.need_koine()
        capture, env = self.assistants()
        for flags, prefix in (([], []), (["--print"], ["-p"]),
                              (["--codex"], []), (["--codex", "--print"], ["exec"])):
            with self.subTest(flags=flags):
                p = self.launch(*flags, "--since", "abc123", "--date", "2026-09-19", **env)
                self.assertEqual(p.returncode, 7, p.stderr)
                cwd, argv = json.loads(capture.read_text())
                self.assertEqual(cwd, str(ROOT))
                self.assertEqual(argv[:-1], prefix)
                self.assertIn("/compare/abc123...main", argv[-1])
                self.assertIn('"closed_on":     "2026-09-19"', argv[-1])
                self.assertNotIn("{when}", argv[-1])
        capture.unlink()
        p = self.launch("--show-prompt", **(env | {"KOINE": str(self.base / "missing")}))
        self.assertEqual(p.returncode, 2)
        self.assertIn("Koine unavailable", p.stderr)
        self.assertFalse(capture.exists())

    def test_empty_local_window_and_shallow_checkout_never_start_an_assistant(self):
        self.need_koine()
        capture, env = self.assistants()
        tree = self.base / "source tree"
        (tree / "src/theory").mkdir(parents=True)
        (tree / "include/cvc5").mkdir(parents=True)
        (tree / "configure.sh").touch()
        (tree / "include/cvc5/cvc5_proof_rule.h").touch()
        def git(*args):
            return subprocess.run(["git", "-C", str(tree), *args], check=True,
                                  capture_output=True, text=True).stdout.strip()
        git("init", "-q")
        git("add", ".")
        git("-c", "user.name=Test", "-c", "user.email=test@example.org", "commit", "-qm", "baseline")
        base = git("rev-parse", "HEAD")
        p = self.launch("--use-local", "--since", base, DOKIMASIA_CVC5=str(tree), **env)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("No commit landed", p.stdout)
        p = self.launch("--use-local", str(tree), "--since", base, "--dry-run", **env)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("0 commit(s)", p.stdout)
        shallow = self.base / "shallow"
        git("clone", "--depth", "1", tree.as_uri(), str(shallow))
        (shallow / "src/theory").mkdir(parents=True)
        p = self.launch("--use-local", str(shallow), "--since", base, "--show-prompt", **env)
        self.assertEqual(p.returncode, 2)
        self.assertIn("shallow clone", p.stderr)
        self.assertEqual(git("status", "--porcelain"), "")
        self.assertEqual(git("rev-parse", "HEAD"), base)
        self.assertFalse(capture.exists())


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
