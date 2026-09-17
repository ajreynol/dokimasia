"""Locate the exact Koine dependency. No network and no checkout mutations."""
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent


def append_db():
    pin = (ROOT / "scripts/koine.lock").read_text().strip()
    explicit = os.environ.get("KOINE")
    candidates = [Path(explicit).expanduser()] if explicit else [ROOT.parent / "koine", ROOT / "deps/koine"]
    problems = []
    for path in candidates:
        script = path / "koine_append_db"
        if not script.is_file():
            problems.append(f"{path}: no koine_append_db")
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
