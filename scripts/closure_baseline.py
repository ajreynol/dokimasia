"""The cvc5 revision recorded by Dokimasia, for Koine's closure window."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "bug_db/bugs.json"


def baseline(explicit=None):
    """The revision the recorded observations were taken against.

    The newest run archive, because that is the revision the claims in the
    database describe. `scripts/cvc5.lock` is the fallback and not the default:
    it pins the revision tests reproduce, which is a different question and is
    routinely older than the last run.
    """
    if explicit:
        return explicit, "--since"
    runs = []
    for path in sorted((DB.parent / "runs").glob("*.json")):
        record = json.loads(path.read_text())
        for target in record.get("targets", []):
            if target.get("project") == "cvc5" and target.get("commit"):
                runs.append((record.get("observed_on", ""), path.name, target["commit"]))
    if runs:
        observed, name, commit = max(runs)
        return commit, f"bug_db/runs/{name}, observed {observed}"
    lock = json.loads((ROOT / "scripts/cvc5.lock").read_text())["cvc5"]["commit"]
    return lock, "scripts/cvc5.lock"


if __name__ == "__main__":
    print("cvc5", *baseline())
