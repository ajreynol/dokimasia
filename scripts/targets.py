"""Shared source scope for the program and agent. Never fetches or checks out."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dokimasia.findings import ANALYSES, DEFAULT_ANALYSES
from dokimasia.paths import CENSUS

CONFIG = ROOT / "scripts/targets.json"


def git(root, *args):
    p = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    return p.stdout.strip() if p.returncode == 0 else ""


def checkout(explicit=None):
    if explicit:
        return Path(explicit).expanduser().resolve(), "--cvc5"
    for key in ("DOKIMASIA_CVC5", "CVC5"):
        if os.environ.get(key):
            return Path(os.environ[key]).expanduser().resolve(), "$" + key
    mapping = Path(os.environ.get("DOKIMASIA_REPOS_FILE", ROOT / "scripts/repos.local"))
    if mapping.exists():
        for line in mapping.read_text().splitlines():
            line = line.split("#", 1)[0].strip()
            parts = line.split(None, 1)
            if parts and parts[0] == "cvc5":
                if len(parts) != 2:
                    raise ValueError(f"{mapping}: cvc5 needs a checkout path")
                path = Path(parts[1]).expanduser()
                return (mapping.parent / path).resolve(), str(mapping)
    # The last fallback, and the one a reporting setup may already name.
    local_config = ROOT / "scripts/deps.local.json"
    if local_config.exists():
        path = json.loads(local_config.read_text()).get("cvc5", {}).get("path")
        if path:
            return Path(path).expanduser().resolve(), str(local_config)
    return ROOT / "deps/cvc5", "deps/cvc5"


def resolve(config=CONFIG, selected=(), explicit=None):
    specs = json.loads(Path(config).read_text())["targets"]
    if not specs or len({s["id"] for s in specs}) != len(specs):
        raise ValueError("targets must have unique ids and must not be empty")
    unknown = set(selected) - {s["id"] for s in specs}
    if unknown:
        raise ValueError(f"unknown targets: {sorted(unknown)}")
    root, via = checkout(explicit)
    resolved = []
    for spec in specs:
        if selected and spec["id"] not in selected:
            continue
        if spec["project"] != "cvc5":
            raise ValueError("Dokimasia targets must be cvc5 checkouts")
        patterns = spec["paths"]
        required = spec["required"]
        if not patterns or not required:
            raise ValueError("targets need input patterns and required paths")
        for pattern in patterns + required:
            p = Path(pattern)
            if p.is_absolute() or ".." in p.parts:
                raise ValueError(f"target path escapes checkout: {pattern}")
        missing = [p for p in required if not (root / p).exists()]
        files = sorted({p.relative_to(root).as_posix() for pat in patterns for p in root.glob(pat)
                        if p.is_file() and not any(x in {".git", "__pycache__", "build", "deps"}
                                                  for x in p.relative_to(root).parts)})
        for rel in files:
            if not (root / rel).resolve().is_relative_to(root):
                raise ValueError(f"target file points outside checkout: {rel}")
        resolved.append({"id": spec["id"], "project": "cvc5", "root": str(root),
                         "resolved_by": via, "commit": git(root, "rev-parse", "HEAD"),
                         "dirty": bool(git(root, "status", "--porcelain")),
                         "files": files, "missing": missing})
    return resolved


def require_targets(resolved):
    for t in resolved:
        if t["missing"] or not t["files"]:
            raise ValueError(f"{t['id']}: incomplete checkout at {t['root']}; missing {t['missing'] or 'all input files'}")


def describe(resolved, analyses):
    lines = ["Analyses: " + ", ".join(analyses),
             "Input scope (individual scanners may read a subset); no analysis or fetch:"]
    for t in resolved:
        lines += [f"{t['id']}: {t['root']} (from {t['resolved_by']})",
                  f"  revision: {t['commit'] or 'not a git checkout'}; dirty: {t['dirty']}",
                  f"  {len(t['files'])} input file(s)"]
        lines += ["  " + f for f in t["files"]]
        lines += ["  MISSING: " + f for f in t["missing"]]
    return "\n".join(lines)


def snapshot(resolved):
    """Portable provenance, including dirty content, without machine paths."""
    result = []
    for t in resolved:
        h = hashlib.sha256()
        for rel in t["files"]:
            h.update(rel.encode() + b"\0")
            h.update(hashlib.sha256((Path(t["root"]) / rel).read_bytes()).digest())
        result.append({k: t[k] for k in ("id", "project", "commit", "dirty", "files")}
                      | {"input_sha256": h.hexdigest()})
    return result


def implementation_digest(analyses=DEFAULT_ANALYSES):
    """Identify the exact analyzer implementation, including uncommitted edits."""
    files = sorted((ROOT / "dokimasia").rglob("*.py")) + [ROOT / p for p in (
        "scripts/dokimasia_analyzer", "scripts/targets.py", "scripts/targets.json",
        "scripts/bug_reports.py", "scripts/koine.py", "scripts/koine.lock")]
    if "latent" in analyses:
        files.append(CENSUS)
    h = hashlib.sha256()
    for p in sorted(files):
        h.update(p.relative_to(ROOT).as_posix().encode() + b"\0")
        h.update(hashlib.sha256(p.read_bytes()).digest())
    return h.hexdigest()


def arguments(parser):
    parser.add_argument("--cvc5", help="explicit checkout; otherwise environment, repos.local, "
                        "deps.local.json, then deps/cvc5")
    parser.add_argument("--config", default=str(CONFIG))
    parser.add_argument("--target", action="append", default=[])
    parser.add_argument("--analysis", action="append", choices=ANALYSES,
                        help="select an analysis; repeatable; default: " + ", ".join(DEFAULT_ANALYSES))


def from_args(args):
    return resolve(args.config, args.target, args.cvc5)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Resolve the cvc5 checkout for reporting and analysis.")
    parser.add_argument("checkout", nargs="?", help="explicit checkout, overriding local configuration")
    args = parser.parse_args()
    try:
        path, via = checkout(args.checkout)
        if not path.is_dir():
            raise ValueError(f"no cvc5 checkout at {path} (from {via}); provide a path, "
                             "set DOKIMASIA_CVC5, or configure scripts/repos.local")
        print(via)
        print(path)
    except (OSError, ValueError) as e:
        parser.exit(2, f"targets: {e}\n")
