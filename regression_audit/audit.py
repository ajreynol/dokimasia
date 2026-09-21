"""Read regression exclusions and retain the source evidence for each one.

This is an inventory of source exclusions, not a simulation of a CI run.
In particular, absence of a disable does not mean a tester is selected or that
its applies() predicate holds. The harness is parsed, never imported/executed.
"""
from __future__ import annotations

import ast
from pathlib import Path
import re

TESTERS = ("proof", "cpc", "cpc-logos")
CLI = Path("test/regress/cli")
HARNESS = CLI / "run_regression.py"
METADATA = re.compile(
    r"^(DISABLE-TESTER|COMMAND-LINE|EXPECT-ERROR|EXPECT|ERROR-SCRUBBER|"
    r"SCRUBBER|REQUIRES|EXIT):\s*(.*)$"
)
# Timeout and slowness comments often omit the tester name. Otherwise require
# both proof-checking vocabulary and a restriction; keep unrelated prose as context.
PROOF_WORD = re.compile(r"\b(proofs?|cpc(?:-logos)?|ethos|logos|checkers?)\b", re.I)
REASON_WORD = re.compile(
    r"disabl|due to|because|since|cannot|can't|fail|unsupported|not supported|"
    r"timeout|time out|interfer|slow|overload", re.I
)
TIMEOUT_WORD = re.compile(r"\b(?:timeouts?|tim(?:e[ds]?|ing)[ -]+outs?)\b(?![-_])", re.I)
SLOW_WORD = re.compile(r"\bslow(?:er|ly)?\b|\btakes a long time\b", re.I)


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
        reasons = [c for c in context if TIMEOUT_WORD.search(c["text"])
                   or SLOW_WORD.search(c["text"])
                   or (PROOF_WORD.search(c["text"]) and REASON_WORD.search(c["text"]))]
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


def scan(root: Path) -> dict:
    root = Path(root).resolve()
    registered, defaults, cascades = read_harness(_read(root / HARNESS))
    files = sorted(p for p in (root / CLI).rglob("*")
                   if p.is_file() and p.suffix in (".smt2", ".sy"))
    if not files:
        raise ValueError(f"{root / CLI}: no .smt2 or .sy regressions found")
    rows = []
    for path in files:
        relative = path.relative_to(root).as_posix()
        directives, commands = read_directives(_read(path), relative, registered, cascades)
        if directives:
            rows.append({"path": relative, "directives": directives,
                         "command_lines": commands})
    testers = {}
    for tester in TESTERS:
        present = tester in registered
        direct = {r["path"] for r in rows
                  if any(d["tester"] == tester for d in r["directives"])}
        inherited = {r["path"] for r in rows
                     if any(tester in d["inherited_at"] for d in r["directives"])}
        testers[tester] = {
            "status": "registered" if present else (
                "planned (not registered)" if tester == "cpc-logos" else "not registered"),
            "default": tester in defaults,
            "direct": len(direct),
            "inherited_only": len(inherited - direct),
            "total_disabled": len(direct | inherited) if present else None,
        }
    return {"schema_version": 1, "checkout": str(root), "files_scanned": len(files),
            "testers": testers, "regressions": rows}
