"""Command-line status report for the regression exclusion audit."""
from __future__ import annotations

import argparse
import json
import sys

from regression_audit.audit import CLI, TESTERS, scan
from scripts.targets import checkout, git

SCOPE = ("Source exclusions only: DISABLE-TESTER directives and the CMake disabled list. "
         "Tester selection, applies(), REQUIRES, and CI/build conditions are not evaluated.")


def render(report: dict, selected: list[str], summary: bool = False) -> str:
    lines = ["cvc5 regression audit", f"Checkout: {report['checkout']}",
             f"Revision: {report['revision'] or '(not a git checkout)'}; "
             f"dirty: {report['dirty']}",
             f"Scanned {report['files_scanned']} regression files under {CLI}", "",
             f"{'tester':<12} {'direct':>7} {'inherited*':>11} {'suite':>7} {'total*':>7}  status"]
    for tester in selected:
        data = report["testers"][tester]
        values = [str(data[k]) if data[k] is not None else "-"
                  for k in ("direct", "inherited_only", "suite_disabled", "total_disabled")]
        status = data["status"]
        if status == "registered":
            status += "; " + ("default tester" if data["default"] else "opt-in tester")
        lines.append(f"{tester:<12} {values[0]:>7} {values[1]:>11} {values[2]:>7} {values[3]:>7}  {status}")
    lines += ["* inherited excludes direct disables; total counts each file once, including suite exclusions.",
              "", SCOPE,
              "Reason comments are source explanations selected heuristically; other nearby prose is context.",
              "Missing reasons are left unknown. No solver/checker is run."]
    if summary:
        return "\n".join(lines)
    count = 0
    for row in report["regressions"]:
        directives = [d for d in row["directives"] if set(d["affects"]) & set(selected)]
        suite = row["suite_disabled"] if any(
            report["testers"][t]["status"] == "registered" for t in selected
        ) else None
        if not directives and not suite:
            continue
        count += 1
        lines += ["", row["path"]]
        if suite:
            lines.append(f"  all testers: suite disabled ({suite['location']})")
            if suite["reason_comments"]:
                for reason in suite["reason_comments"]:
                    lines.append(f"    Reason comment: {reason['text']} ({reason['location']})")
            else:
                lines.append("    Reason: unknown; no adjacent CMake comment")
        for directive in directives:
            effects = [t if t == directive["tester"] else f"{t} via {directive['tester']}"
                       for t in directive["affects"] if t in selected]
            lines.append(f"  {', '.join(effects)}: disabled ({directive['location']})")
            if directive["reason_comments"]:
                for reason in directive["reason_comments"]:
                    lines.append(f"    Reason comment: {reason['text']} ({reason['location']})")
            else:
                lines.append("    Reason: unknown; no explanation identified in adjacent comments")
            for context in directive["context"]:
                lines.append(f"    Context: {context['text']} ({context['location']})")
            for tester, location in directive["inherited_at"].items():
                if tester in selected:
                    lines.append(f"    {tester} inherits this disable at {location}")
        for command in row["command_lines"]:
            lines.append(f"  COMMAND-LINE: {command}")
    if not count:
        message = "No source exclusions found for the selected testers."
        if not any(report["testers"][t]["status"] == "registered" for t in selected):
            message = "Selected testers are not registered; no coverage is available to audit."
        lines += ["", message]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="eo_cvc5_regressions_audit",
        description="Show which cvc5 regressions disable proof, cpc, or cpc-logos, and why.")
    parser.add_argument("--cvc5", help="source checkout; defaults to the shared Dokimasia checkout resolver")
    parser.add_argument("--tester", choices=TESTERS, action="append", help="limit the report; repeat to select several")
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--summary", action="store_true", help="print counts and tester availability only")
    output.add_argument("--json", action="store_true", help="print status and source evidence as JSON")
    args = parser.parse_args(argv)
    try:
        root, via = checkout(args.cvc5)
        report = scan(root)
        report.update({"resolved_via": via, "revision": git(root, "rev-parse", "HEAD") or None,
                       "dirty": bool(git(root, "status", "--porcelain")), "scope": SCOPE})
        selected = [t for t in TESTERS if not args.tester or t in args.tester]
        if args.json:
            report["testers"] = {t: report["testers"][t] for t in selected}
            for row in report["regressions"]:
                row["directives"] = [d for d in row["directives"] if set(d["affects"]) & set(selected)]
            report["regressions"] = [r for r in report["regressions"] if r["directives"] or r["suite_disabled"]]
            if not any(t["status"] == "registered" for t in report["testers"].values()):
                report["regressions"] = []
            print(json.dumps(report, indent=2))
        else:
            print(render(report, selected, args.summary))
        return 0
    except (OSError, ValueError, SyntaxError) as exc:
        print(f"eo_cvc5_regressions_audit: {exc}", file=sys.stderr)
        return 2
