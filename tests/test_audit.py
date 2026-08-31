"""Tests for the LOC audit.

Run: python3 tests/test_audit.py
"""
import os, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import importlib.util  # noqa: E402
from importlib.machinery import SourceFileLoader  # noqa: E402

# the script has no .py extension, so the loader must be named explicitly
_PATH = os.path.join(os.path.dirname(__file__), "..", "scripts", "audit_loc")
_spec = importlib.util.spec_from_loader("audit_loc", SourceFileLoader("audit_loc", _PATH))
audit = importlib.util.module_from_spec(_spec)
# @dataclass resolves annotations through sys.modules, so register before exec
sys.modules["audit_loc"] = audit
_spec.loader.exec_module(audit)

FAILURES = []


def check(label, got, want):
    ok = got == want
    print(f"  {'ok  ' if ok else 'FAIL'} {label}: {got!r}" + ("" if ok else f" != {want!r}"))
    if not ok:
        FAILURES.append(label)


def test_classification():
    print("line classification:")
    c = audit._classify_python('"""A docstring.\n\nTwo lines of it.\n"""\nx = 1  # trailing\n# whole\n\ny = 2\n')
    check("a docstring counts as comment", c.comment, 4)
    check("a line with a trailing comment is code", c.code, 2)
    check("a whole-line comment is comment", c.comment >= 4, True)
    check("blanks are blanks", c.blank, 2)

    # a `#` inside a string is not a comment -- the reason this uses tokenize
    c2 = audit._classify_python('s = "# not a comment"\n')
    check("a hash inside a string is code", (c2.code, c2.comment), (1, 0))

    c3 = audit._classify_markdown("# Title\n\nprose\n")
    check("markdown is prose, never code", (c3.prose, c3.code), (2, 0))
    c4 = audit._classify_data('{\n  "a": 1\n}\n')
    check("json is data, never prose", (c4.data, c4.prose), (3, 0))


def test_attribution():
    print("file attribution:")
    check("an engine module", audit._attribute("dokimasia/ledger/build.py"), ("ledger", "engine"))
    check("a CLI", audit._attribute("dokimasia/ledger/__main__.py"), ("ledger", "cli"))
    check("shared infrastructure", audit._attribute("dokimasia/sanity.py"), ("(shared)", "engine"))
    check("a test maps to its analysis",
          audit._attribute("tests/test_ledger.py"), ("ledger", "tests"))
    check("a baseline", audit._attribute("ledger-baseline.json"), ("ledger", "baseline"))
    check("a doc", audit._attribute("docs/issues.md"), ("(docs)", "docs"))


def test_totals():
    print("totals are consistent:")
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "dokimasia", "x"))
        with open(os.path.join(tmp, "dokimasia", "x", "y.py"), "w") as fh:
            fh.write("# c\nx = 1\n\n")
        infos = audit.collect(tmp)
        check("one file found", len(infos), 1)
        c = infos[0].count
        check("code + comment + blank equals the file length",
              c.code + c.comment + c.blank, 3)
        check("total agrees", c.total, 3)


if __name__ == "__main__":
    test_classification(); print()
    test_attribution(); print()
    test_totals(); print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)}: {', '.join(FAILURES)}")
        sys.exit(1)
    print("all checks passed")
