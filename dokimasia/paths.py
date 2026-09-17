"""Repository data paths, independent of the caller's working directory."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASELINES = ROOT / "tests" / "baselines"
CENSUS = ROOT / "tests" / "corpus" / "reach-corpus.json"


def baseline(analysis: str) -> Path:
    return BASELINES / f"{analysis}.json"
