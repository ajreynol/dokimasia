#!/usr/bin/env python3
"""Probe a rewrite with cvc5 and an independent solver.

Each probe is an .smt2 file built so that a single rewrite rule decides it,
typically ``(assert (not (= LHS RHS)))`` or ``(assert LHS)`` with a model
fixed by equalities. For each file this reports:

  * the cvc5 and z3 answers, and whether they disagree (a disagreement on a
    probe is direct evidence of an unsound rewrite in one of them);
  * on an unsat answer, the trust steps left in a cvc5 proof printed at
    ``--proof-granularity=dsl-rewrite``. A step reconstructed by RARE rules
    leaves none; a rewrite the proof rules do not capture leaves a ``trust``
    step whose identifier (e.g. ``MACRO_THEORY_REWRITE_RCONS_SIMPLE``,
    ``REWRITE_NO_ELABORATE``) says which part of the pipeline gave up.

A probe may declare its expectation with a line ``; EXPECT: sat|unsat``, and
cvc5-only options with ``; CVC5-OPTS: --opt ...`` (passed to cvc5, never z3).

    python3 rewriter_report/tools/probe.py FILE.smt2 [...] [--json]

The solver binaries come from ``$CVC5_BIN`` and ``$Z3_BIN`` (default: the
first ``cvc5``/``z3`` on PATH). The cvc5 *binary* revision need not match the
source checkout being analyzed; the report records the version string.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

TIMEOUT = 30
_TRUST = re.compile(r"^; trust (\S+)(?: (\S+))?\s*$", re.M)
_TRUST_STEP = re.compile(r"^\(step (\S+) :rule trust .*?:args \((.*)\)\)\s*$", re.M)
_RULE = re.compile(r":rule ([A-Za-z0-9_.\-]+)")
_EXPECT = re.compile(r"^;\s*EXPECT:\s*(sat|unsat)", re.M)
_OPTS = re.compile(r"^;\s*CVC5-OPTS:(.*)$", re.M)
# Proof-structure rules; everything else in a proof is rewrite evidence.
_STRUCTURAL = frozenset({
    "assume", "trans", "cong", "nary_cong", "ho_cong", "refl", "symm",
    "eq_resolve", "modus_ponens", "and_elim", "and_intro", "not_and",
    "resolution", "chain_resolution", "factoring", "reordering",
    "true_intro", "true_elim", "false_intro", "false_elim", "scope",
    "process_scope", "contra", "split", "implies_elim", "not_not_elim",
    "equiv_elim1", "equiv_elim2", "not_equiv_elim1", "not_equiv_elim2",
    "trust"})


def _bin(env: str, name: str) -> str:
    return os.environ.get(env) or shutil.which(name) or name


def _run(cmd: list[str], timeout: int = TIMEOUT) -> tuple[str, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return "timeout", ""


_DEFINE = re.compile(r"^\(define (@t\d+) \(\) (.*)\)\s*$", re.M)
_REF = re.compile(r"@t\d+")


def _expand(term: str, pf: str) -> str:
    """Inline the printer's ``(define @tN () ...)`` abbreviations."""
    defs = dict(_DEFINE.findall(pf))
    for _ in range(64):
        new = _REF.sub(lambda m: defs.get(m.group(0), m.group(0)), term)
        if new == term or len(new) > 4000:
            return new
        term = new
    return term


def _answer(out: str) -> str:
    # A solver that reports an error may skip the offending assertion and
    # still answer (z3 does this for operators it lacks), so any error makes
    # the answer no evidence. Pass cvc5-only options via ``; CVC5-OPTS:``.
    if "(error" in out:
        return "error"
    for line in out.splitlines():
        line = line.strip()
        if line in ("sat", "unsat", "unknown", "timeout"):
            return line
    return "error"


def versions() -> dict:
    cv, _ = _run([_bin("CVC5_BIN", "cvc5"), "--version"])
    zv, _ = _run([_bin("Z3_BIN", "z3"), "--version"])
    return {"cvc5": cv.splitlines()[0] if cv else "?",
            "z3": zv.splitlines()[0] if zv else "?"}


def _ethos(pf: str, path: str) -> tuple[bool, str]:
    """Check a printed CPC proof with ethos against ``$CPC_SIG/Cpc.eo``.

    The signature defaults to ``deps/cvc5/proofs/eo/cpc``; it should match the
    cvc5 binary's revision, or failures may be version skew, not rewrites.
    """
    sig = os.environ.get("CPC_SIG") or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", "deps", "cvc5",
        "proofs", "eo", "cpc")
    lines = pf.splitlines()
    # Drop the "unsat" line and the outer parentheses of the printed proof.
    body = [ln for ln in lines if ln.strip() not in ("unsat", "(", ")")]
    tmp = path + ".eo.tmp"
    try:
        with open(tmp, "w") as f:
            f.write(f'(include "{os.path.abspath(sig)}/Cpc.eo")\n')
            f.write("\n".join(body) + "\n")
        out, err = _run([_bin("ETHOS_BIN", "ethos"), tmp], timeout=120)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    # The verdict is on stdout; stderr may carry warnings.
    last = (out.strip().splitlines() or err.strip().splitlines()
            or ["no output"])[-1][:300]
    # ethos prints "correct", or "incomplete" when the proof has trust steps.
    return last == "correct", last


