"""Locate the exact Koine dependency. No network and no checkout mutations."""
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent

# Koine owns the tooling; bug_db/ in a consumer holds that consumer's data.
# Probe the implementation, never the retired root entry point.
SCRIPT = Path("bug_db_manager/koine_append_db")


def append_db():
    pin = (ROOT / "scripts/koine.lock").read_text().strip()
    explicit = os.environ.get("KOINE")
    candidates = [Path(explicit).expanduser()] if explicit else [ROOT.parent / "koine", ROOT / "deps/koine"]
    problems = []
    for path in candidates:
        script = path / SCRIPT
        if not script.is_file():
            stale = " (retired layout; update the checkout)" if any(
                (path / old).is_file() for old in (SCRIPT.name, "bug_db/koine_append_db")) else ""
            problems.append(f"{path}: no {SCRIPT}{stale}")
            continue
        rev = subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True, text=True)
        dirty = subprocess.run(["git", "-C", str(path), "status", "--porcelain", "--untracked-files=no"],
                               capture_output=True, text=True)
        if rev.returncode or rev.stdout.strip() != pin or dirty.returncode or dirty.stdout.strip():
            problems.append(f"{path}: needs clean pinned commit {pin}")
            continue
        return script.resolve()
    raise ValueError("Koine unavailable: " + "; ".join(problems)
                     + ". Set KOINE to a clean checkout at scripts/koine.lock. No checkout was changed.")
