"""The safe-build invariant, and its verifier.

    A safe build differs from an unrestricted build only in
      (a) the default value of the `safeMode` option,
      (b) the text of diagnostics, and
      (c) what the build reports about itself.
    Nothing gates solver behaviour on the build macro.

While that holds, `--safe-mode=safe` on an unrestricted binary *is* a safe
build for every purpose except the text of its error messages, and a separate
build exists only to change a default. The moment it stops holding, some
behaviour is reachable in one and not the other, and no runtime flag can stand
in for the build.

The classifier is deliberately closed: a conditional is benign only on positive
evidence, and anything unrecognised is reported. A new `#ifdef CVC5_SAFE_MODE`
should have to argue for itself.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

from .. import source

MACROS = ("CVC5_SAFE_MODE", "CVC5_STABLE_MODE")

_COND = re.compile(r"^[ \t]*#[ \t]*(if|ifdef|ifndef|elif)\b[^\n]*", re.M)

#: What a guarded block may do and still leave the invariant standing.
OPTION_DEFAULT = "option-default"   # sets the safeMode option's initial value
DIAGNOSTIC = "diagnostic"           # builds an error/help string, nothing else
CONFIG_REPORT = "config-report"     # defines what the build reports about itself
UNCLASSIFIED = "UNCLASSIFIED"       # anything else -- the check fires

REVIEWED = "diagnostic-reviewed"    # a human read it; the hash pins what they read

BENIGN = (OPTION_DEFAULT, DIAGNOSTIC, CONFIG_REPORT, REVIEWED)

#: Blocks a person has read and judged diagnostic-only, where the classifier is
#: too strict to say so itself -- typically because the block computes *which*
#: hint to print. Keyed by site, valued by (sha1 of the block, why). The hash is
#: the point: edit the block and it needs reading again.
#:
#: Keep this list short. It is the seam where the check stops being mechanical,
#: and every entry is a small debt.
REVIEWED_BLOCKS = {
    "smt/illegal_checker.cpp": (
        "dc19d72ac1e5aef8",
        "appends a 'Try --arrays-exp.'-style hint to the exception text; the "
        "kindToTheoryId call only selects which hint, and nothing escapes the "
        "stringstream",
    ),
}


def _hash(body: str) -> str:
    """A short, whitespace-insensitive digest of a guarded block."""
    import hashlib
    norm = " ".join(body.split())
    return hashlib.sha1(norm.encode("utf-8")).hexdigest()[:16]

#: A statement that only contributes to a message. Anything outside this set in
#: a guarded block makes the block unclassified.
_DIAG_LINE = re.compile(
    r"""^\s*(?:
          //.*                                   # a comment
        | \#\s*(?:if|ifdef|ifndef|elif|else|endif)\b.*
        | (?:ss|out|o|os)\s*<<.*                 # streaming into a message
        | case\s+\w[\w:]*\s*:.*                  # a switch arm doing the above
        | default\s*:.*
        | break\s*;
        | switch\s*\(.*
        | if\s*\(.*                              # a branch whose body is text
        | else\b.*
        | \}|\{|\)\s*;?
        | :\s*LogicException\(.*                 # the ctor-init form
        )\s*$""",
    re.X)

_OPT_DEFAULT = re.compile(r"safeMode\s*=\s*options::SafeMode::(SAFE|STABLE)")
_CONFIG_DEF = re.compile(r"#\s*define\s+IS_(SAFE|STABLE)_BUILD\b")


@dataclass
class Conditional:
    path: str
    line: int
    directive: str
    kind: str
    body: str = ""

    @property
    def where(self) -> str:
        return f"{self.path}:{self.line}"


@dataclass
class Report:
    conditionals: list[Conditional] = field(default_factory=list)
    #: files the build excludes when ENABLE_SAFE_MODE is on -- must be empty
    excluded_sources: list[str] = field(default_factory=list)
    #: call sites of Configuration::isSafeBuild() outside reporting
    behavioural_readers: list[str] = field(default_factory=list)
    #: optional libraries a safe build refuses to link
    disabled_libraries: list[str] = field(default_factory=list)

    def unclassified(self) -> list[Conditional]:
        return [c for c in self.conditionals if c.kind == UNCLASSIFIED]

    def by_kind(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for c in self.conditionals:
            out[c.kind] = out.get(c.kind, 0) + 1
        return out

    def holds(self) -> bool:
        return not (self.unclassified() or self.excluded_sources
                    or self.behavioural_readers)


def _block(text: str, start: int) -> tuple[str, int]:
    """The text guarded by the directive beginning at `start`, and its depth."""
    depth = 0
    out: list[str] = []
    for line in text[start:].splitlines():
        s = line.strip()
        if re.match(r"#\s*(if|ifdef|ifndef)\b", s):
            depth += 1
        elif re.match(r"#\s*endif\b", s):
            depth -= 1
            if depth <= 0:
                break
        out.append(line)
    return "\n".join(out), depth


def _classify(directive: str, body: str) -> str:
    if _CONFIG_DEF.search(body) or _CONFIG_DEF.search(directive):
        return CONFIG_REPORT
    if _OPT_DEFAULT.search(body):
        # Only benign if that assignment is *all* it does.
        rest = _OPT_DEFAULT.sub("", body)
        if not re.search(r"[A-Za-z_]\w*\s*\(", rest.replace("options::", "")):
            return OPTION_DEFAULT
        return UNCLASSIFIED
    lines = [ln for ln in body.splitlines() if ln.strip()]
    if lines and all(_DIAG_LINE.match(ln) for ln in lines[1:]):
        return DIAGNOSTIC
    return UNCLASSIFIED


def scan(root: str) -> Report:
    src = os.path.join(root, "src") if os.path.isdir(os.path.join(root, "src")) else root
    rep = Report()

    for path in source.walk(src, (".cpp", ".h", ".cpp.in", ".h.in")):
        text = source.read(path)
        if not any(m in text for m in MACROS):
            continue
        rel = os.path.relpath(path, src)
        for m in _COND.finditer(text):
            directive = m.group(0)
            if not any(mac in directive for mac in MACROS):
                continue
            body, _ = _block(text, m.start())
            kind = _classify(directive, body)
            if kind == UNCLASSIFIED and rel in REVIEWED_BLOCKS:
                want, _why = REVIEWED_BLOCKS[rel]
                if _hash(body) == want:
                    kind = REVIEWED
            rep.conditionals.append(Conditional(
                rel, text[:m.start()].count("\n") + 1, directive.strip(),
                kind, body))

    # A safe build must not compile a different set of files.
    for cm in ("CMakeLists.txt", os.path.join("src", "CMakeLists.txt")):
        p = os.path.join(root, cm)
        if not os.path.exists(p):
            continue
        for mm in re.finditer(r"ENABLE_SAFE_MODE", source.read(p)):
            seg = source.read(p)[mm.start():mm.start() + 600]
            for f in re.findall(r"\b([\w/]+\.(?:cpp|h))\b", seg):
                rep.excluded_sources.append(f"{cm}: {f}")
            for lib in re.findall(r"set\((USE_\w+)\s+OFF\)", seg):
                if lib not in rep.disabled_libraries:
                    rep.disabled_libraries.append(lib)

    # isSafeBuild() may be reported, never branched on.
    for path in source.walk(src, (".cpp", ".h")):
        text = source.read(path)
        if "isSafeBuild" not in text:
            continue
        rel = os.path.relpath(path, src)
        for ln, line in enumerate(text.splitlines(), 1):
            if "isSafeBuild" not in line:
                continue
            if re.search(r"\b(if|while|\?|&&|\|\|)\b.*isSafeBuild", line):
                rep.behavioural_readers.append(f"{rel}:{ln}: {line.strip()}")
    return rep
