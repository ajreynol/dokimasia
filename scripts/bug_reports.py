"""Dokimasia's dump validation and report rendering; Koine alone edits the DB.

`render` rewrites `bug_db/bugs.md` from Dokimasia's database artifact. Koine
provides the only database writer; Dokimasia owns the records and evidence.
Triage decisions remain in the reviewed register, outside the generated page.
"""
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.parse import quote

from dokimasia_analyzer.findings import observation
import koine

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "bug_db/bugs.json"
PAGE = DB.with_suffix(".md")


def write(path, body):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(body)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def write_json(path, data):
    write(path, json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n")


def read_dump(path):
    data = json.loads(Path(path).read_text())
    if not isinstance(data, list):
        raise ValueError("a findings dump must be a JSON list")
    seen = set()
    for row in data:
        if not isinstance(row, dict) or not isinstance(row.get("description"), str) or not row["description"].strip():
            raise ValueError("each finding needs an object with a nonempty description")
        expected = observation(row.get("code"), row.get("entity"))
        if set(row) != set(expected):
            raise ValueError("dump fields must match finding_id.py --record; put run evidence in the sidecar")
        for key, value in expected.items():
            if key != "description" and row[key] != value:
                raise ValueError(f"invalid {key}: {row[key]!r}")
        if row["id"] in seen:
            raise ValueError(f"duplicate finding id: {row['id']}")
        seen.add(row["id"])
    return data


def read_run(path, bugs):
    run = json.loads(Path(str(path) + ".run.json").read_text())
    if not isinstance(run, dict) or run.get("dump_sha256") != hashlib.sha256(Path(path).read_bytes()).hexdigest():
        raise ValueError("run record does not match the dump")
    if run.get("producer") not in ("program", "agent") or not isinstance(run.get("complete"), bool):
        raise ValueError("run record needs producer and complete fields")
    from dokimasia_analyzer.findings import ANALYSES, CHECKS
    analyses = run.get("analyses")
    if not isinstance(analyses, list) or not analyses or any(not isinstance(a, str) for a in analyses) or set(analyses) - set(ANALYSES):
        raise ValueError("run record needs known analyses")
    if not isinstance(run.get("targets"), list) or not run["targets"] or not isinstance(run.get("coverage"), dict) or not run["coverage"]:
        raise ValueError("run record needs targets and actual coverage")
    for t in run["targets"]:
        if not isinstance(t, dict) or not all(isinstance(t.get(k), str) for k in ("id", "project", "commit", "input_sha256")):
            raise ValueError("target provenance is incomplete")
        if not re.fullmatch(r"[0-9a-f]{64}", t["input_sha256"]) or not isinstance(t.get("files"), list) or not all(isinstance(p, str) for p in t["files"]):
            raise ValueError("target provenance is incomplete")
    evidence = run.get("evidence", {})
    if not isinstance(evidence, dict) or any(not isinstance(rows, dict) for rows in evidence.values()):
        raise ValueError("evidence must map targets to findings")
    if run["producer"] == "program" and not run["complete"]:
        raise ValueError("incomplete program run cannot be appended")
    for bug in bugs:
        if CHECKS[bug["code"]][0] not in run["analyses"]:
            raise ValueError(f"{bug['id']}: check is outside the selected analyses")
        if not any(isinstance(rows.get(bug["id"]), list) and rows[bug["id"]]
                   and all(isinstance(e, dict) and e for e in rows[bug["id"]]) for rows in evidence.values()):
            raise ValueError(f"{bug['id']}: no evidence in run record")
    return run


def render(db=DB, page=None):
    db = Path(db).resolve()
    page = Path(page).resolve() if page else db.parent / PAGE.name
    bugs = json.loads(db.read_text())["bugs"]
    def link(path):
        return quote(Path(os.path.relpath(path, page.parent)).as_posix(), safe="/.")
    lines = ["# Dokimasia bug database", "",
        f"Generated from [bugs.json]({link(db)}) by `scripts/append_findings --render-only`, "
        "and **rewritten whole**: anything typed in here is lost on the next run.", "",
        "This is observation history, not a list of confirmed defects or open reports.",
        "Dokimasia owns this artifact; Koine supplies the writer. Dates record ingestion, not fresh confirmation.",
        "The first claim is preserved. Disappearance does not close a finding.",
        f"[Archived run records]({link(db.parent / 'runs')}/) contain the source revisions, actual coverage and evidence keyed by id.",
        # Named, not linked. A generated page that links a hand-written
        # document re-creates a stale cross-reference on every render, which is
        # how this one survived a documentation refactor pointing nowhere.
        "See `docs/maintenance.md` for evidence, limitations and the historical register.", "",
        f"{len(bugs)} observation(s).", "",
        "| id | check | entity | first seen | last seen | original claim |",
        "| --- | --- | --- | --- | --- | --- |"]
    def cell(value):
        return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "&#124;").replace("`", "&#96;").replace("\n", " ")
    for b in bugs:
        lines.append("| " + " | ".join(cell(b.get(k, "")) for k in
                     ("id", "code", "entity", "first_seen", "last_seen", "description")) + " |")
    return "\n".join(lines) + "\n"


@contextmanager
def writer(db):
    """Serialize this repository's writers around Koine's atomic replacement."""
    db = Path(db)
    db.parent.mkdir(parents=True, exist_ok=True)
    with open(str(db) + ".lock", "a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError(f"another writer is updating {db}") from None
        yield


def append(dump, db=DB, page=PAGE, dry_run=False, date=None):
    paths = [Path(p).resolve() for p in (dump, str(dump) + ".run.json", db, page)]
    if len(set(paths)) != len(paths):
        raise ValueError("dump, evidence, database and page must be different files")
    bugs = read_dump(dump)
    run = read_run(dump, bugs)
    script = koine.script()
    argv = [sys.executable, str(script), str(dump), str(db)]
    if dry_run:
        argv.append("--dry-run")
    if date:
        argv += ["--date", date]
    if dry_run:
        return subprocess.run(argv).returncode
    with writer(db):
        # This lock covers the archive, append and rendering. Koine uses the
        # same lock file; taking it again in the child would deadlock.
        argv.append("--no-lock")
        archive = dict(run, observations=bugs)
        body = json.dumps(archive, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
        name = hashlib.sha256(body.encode()).hexdigest() + ".json"
        write(Path(db).parent / "runs" / name, body)
        rc = subprocess.run(argv).returncode
        if rc == 0:
            write(page, render(db, page))
        return rc
