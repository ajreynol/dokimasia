"""Read cvc5's CI configuration and regression runner as data.

Two files decide whether proofs are tested at all:

``.github/workflows/*.yml``
    a build matrix; each entry names a config and the ``--tester`` list its
    regression run uses.
``test/regress/cli/run_regression.py``
    the testers themselves, and the cvc5 flags each one adds.

The workflow YAML is read with an indentation scanner rather than a YAML
parser, to keep this dependency-free. The matrix entries have a fixed shape --
``- name:`` followed by ``key: value`` lines -- which is all that is needed.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from ..sanity import expect

#: Testers whose purpose is to exercise proof production.
PROOF_TESTERS = frozenset({"proof", "cpc", "lfsc", "alethe", "unsat-core"})

#: The tester that makes cvc5 check its own proofs, as opposed to printing them.
CHECKING_TESTER = "proof"


@dataclass
class Job:
    name: str
    workflow: str
    config: str = ""
    testers: list[str] = field(default_factory=list)
    exclude_regress: str = ""

    @property
    def proof_testers(self) -> list[str]:
        return [t for t in self.testers if t in PROOF_TESTERS]

    @property
    def mode(self) -> str:
        """safe | stable | unrestricted, from the build config."""
        if "safe-mode" in self.config:
            return "safe"
        if "stable-mode" in self.config:
            return "stable"
        return "unrestricted"


@dataclass
class Tester:
    name: str
    flags: list[str] = field(default_factory=list)
    line: int = 0


@dataclass
class CiModel:
    jobs: list[Job] = field(default_factory=list)
    testers: dict[str, Tester] = field(default_factory=dict)
    default_testers: list[str] = field(default_factory=list)

    def jobs_with_proofs(self) -> list[Job]:
        return [j for j in self.jobs if j.proof_testers]

    def modes_promising_proofs(self) -> list[Job]:
        """Jobs whose build config carries the completeness contract."""
        return [j for j in self.jobs if j.mode in ("safe", "stable")]

    def completeness_chain(self) -> list[tuple[str, bool, str]]:
        """The links the completeness guarantee hangs on.

        `--check-proofs-complete` is never named in the configuration. In a safe
        build, `setDefaultsPre` turns it on when `--check-proofs` is set and no
        granularity was requested -- so completeness is tested only as a side
        effect, through a chain nothing asserts.
        """
        safe = [j for j in self.jobs if j.mode == "safe"]
        with_proof = [j for j in safe if CHECKING_TESTER in j.testers]
        pt = self.testers.get(CHECKING_TESTER)
        flags = pt.flags if pt else []
        has_check = any("--check-proofs" == f for f in flags)
        no_gran = not any(f.startswith("--proof-granularity") for f in flags)
        explicit = any("--check-proofs-complete" in f for f in flags)
        return [
            ("a build job runs in safe mode", bool(safe),
             ", ".join(j.name for j in safe) or "none"),
            (f"that job runs --tester {CHECKING_TESTER}", bool(with_proof),
             ", ".join(j.name for j in with_proof) or "none"),
            ("the tester passes --check-proofs", has_check,
             " ".join(flags) or "none"),
            ("the tester requests no --proof-granularity", no_gran,
             "none requested" if no_gran else "a granularity is set"),
            ("completeness is named explicitly", explicit,
             "--check-proofs-complete appears nowhere" if not explicit else "yes"),
        ]


_ENTRY = re.compile(r"^(\s+)- name:\s*(.+?)\s*$")
_KV = re.compile(r"^(\s+)([a-z_-]+):\s*(.*?)\s*$")


def _parse_workflow(path: str, name: str) -> list[Job]:
    with open(path, encoding="utf-8", errors="ignore") as fh:
        lines = fh.read().split("\n")
    jobs: list[Job] = []
    cur: Job | None = None
    indent = 0
    for ln in lines:
        m = _ENTRY.match(ln)
        if m:
            # only matrix entries carry a config or a tester list; steps do not
            cur = Job(name=m.group(2), workflow=name)
            indent = len(m.group(1))
            jobs.append(cur)
            continue
        if cur is None:
            continue
        kv = _KV.match(ln)
        if not kv or len(kv.group(1)) <= indent:
            if ln.strip() and not ln.startswith(" " * (indent + 1)):
                cur = None
            continue
        key, val = kv.group(2), kv.group(3)
        if key == "config":
            cur.config = val
        elif key == "run_regression_args":
            cur.testers = re.findall(r"--tester\s+([a-z-]+)", val)
        elif key == "exclude_regress":
            cur.exclude_regress = val
    # matrix entries are the ones that named a config; the rest are steps
    return [j for j in jobs if j.config or j.testers]


def _parse_testers(path: str) -> tuple[dict[str, Tester], list[str]]:
    with open(path, encoding="utf-8", errors="ignore") as fh:
        text = fh.read()
    testers: dict[str, Tester] = {}
    for m in re.finditer(r'super\(\)\.__init__\("([a-z-]+)"\)', text):
        name = m.group(1)
        line = text.count("\n", 0, m.start()) + 1
        # Testers build their argument lists in several shapes -- appended to
        # command_line_args, prepended to it, or via a local list that itself
        # contains an index expression. Rather than model each, take every
        # "--flag" literal in the class body. An approximation: a flag named in
        # a comment or an error message would be counted, so the flags are
        # evidence to read, not a contract.
        # bound the class body at the next top-level statement, so the last
        # tester does not swallow the module's argparse definitions
        nm = re.search(r"^[A-Za-z_@#]", text[m.end():], re.M)
        seg = text[m.end(): m.end() + nm.start()] if nm else text[m.end():]
        flags: list[str] = []
        for f in re.findall(r'"(--[A-Za-z0-9][^"]*)"', seg):
            if f not in flags:
                flags.append(f)
        testers[name] = Tester(name=name, flags=flags, line=line)
    dm = re.search(r"g_default_testers\s*=\s*\[(.*?)\]", text, re.S)
    defaults = re.findall(r'"([a-z-]+)"', dm.group(1)) if dm else []
    expect(len(testers), 5, "testers in run_regression.py",
           "`super().__init__(\"<name>\")` in the Tester subclasses")
    return testers, defaults


def scan(root: str) -> CiModel:
    wf = os.path.join(root, ".github", "workflows")
    rr = os.path.join(root, "test", "regress", "cli", "run_regression.py")
    if not os.path.isdir(wf):
        raise SystemExit(f"no .github/workflows in {root!r}")
    m = CiModel()
    for fn in sorted(os.listdir(wf)):
        if fn.endswith((".yml", ".yaml")):
            m.jobs.extend(_parse_workflow(os.path.join(wf, fn), fn))
    if os.path.exists(rr):
        m.testers, m.default_testers = _parse_testers(rr)
    return m