def probe(path: str, check: bool = False, ethos: bool = False) -> dict:
    cvc5, z3 = _bin("CVC5_BIN", "cvc5"), _bin("Z3_BIN", "z3")
    text = open(path).read()
    m = _EXPECT.search(text)
    expect = m.group(1) if m else None
    opts = [o for line in _OPTS.findall(text) for o in line.split()]
    c_out, c_err = _run([cvc5, *opts, path])
    z_out, _ = _run([z3, path])
    r = {"file": path, "expect": expect,
         "cvc5": _answer(c_out), "z3": _answer(z_out)}
    if r["cvc5"] == "error":
        r["cvc5_error"] = (c_out + c_err).strip()[:300]
    decided = {r["cvc5"], r["z3"]} <= {"sat", "unsat"}
    r["disagree"] = decided and r["cvc5"] != r["z3"]
    r["unexpected"] = bool(expect) and r["cvc5"] in ("sat", "unsat") \
        and r["cvc5"] != expect
    if r["cvc5"] == "unsat":
        pf, pf_err = _run([cvc5, *opts, "--dump-proofs", "--proof-format=cpc",
                           "--proof-granularity=dsl-rewrite", "--dag-thresh=0",
                           path])
        err = [ln for ln in (pf + "\n" + pf_err).splitlines()
               if ln.startswith("(error") or "Fatal" in ln or "Assertion" in ln]
        if pf == "timeout" or err or "(step" not in pf:
            r["proof_error"] = (err[0] if err else pf_err.strip()
                                or pf.strip() or "no proof")[:300]
        if ethos and "proof_error" not in r:
            ok, msg = _ethos(pf, path)
            r["ethos"] = msg
            r["ethos_ok"] = ok
        if check:
            ck, ck_err = _run([cvc5, *opts, "--check-proofs",
                               "--check-proofs-complete", path])
            r["check_proofs"] = _answer(ck) == "unsat"
            if not r["check_proofs"]:
                r["check_proofs_error"] = (ck + ck_err).strip()[:300]
        r["trust"] = [{"id": i or k, "kind": k} for k, i in _TRUST.findall(pf)]
        r["trust_steps"] = [_expand(a, pf)[:600]
                            for _, a in _TRUST_STEP.findall(pf)]
        rules: dict[str, int] = {}
        for x in _RULE.findall(pf):
            rules[x] = rules.get(x, 0) + 1
        r["rules"] = rules
    return r


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check", action="store_true",
                    help="also run cvc5 --check-proofs --check-proofs-complete "
                         "on unsat probes (fails on any trust step)")
    ap.add_argument("--ethos", action="store_true",
                    help="also check unsat proofs with ethos against $CPC_SIG "
                         "(default deps/cvc5/proofs/eo/cpc)")
    ap.add_argument("--jobs", "-j", type=int, default=1)
    ap.add_argument("--out", help="write the --json report to this file")
    a = ap.parse_args(argv)
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
        res = list(ex.map(lambda f: probe(f, a.check, a.ethos), a.files))
    if a.out:
        with open(a.out, "w") as f:
            json.dump({"versions": versions(), "probes": res}, f, indent=1)
    if a.json:
        print(json.dumps({"versions": versions(), "probes": res}, indent=2))
    else:
        for r in res:
            flags = []
            if r["disagree"]:
                flags.append("DISAGREE")
            if "error" in (r["cvc5"], r["z3"]):
                flags.append("SOLVER-ERROR")
            if r["unexpected"]:
                flags.append("UNEXPECTED")
            if r.get("proof_error"):
                flags.append("PROOF-ERROR")
            if r.get("check_proofs") is False:
                flags.append("CHECK-FAILED")
            if "ethos" in r:
                flags.append("ETHOS-OK" if r["ethos_ok"]
                             else f"ETHOS[{r['ethos']}]")
            tr = ",".join(sorted({t["id"] for t in r.get("trust", [])}))
            dsl = sorted(k for k in r.get("rules", {})
                         if k not in _STRUCTURAL)
            print(f"{r['file']}: cvc5={r['cvc5']} z3={r['z3']}"
                  f"{' ' + ' '.join(flags) if flags else ''}"
                  f"{' trust=' + tr if tr else ''}"
                  f"{' rules=' + ','.join(dsl) if dsl else ''}")
            for s in r.get("trust_steps", []):
                print(f"    trust: {s}")
            if r.get("proof_error"):
                print(f"    proof error: {r['proof_error']}")
    return 1 if any(r["disagree"] or r["unexpected"] for r in res) else 0


if __name__ == "__main__":
    sys.exit(main())
