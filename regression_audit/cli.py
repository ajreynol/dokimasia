"""Command-line status report for the regression exclusion audit."""
from __future__ import annotations

import argparse
import json
import sys
from textwrap import shorten

from regression_audit.audit import CLI, TESTERS, TIMEOUT_WORD, scan
from scripts.targets import checkout, git

SCOPE = ("DISABLE-TESTER directives only. Suite-wide exclusions are out of scope; "
         "tester selection, applies(), REQUIRES, and CI/build conditions are not evaluated.")


def compact_rows(report: dict, selected: list[str]) -> list[dict]:
    """One row per excluded file, using only evidence for the selected testers."""
    registered = {t for t in selected if report["testers"][t]["status"] == "registered"}
    rows = []
    for row in report["regressions"]:
        directives = [d for d in row["directives"] if set(d["affects"]) & registered]
        affected = set()
        for directive in directives:
            affected.update(set(directive["affects"]) & registered)
        if not affected:
            continue
        # "yes" is a property of the file's literal metadata, never a derived
        # effect of another tester's directive.
        direct = {d["tester"] for d in directives}
        cells = {}
        for tester in selected:
            if tester in direct:
                cells[tester] = "yes"
            elif tester not in registered or tester in affected:
                cells[tester] = "--"
            else:
                cells[tester] = "no"
        notes = []
        for source in directives:
            text = " ".join(c["text"] for c in source["reason_comments"])
            category = "timeout" if TIMEOUT_WORD.search(text) else ("other" if text else "unknown")
            note = "timeout" if category == "timeout" else (text or "unknown")
            if note not in notes:
                notes.append(note)
        direct_reasons = {}
        for tester in direct & set(selected):
            text = " ".join(c["text"] for d in directives if d["tester"] == tester
                            for c in d["reason_comments"])
            direct_reasons[tester] = "timeout" if TIMEOUT_WORD.search(text) else ("other" if text else "unknown")
        rows.append({"path": row["path"].removeprefix(f"{CLI}/"),
                     "cells": cells,
                     "direct_reasons": direct_reasons,
                     "note": "; ".join(notes)})
    return rows


def totals(rows: list[dict]) -> dict:
    return {"yes_entries": sum(len(r["direct_reasons"]) for r in rows),
            "regressions_with_directives": sum(bool(r["direct_reasons"]) for r in rows),
            "reasons": {reason: sum(reason == category for r in rows for category in r["direct_reasons"].values())
                        for reason in ("timeout", "other", "unknown")}}


def total_lines(report: dict, selected: list[str], counts: dict) -> list[str]:
    by_tester = []
    for tester in selected:
        data = report["testers"][tester]
        status = "" if data["status"] == "registered" else (
            " (planned)" if data["status"].startswith("planned") else " (not registered)")
        by_tester.append(f"{tester} {data['direct']}{status}")
    return ["Yes totals: " + " / ".join(by_tester)
            + f"; sum {counts['yes_entries']} ({counts['regressions_with_directives']} regressions)",
            "Reasons (yes only): " + " / ".join(f"{reason} {count}" for reason, count in counts["reasons"].items())]


def render(report: dict, selected: list[str], summary: bool = False, verbose: bool = False) -> str:
    rows = compact_rows(report, selected)
    counts = totals(rows)
    if verbose:
        return render_verbose(report, selected) + "\n\n" + "\n".join(total_lines(report, selected, counts))
    revision = (report["revision"] or "unversioned")[:10]
    dirty = " (dirty)" if report["dirty"] else ""
    lines = [f"cvc5 {revision}{dirty} | {report['files_scanned']} regressions scanned", ""]
    if not summary and rows:
        path_width = max(len("Regression"), *(len(r["path"]) for r in rows))
        widths = {t: max(len(t), *(len(r["cells"][t]) for r in rows)) for t in selected}
        header = "  ".join(f"{t:<{widths[t]}}" for t in selected)
        lines.append(f"{'Regression':<{path_width}}  {header}  Note")
        for row in rows:
            cells = "  ".join(f"{row['cells'][t]:<{widths[t]}}" for t in selected)
            note = shorten(row["note"], width=72, placeholder="...")
            lines.append(f"{row['path']:<{path_width}}  {cells}  {note}")
        lines.append("")
    lines += total_lines(report, selected, counts)
    if not summary and rows:
        lines.append("yes=literal DISABLE-TESTER directive; no=no directive; --=implied or unavailable")
    lines.append("Totals count yes cells only. Details: --verbose")
    return "\n".join(lines)


def render_verbose(report: dict, selected: list[str]) -> str:
    lines = ["cvc5 regression audit", f"Checkout: {report['checkout']}",
             f"Revision: {report['revision'] or '(not a git checkout)'}; "
             f"dirty: {report['dirty']}",
             f"Scanned {report['files_scanned']} regression files under {CLI}", "",
             f"{'tester':<12} {'direct':>7} {'inherited*':>11} {'affected*':>9}  status"]
    for tester in selected:
        data = report["testers"][tester]
        values = [str(data[k]) if data[k] is not None else "-"
                  for k in ("direct", "inherited_only", "total_disabled")]
        status = data["status"]
        if status == "registered":
            status += "; " + ("default tester" if data["default"] else "opt-in tester")
        lines.append(f"{tester:<12} {values[0]:>7} {values[1]:>11} {values[2]:>9}  {status}")
    lines += ["* inherited excludes direct disables; affected counts direct and inherited disables once per file.",
              "", SCOPE,
              "Reason comments are source explanations selected heuristically; other nearby prose is context.",
              "Missing reasons are left unknown. No solver/checker is run."]
    count = 0
    for row in report["regressions"]:
        directives = [d for d in row["directives"] if set(d["affects"]) & set(selected)]
        if not directives:
            continue
        count += 1
        lines += ["", row["path"]]
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
    output.add_argument("--verbose", "-v", action="store_true", help="include full reasons, source locations, inheritance, and command lines")
    output.add_argument("--json", action="store_true", help="print status and source evidence as JSON")
    args = parser.parse_args(argv)
    try:
        root, via = checkout(args.cvc5)
        report = scan(root)
        report.update({"resolved_via": via, "revision": git(root, "rev-parse", "HEAD") or None,
                       "dirty": bool(git(root, "status", "--porcelain")), "scope": SCOPE})
        selected = [t for t in TESTERS if not args.tester or t in args.tester]
        report["totals"] = totals(compact_rows(report, selected))
        if args.json:
            report["testers"] = {t: report["testers"][t] for t in selected}
            for row in report["regressions"]:
                row["directives"] = [d for d in row["directives"] if set(d["affects"]) & set(selected)]
            report["regressions"] = [r for r in report["regressions"] if r["directives"]]
            if not any(t["status"] == "registered" for t in report["testers"].values()):
                report["regressions"] = []
            print(json.dumps(report, indent=2))
        else:
            print(render(report, selected, args.summary, args.verbose))
        return 0
    except (OSError, ValueError, SyntaxError) as exc:
        print(f"eo_cvc5_regressions_audit: {exc}", file=sys.stderr)
        return 2
