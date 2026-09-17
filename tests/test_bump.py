"""The pin on anoieu moves only onto a commit anoieu's own CI was green at.

The requirement is anoieu's, and the half of it we can be held to is the
*refusal*: work anoieu could not get past its own build is not work to take on.
What matters more than the refusal is that **unknown is not green** -- an
unreachable remote, an unfinished run and a commit nothing is reported about
are all different from a failure, and none of them is a pass.

These cases are synthetic payloads, so the test makes no network call and fails
only for a reason in this tree.

Run: python3 tests/test_bump.py
"""
import importlib.machinery
import importlib.util
import json
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SCRIPT = os.path.join(ROOT, "scripts", "bump_anoieu")
FAILURES = []


def load_script():
    loader = importlib.machinery.SourceFileLoader("bump_anoieu", SCRIPT)
    spec = importlib.util.spec_from_loader("bump_anoieu", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def check(label, got, want):
    ok = got == want
    print(f"  {'ok  ' if ok else 'FAIL'} {label}: {got!r}" + ("" if ok else f" != {want!r}"))
    if not ok:
        FAILURES.append(label)


def verdict(bump, payload, monkey):
    """`green()` against a canned check-runs response."""
    monkey(payload)
    ok, _why = bump.green({"url": "https://github.com/ajreynol/anoieu"}, "0" * 40)
    return ok


def main():
    bump = load_script()

    check("the clone URL yields owner and repository",
          bump.owner_repo("https://github.com/ajreynol/anoieu.git"),
          ("ajreynol", "anoieu"))

    class Response:
        def __init__(self, body):
            self.body = body

        def read(self):
            return self.body

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    state = {}

    def monkey(payload):
        state["payload"] = payload

        def urlopen(_request, timeout=None):
            if isinstance(payload, Exception):
                raise payload
            return Response(json.dumps(payload).encode())

        bump.urllib.request.urlopen = urlopen

    run = {"name": "suites (3.12)", "status": "completed", "conclusion": "success"}

    check("every check successful is green",
          verdict(bump, {"total_count": 1, "check_runs": [run]}, monkey), True)
    check("one failure is not green",
          verdict(bump, {"total_count": 2, "check_runs": [
              run, dict(run, name="corpus", conclusion="failure")]}, monkey), False)
    check("a cancelled run is not green",
          verdict(bump, {"total_count": 1, "check_runs": [
              dict(run, conclusion="cancelled")]}, monkey), False)
    check("a run still going is unknown, not green",
          verdict(bump, {"total_count": 1, "check_runs": [
              dict(run, status="in_progress", conclusion=None)]}, monkey), None)
    check("no checks at all is unknown, not green",
          verdict(bump, {"total_count": 0, "check_runs": []}, monkey), None)
    check("a truncated page is unknown, not green",
          verdict(bump, {"total_count": 9, "check_runs": [run]}, monkey), None)
    check("an unreachable remote is unknown, not green",
          verdict(bump, OSError("no network"), monkey), None)

    # The exit codes exist so that a run can log which refusal it hit.
    check("an unverified refusal has its own exit code",
          bump.UNVERIFIED not in (0, 1), True)


if __name__ == "__main__":
    main()
    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)}: {', '.join(FAILURES)}")
        sys.exit(1)
    print("all checks passed")
