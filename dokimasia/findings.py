"""Structured observations from the existing scanners; no database maintenance.

An observation describes what a scanner saw, not a verdict about cvc5. Moving
evidence belongs to a run, while the identity and claim go to Koine.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import PurePosixPath

from . import source

# Code -> (analysis, claim). These are also the agent's allowed questions.
CHECKS = {
    "RULE0001": ("ledger", "Produced rule has no registered checker"),
    "RULE0002": ("ledger", "Produced rule has a trusted checker registration"),
    "ELAB0001": ("ledger", "Produced macro has no detected postprocessor expansion"),
    "SEAM0001": ("ledger", "Produced rule is refused by the Eunoia seam"),
    "CI0001": ("ci", "Proof-promising build job runs no proof tester"),
    "CI0002": ("ci", "Proof completeness chain has an unsatisfied link"),
    "CI0003": ("ci", "Proof tester requests lazy proof checking"),
    "CI0004": ("ci", "Proof-testing job excludes regression levels"),
    "BUILD0001": ("buildmode", "Safe-build invariant needs review"),
    "MODE0001": ("modes", "Proof-unsupported option defaults on without a direct safe-mode override"),
    "RW0001": ("rewrites", "Implemented rewrite is refused by the Eunoia seam"),
    "RW0002": ("rewrites", "Implemented rewrite is printable only in unrestricted mode"),
    "TRUST0001": ("trust", "File constructs trust steps with no reason id"),
    "INFER0002": ("infer", "Emitted inference has no case in a reconstructor with a trust fallback"),
    "INFERID0001": ("inferid", "Inference id has multiple detected production sites"),
    "INFERID0002": ("inferid", "File produces an inference with a sentinel id"),
    "SIG0001": ("signature", "Printable rule has no signature declaration"),
    "SIG0002": ("signature", "Constructed skolem is refused by the Eunoia seam"),
    "SIG0003": ("signature", "Documented rule arity disagrees with detected checker arity"),
}
ANALYSES = ("ledger", "ci", "buildmode", "modes", "rewrites", "trust",
            "infer", "inferid", "signature", "gates", "fragment", "tcb", "latent")


def finding_id(code: str, entity: str, owner: str = "cvc5") -> str:
    if not isinstance(code, str) or code not in CHECKS:
        raise ValueError(f"unknown check code: {code}")
    if not isinstance(entity, str) or not entity or entity != entity.strip() or "\\" in entity or "\n" in entity:
        raise ValueError("entity must be nonempty, normalized text")
    if PurePosixPath(entity).is_absolute() or ".." in PurePosixPath(entity).parts:
        raise ValueError("entity must not contain an absolute or parent path")
    body = json.dumps([owner, code, entity], ensure_ascii=False, separators=(",", ":"))
    return "dokimasia:" + hashlib.sha256(body.encode()).hexdigest()[:24]


def observation(code: str, entity: str) -> dict:
    """The stable part of a finding, shared with the independent producer."""
    return {"id": finding_id(code, entity), "bug": f"{code}-{entity}",
            "tool": "dokimasia", "owner": "cvc5", "code": code,
            "entity": entity, "description": f"{CHECKS[code][1]}: {entity}",
            "kind": "static-observation"}


class Findings:
    def __init__(self):
        self.bugs: dict[str, dict] = {}
        self.evidence: dict[str, list[dict]] = {}
        self.measurements: dict[str, dict] = {}

    def add(self, code, entity, **evidence):
        bug = observation(code, entity)
        self.bugs[bug["id"]] = bug
        rows = self.evidence.setdefault(bug["id"], [])
        if evidence not in rows:
            rows.append(evidence)

    def dump(self):
        return sorted(self.bugs.values(), key=lambda b: (b["code"], b["entity"]))


def collect(root: str, analyses=ANALYSES) -> Findings:
    """A complete selected run or an exception. Partial runs are never appended."""
    unknown = set(analyses) - set(ANALYSES)
    if unknown:
        raise ValueError(f"unknown analyses: {sorted(unknown)}")
    source.clear()
    out = Findings()
    for name in analyses:
        globals()["collect_" + name](root, out)
    for rows in out.evidence.values():
        rows.sort(key=lambda r: json.dumps(r, sort_keys=True))
    return out


def collect_ledger(root, out):
    from .ledger.build import build
    from .sanity import expect
    r = build(root)
    expect(len(r.rules), 100, "declared proof rules", "include/cvc5/cvc5_proof_rule.h")
    expect(sum(x.printed != "never" for x in r.rows()), 100, "handled proof rules",
           "EoPrinter::isHandled in src/proof/eo/eo_printer.cpp")
    out.measurements["ledger"] = {"declared": len(r.rules),
        "unproduced": sorted(x.name for x in r.rows() if not x.produced),
        "refusals": {k: sorted(x.name for x in v) for k, v in r.unprintable().items()}}
    for row in r.producible():
        for code in row.holes:
            if code in CHECKS:
                out.add(code, row.name, locations=sorted("src/" + s for s in row.produced),
                        checker="src/" + row.checker if row.checker else None,
                        pedantic=row.pedantic, printed=row.printed,
                        limitation="Production is syntactic; safe-mode reachability and a failing input are not established.")


def collect_ci(root, out):
    from .ci.scan import scan
    r = scan(root)
    chain = r.completeness_chain()
    out.measurements["ci"] = {"jobs": len(r.jobs), "completeness_chain": chain}
    for j in r.modes_promising_proofs():
        if not j.proof_testers:
            out.add("CI0001", f"{j.workflow}#{j.name}", location=".github/workflows/" + j.workflow,
                    mode=j.mode, config=j.config)
    for entity, (claim, holds, detail) in zip(
            ("safe-job", "safe-job-proof-tester", "check-proofs", "no-granularity", "explicit-completeness"), chain):
        if not holds:
            out.add("CI0002", entity, claim=claim, detail=detail,
                    location="test/regress/cli/run_regression.py",
                    limitation="An implicit guarantee may hold; explicit-completeness is an instrumentation observation.")
    tester = r.testers.get("proof")
    if tester and "--proof-check=lazy" in tester.flags:
        out.add("CI0003", "proof", location=f"test/regress/cli/run_regression.py:{tester.line}",
                flags=tester.flags, limitation="Lazy checking is a configuration fact, not a demonstrated incomplete proof.")
    for j in r.jobs_with_proofs():
        if j.exclude_regress:
            out.add("CI0004", f"{j.workflow}#{j.name}", location=".github/workflows/" + j.workflow,
                    excluded=j.exclude_regress, limitation="Exclusion may be intentional.")


def collect_buildmode(root, out):
    from .buildmode.buildmode import scan
    r = scan(root)
    out.measurements["buildmode"] = {"holds": r.holds(), "conditionals": r.by_kind(),
                                     "disabled_libraries": sorted(r.disabled_libraries)}
    for c in r.unclassified():
        out.add("BUILD0001", "src/" + c.path + "#conditional", location="src/" + c.where,
                directive=c.directive, body=c.body,
                limitation="The classifier could not establish that this block is benign.")
    for s in r.behavioural_readers:
        path = s.split(":", 1)[0]
        out.add("BUILD0001", "src/" + path + "#reader", location="src/" + s)
    for s in r.excluded_sources:
        out.add("BUILD0001", s, location=s,
                limitation="Source exclusion is inferred from nearby CMake text; review the condition.")


def collect_modes(root, out):
    from .modes.delta import ModeDelta, unsupported_but_enabled
    r = ModeDelta.load(root + "/src")
    out.measurements["modes"] = {m: len(r.for_mode(m)) for m in ("safe", "stable")}
    for row in unsupported_but_enabled(root + "/src", r):
        out.add("MODE0001", row["option"], location="src/options/" + row["file"], option=row,
                limitation="Defaults-only analysis misses coupled option guards, including the historical macrosQuantMode false positive (s-4).")


def collect_rewrites(root, out):
    from .rewrites.scan import scan
    from .gates.gates import scan as gates
    r, g = scan(root), gates(root)
    out.measurements["rewrites"] = {"declared": len(r.declared), "rare": len(r.rare),
                                   "correspondence": r.correspondence()}
    for code, names in (("RW0001", r.gaps()), ("RW0002", r.safe_mode_gaps())):
        for name in names:
            verdict, why = g.verdict(name)
            out.add(code, name, location="src/" + r.implemented[name],
                    safe_mode_gate={"verdict": verdict, "reason": why}, macro=name.startswith("MACRO_"),
                    limitation="Gates are partial syntactic evidence; macro reconstruction may succeed. No failing input is established.")


def collect_trust(root, out):
    from .trust.census import census
    r = census(root)
    out.measurements["trust"] = {"live": sorted(r.live()), "dead": sorted(r.dead()),
                                "passes": r.pass_correspondence()}
    for s in r.anonymous():
        out.add("TRUST0001", "src/" + s.path, location="src/" + s.where(),
                limitation="An unnamed trust step is an attribution gap, not proof of safe-mode reachability.")


def collect_infer(root, out):
    from .infer.coverage import scan
    r = scan(root)
    out.measurements["infer"] = {"without_reconstructor": sorted(t.theory for t in r.without_reconstructor()),
        "unhandled": {t.theory: t.unhandled for t in r.with_reconstructor()}}
    for t in r.with_reconstructor():
        if t.trust_fallback:
            for name in t.unhandled:
                out.add("INFER0002", t.theory + ":" + name, location="src/" + t.ipc_file,
                        limitation="Switch coverage only; reachability and call-site ProofGenerators need separate verification.")


def collect_inferid(root, out):
    from .inferid.scan import scan
    r = scan(root + "/src")
    out.measurements["inferid"] = {"declared": len(r.declared), "unused": sorted(r.unused())}
    for name, sites in r.violations():
        out.add("INFERID0001", name, locations=sorted("src/" + s.where() for s in sites),
                limitation="A hygiene observation: multiple sites are not necessarily a defect.")
    for name, sites in r.sentinel_uses().items():
        for s in sites:
            out.add("INFERID0002", "src/" + s.path + "#" + name, location="src/" + s.where())


def collect_signature(root, out):
    from .signature.compare import scan
    from .signature.checker import scan_checkers, agrees
    r, checkers = scan(root), scan_checkers(root)
    out.measurements["signature"] = {"printable": len(r.printable), "declarations": len(r.sig),
                                     "checkers_with_arity": len(checkers)}
    for name in r.missing():
        out.add("SIG0001", name, location="src/proof/eo/eo_printer.cpp",
                limitation="Check printer renaming and generated signature handling before reporting.")
    for name in r.skolems.unprintable():
        out.add("SIG0002", name, location="src/proof/eo/eo_node_converter.cpp",
                limitation="Safe-mode gates and a reproducer are required; construction alone does not establish reachability.")
    for name, (premises, args) in r.doc.items():
        c = checkers.get(name)
        if c and (agrees(premises, c.premises) is False or agrees(args, c.arguments) is False):
            out.add("SIG0003", name, location="src/" + c.file, evidence=c.evidence,
                    documented=[premises, args], checked=[c.premises, c.arguments],
                    limitation="Both the LaTeX and checker arity parsers are partial.")


def collect_gates(root, out):
    from .gates.gates import scan
    r = scan(root)
    out.measurements["gates"] = {"kinds": {k: sorted(v) for k, v in sorted(r.kind_gate.items())},
        "rewrites": {k: r.verdict(k) for k in sorted(r.rule_kinds)}}


def collect_fragment(root, out):
    from .fragment.fragment import scan
    r = scan(root)
    out.measurements["fragment"] = {"theories": {t: dict(zip(("available", "blocked"), r.safe_fragment(t)))
        for t in sorted(r.by_theory())}, "nonkind_options": r.uncovered_expert_options()}


def collect_tcb(root, out):
    from .tcb.closure import IncludeGraph, Closure, SEED_SETS, _expand
    src = root + "/src"
    g = IncludeGraph.build(src)
    seeds = _expand(src, SEED_SETS["proof-checker"])
    if not seeds:
        raise ValueError("TCB checker seeds matched no files")
    c = Closure.compute(g, seeds, mode="headers")
    out.measurements["tcb"] = {"files": len(c.files), "lines": c.loc,
                              "limitation": "Compile-time include closure, not runtime call coverage."}


def collect_latent(root, out):
    from .latent.latent import scan, provenance
    r = scan(root)
    recorded = {k: v for k, v in provenance().items() if k != "corpus"}
    recorded.update(corpus=r.corpus, source_record="reach-corpus.json")
    out.measurements["latent"] = {"counts": dict(Counter(h.state for h in r.holes)),
        "census_provenance": recorded, "have_census": r.have_census,
        "limitation": "Historical runtime census, potentially a different revision/build; not fresh evidence of reachability."}
