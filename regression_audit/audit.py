"""Read regression exclusions and retain the source evidence for each one.

This is an inventory of source exclusions, not a simulation of a CI run.
In particular, absence of a disable does not mean a tester is selected or that
its applies() predicate holds. The harness is parsed, never imported/executed.
"""
from __future__ import annotations

import ast
from pathlib import Path
import re
import shlex

TESTERS = ("proof", "cpc", "cpc-logos")
CLI = Path("test/regress/cli")
HARNESS = CLI / "run_regression.py"
CMAKE = CLI / "CMakeLists.txt"
METADATA = re.compile(
    r"^(DISABLE-TESTER|COMMAND-LINE|EXPECT-ERROR|EXPECT|ERROR-SCRUBBER|"
    r"SCRUBBER|REQUIRES|EXIT):\s*(.*)$"
)
# Only identify a possible reason when a comment both names proof checking
# and explains a restriction. Other adjacent prose remains context, not a why.
PROOF_WORD = re.compile(r"\b(proofs?|cpc(?:-logos)?|ethos|logos|checkers?)\b", re.I)
REASON_WORD = re.compile(
    r"disabl|due to|because|since|cannot|can't|fail|unsupported|not supported|"
    r"timeout|time out|interfer|slow|overload", re.I
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_harness(text: str) -> tuple[set[str], set[str], dict[str, dict[str, int]]]:
    """Read literal tester registrations and disable cascades in cvc5's runner.

    The supported cascade shape is `if disable_tester == "proof": ...
    testers.remove("cpc")`. Refuse dynamic removal targets instead of silently
    dropping them when a future runner changes this contract.
    """
    tree = ast.parse(text, filename=str(HARNESS))
    assignments = {
        target.id: node.value
        for node in tree.body if isinstance(node, ast.Assign)
        for target in node.targets if isinstance(target, ast.Name)
    }
    registry = assignments.get("g_testers")
    if not isinstance(registry, ast.Dict) or not registry.keys:
        raise ValueError(f"{HARNESS}: expected a literal g_testers dictionary")
    registered = set()
    for key in registry.keys:
        if not isinstance(key, ast.Constant) or not isinstance(key.value, str):
            raise ValueError(f"{HARNESS}: nonliteral tester registration")
        registered.add(key.value)
    try:
        defaults = ast.literal_eval(assignments["g_default_testers"])
    except (KeyError, ValueError, TypeError) as exc:
        raise ValueError(f"{HARNESS}: expected literal g_default_testers") from exc
    if not isinstance(defaults, (list, tuple)) or any(
        not isinstance(t, str) or t not in registered for t in defaults
    ):
        raise ValueError(f"{HARNESS}: invalid default testers")

    cascades: dict[str, dict[str, int]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.If) or not isinstance(node.test, ast.Compare):
            continue
        test = node.test
        if len(test.ops) != 1 or not isinstance(test.ops[0], ast.Eq):
            continue
        left, right = test.left, test.comparators[0]
        if isinstance(right, ast.Name) and right.id == "disable_tester":
            left, right = right, left
        if not (isinstance(left, ast.Name) and left.id == "disable_tester"
                and isinstance(right, ast.Constant) and isinstance(right.value, str)):
            continue
        removed = cascades.setdefault(right.value, {})
        for statement in node.body:
            for call in ast.walk(statement):
                if not (isinstance(call, ast.Call)
                        and isinstance(call.func, ast.Attribute)
                        and isinstance(call.func.value, ast.Name)
                        and call.func.value.id == "testers"
                        and call.func.attr == "remove"):
                    continue
                if (len(call.args) != 1 or not isinstance(call.args[0], ast.Constant)
                        or not isinstance(call.args[0].value, str)):
                    raise ValueError(f"{HARNESS}:{call.lineno}: dynamic disable cascade")
                removed[call.args[0].value] = call.lineno
    return registered, set(defaults), cascades


def _metadata(line: str):
    # Match the runner: exactly one leading semicolon in column zero. An
    # indented or double-commented directive is ignored by run_regression.py.
    return METADATA.match(line[1:].lstrip()) if line.startswith(";") else None


def _context(lines: list[str], index: int, path: str) -> list[dict]:
    groups = []
    for direction in (-1, 1):
        pos = index + direction
        # A prose comment can explain a consecutive block of disabled testers.
        while 0 <= pos < len(lines):
            meta = _metadata(lines[pos])
            if not meta or meta[1] != "DISABLE-TESTER":
                break
            pos += direction
        comments = []
        while 0 <= pos < len(lines) and lines[pos].startswith(";"):
            prose = lines[pos].lstrip("; \t").strip()
            if not prose or METADATA.match(prose):
                break
            comments.append((pos + 1, prose))
            pos += direction
        if comments:
            comments.sort()
            groups.append({"location": f"{path}:{comments[0][0]}",
                           "text": " ".join(text for _, text in comments)})
    return groups


def read_directives(text: str, path: str, registered: set[str], cascades: dict):
    lines = text.splitlines()
    directives, commands = [], []
    for index, line in enumerate(lines):
        meta = _metadata(line)
        if not meta:
            continue
        kind, value = meta[1], meta[2].strip()
        if kind == "COMMAND-LINE":
            commands.append(value)
        if kind != "DISABLE-TESTER":
            continue
        if value not in registered:
            raise ValueError(f"{path}:{index + 1}: unknown DISABLE-TESTER {value!r}")
        affected = set(cascades.get(value, {})) | {value}
        affected &= registered & set(TESTERS)
        if not affected:
            continue
        context = _context(lines, index, path)
        reasons = [c for c in context if PROOF_WORD.search(c["text"])
                   and REASON_WORD.search(c["text"])]
        directives.append({
            "tester": value,
            "location": f"{path}:{index + 1}",
            "affects": [t for t in TESTERS if t in affected],
            "inherited_at": {
                t: f"{HARNESS}:{n}" for t, n in cascades.get(value, {}).items()
                if t in affected and t != value
            },
            "reason_comments": reasons,
            "context": [c for c in context if c not in reasons],
        })
    return directives, commands


def read_suite_disables(text: str) -> dict[str, dict]:
    """Read cvc5's literal disabled list; comments attach only to the next entry.

    Do not spread a reason to following entries: CMake provides no grouping
    syntax for reasons, and doing so would attribute unrelated exclusions.
    """
    start = re.search(r"(?m)^\s*set\(regression_disabled_tests\b", text)
    if not start:
        raise ValueError(f"{CMAKE}: missing regression_disabled_tests list")
    disabled = {}
    comments = []
    for number, line in enumerate(text[start.end():].splitlines(),
                                  text.count("\n", 0, start.end()) + 1):
        stripped = line.strip()
        if stripped == ")":
            return disabled
        if not stripped:
            comments = []
            continue
        if stripped.startswith("#"):
            prose = stripped.lstrip("# ").strip()
            if prose:
                comments.append({"location": f"{CMAKE}:{number}", "text": prose})
            else:
                comments = []
            continue
        code, _, inline = line.partition("#")
        entries = shlex.split(code)
        for entry in entries:
            if not re.fullmatch(r"regress[^\s$()]*\.(?:smt2|sy)", entry):
                raise ValueError(f"{CMAKE}:{number}: unsupported disabled entry {entry!r}")
            if entry in disabled:
                raise ValueError(f"{CMAKE}:{number}: duplicate disabled entry {entry}")
            reason = comments + ([{"location": f"{CMAKE}:{number}",
                                   "text": inline.strip()}] if inline.strip() else [])
            disabled[entry] = {"location": f"{CMAKE}:{number}",
                               "reason_comments": reason}
            comments = []
    raise ValueError(f"{CMAKE}: unterminated regression_disabled_tests list")


def scan(root: Path) -> dict:
    root = Path(root).resolve()
    registered, defaults, cascades = read_harness(_read(root / HARNESS))
    suite_disables = read_suite_disables(_read(root / CMAKE))
    files = sorted(p for p in (root / CLI).rglob("*")
                   if p.is_file() and p.suffix in (".smt2", ".sy"))
    if not files:
        raise ValueError(f"{root / CLI}: no .smt2 or .sy regressions found")
    missing = set(suite_disables) - {p.relative_to(root / CLI).as_posix() for p in files}
    if missing:
        raise ValueError(f"{CMAKE}: disabled regression files missing: {', '.join(sorted(missing))}")
    rows = []
    for path in files:
        relative = path.relative_to(root).as_posix()
        directives, commands = read_directives(_read(path), relative, registered, cascades)
        suite = suite_disables.get(path.relative_to(root / CLI).as_posix())
        if directives or suite:
            rows.append({"path": relative, "directives": directives,
                         "suite_disabled": suite, "command_lines": commands})
    testers = {}
    for tester in TESTERS:
        present = tester in registered
        direct = {r["path"] for r in rows
                  if any(d["tester"] == tester for d in r["directives"])}
        inherited = {r["path"] for r in rows
                     if any(tester in d["inherited_at"] for d in r["directives"])}
        suite = {r["path"] for r in rows if r["suite_disabled"]} if present else set()
        testers[tester] = {
            "status": "registered" if present else (
                "planned (not registered)" if tester == "cpc-logos" else "not registered"),
            "default": tester in defaults,
            "direct": len(direct),
            "inherited_only": len(inherited - direct),
            "suite_disabled": len(suite) if present else None,
            "total_disabled": len(direct | inherited | suite) if present else None,
        }
    return {"schema_version": 1, "checkout": str(root), "files_scanned": len(files),
            "testers": testers, "regressions": rows}
