"""Compare a rule's Eunoia declaration against cvc5's documented inference.

Two sources:

``proofs/eo/**/*.eo``            `(declare-rule name (params) :premises (...)
                                 :args (...) :conclusion ...)`
``include/cvc5/cvc5_proof_rule.h``  the doc comment's
                                 `\\inferrule{premises \\mid args}{conclusion}`

and one mapping, lifted from `EoPrinter::getRuleName`, which decides what a
`ProofRule` is called when it reaches the signature.

What a mismatch means
---------------------
`ethos` checks a proof against the signature. If the signature expects two
premises where cvc5 documents one, the two disagree about the calculus, and at
most one of them describes what the checker enforces. We report the
disagreement; which side is wrong is a question for whoever owns the rule.

Arity is compared *by shape*, not by number: `variadic` (`F_1 \\dots F_n` in the
docs, `:premise-list` in the signature), `none`, or a fixed count. Comparing
counts across a variadic boundary would produce noise, not findings.
"""

from __future__ import annotations

import glob
import os
import re
from dataclasses import dataclass, field

_DECL = re.compile(r"\(declare-rule\s+([^\s()]+)\s*\((.*?)\)\s*(.*?)(?=\n\(|\Z)", re.S)
_EVALUE_DOC = re.compile(
    r"/\*\*(.*?)\*/\s*\n\s*EVALUE\(([A-Z][A-Z0-9_]*)\)", re.S)
_INFER = re.compile(r"\\inferrule\{(.*?)\}\{(.*?)\}", re.S)

#: Rules whose printed name is not `tolower(name)`, from EoPrinter::getRuleName.
SPECIAL_NAME = {
    "ENCODE_EQ_INTRO": "refl",
    "HO_APP_ENCODE": "refl",
    "BV_EAGER_ATOM": "refl",
    "ACI_NORM": "aci_norm",          # or aci_norm_expert, by argument kind
}

#: Handled by the printer without a declared rule of their own.
NO_SIGNATURE_RULE = {"ASSUME"}       # an Eunoia `assume` command, not a rule


def printed_name(rule: str) -> str:
    return SPECIAL_NAME.get(rule, rule.lower())


@dataclass
class Skolems:
    """SkolemIds: declared, documented, constructed, and printable."""
    declared: list[str] = field(default_factory=list)
    doc_indices: dict[str, int] = field(default_factory=dict)
    constructed: set[str] = field(default_factory=set)
    seam_handled: set[str] = field(default_factory=set)

    SENTINELS = frozenset({"NONE", "INTERNAL"})

    def unprintable(self) -> list[str]:
        """Constructed by the solver, refused by the Eunoia seam.

        A skolem the seam cannot print sinks a proof exactly as a rule it
        cannot print does.
        """
        return sorted(self.constructed - self.seam_handled - self.SENTINELS)

    def dead(self) -> list[str]:
        return sorted(set(self.declared) - self.constructed - self.SENTINELS)

    def undocumented(self) -> list[str]:
        return sorted(self.constructed - set(self.doc_indices) - self.SENTINELS)


@dataclass
class Signature:
    #: signature rule -> (premise shape, arg count)
    sig: dict[str, tuple[object, int]] = field(default_factory=dict)
    #: ProofRule -> (premise shape, arg count) from the doc comment
    doc: dict[str, tuple[object, int]] = field(default_factory=dict)
    #: ProofRules the Eunoia seam can print
    printable: set[str] = field(default_factory=set)
    #: the skolem half of the same question
    skolems: Skolems = field(default_factory=lambda: Skolems())

    def missing(self) -> list[str]:
        """Printable rules the signature does not declare -- ethos would reject."""
        return sorted(r for r in self.printable
                      if r not in NO_SIGNATURE_RULE
                      and r not in ("DSL_REWRITE", "THEORY_REWRITE")
                      and printed_name(r) not in self.sig)

    def mismatches(self) -> list[tuple[str, str, tuple, tuple]]:
        """(rule, signature name, doc shape, signature shape) where they disagree."""
        out = []
        for r in sorted(self.printable):
            if r in NO_SIGNATURE_RULE or r in ("DSL_REWRITE", "THEORY_REWRITE"):
                continue
            n = printed_name(r)
            if n not in self.sig or r not in self.doc:
                continue
            d, s = self.doc[r], self.sig[n]
            if d[0] != s[0] or d[1] != s[1]:
                out.append((r, n, d, s))
        return out

    def undocumented(self) -> list[str]:
        """Printable rules with no parseable `\\inferrule` in their doc comment."""
        return sorted(r for r in self.printable if r not in self.doc)


_LATEX_SPACE = re.compile(r"\\[,;:!>]")


def _detex(text: str) -> str:
    """Strip LaTeX spacing commands.

    `\,` is a thin space whose second character is a comma, so splitting a
    premise list on `,` without removing it invents a premise. That bug alone
    accounted for several apparent disagreements.
    """
    return _LATEX_SPACE.sub(" ", text)


def _split_top(text: str, sep: str = ",") -> list[str]:
    """Split on *sep* at paren depth 0."""
    out, depth, cur = [], 0, ""
    for ch in text:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == sep and depth == 0:
            out.append(cur); cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur)
    return [p for p in out if p.strip()]


def _sexprs(text: str) -> int:
    """Count top-level s-expressions: `(= F1 F2) i` is two, not four tokens."""
    n, depth, in_atom = 0, 0, False
    for ch in text:
        if ch == "(":
            if depth == 0:
                n += 1
            depth += 1
            in_atom = False
        elif ch == ")":
            depth -= 1
        elif depth == 0:
            if ch.isspace():
                in_atom = False
            elif not in_atom:
                n += 1
                in_atom = True
    return n


def _premise_shape(text: str):
    r"""`-` is none; a comma-separated list with dots is variadic; otherwise a count.

    `\dots` *inside* one premise -- `(F_1 \land \dots \land F_n)` -- describes
    the shape of a single conjunction, not a list of premises. Treating it as
    variadic was a bug that made 30-odd rules look like they disagreed with the
    signature when they agree.
    """
    t = " ".join(_detex(text).split())
    if t in ("-", ""):
        return 0
    parts = _split_top(t)
    # A premise is variadic only if it *is* a bare list -- `F_1 \dots F_n` with
    # no operator around it. Dots inside a formula describe that formula's
    # shape, not a list of premises.
    def is_bare_list(s: str) -> bool:
        s = s.strip()
        if "\\dots" not in s and "\\ldots" not in s:
            return False
        return bool(re.fullmatch(r"[A-Za-z]\w*_\d+\s*\\l?dots\s*[A-Za-z]\w*_[A-Za-z0-9]+", s))
    # `t_1=t_2, \dots, t_{n-1}=t_n` -- an ellipsis standing alone between listed
    # items -- is a variadic list written out rather than abbreviated.
    if any(p.strip() in ("\\dots", "\\ldots") for p in parts):
        return "variadic"
    if len(parts) == 1:
        return "variadic" if is_bare_list(parts[0]) else 1
    if any(is_bare_list(p) for p in parts):
        return "variadic"
    return len(parts)


def _arg_count(text: str) -> int:
    t = " ".join(_detex(text).split())
    if t in ("-", ""):
        return 0
    parts = _split_top(t)
    if any("\\dots" in p or "\\ldots" in p for p in parts):
        return -1                     # variadic argument list
    return len(parts)


def _field(body: str, key: str) -> str | None:
    """The balanced `( ... )` following *key*, or None."""
    i = body.find(key)
    if i < 0:
        return None
    j = body.find("(", i)
    if j < 0:
        return None
    depth = 0
    for k in range(j, len(body)):
        if body[k] == "(":
            depth += 1
        elif body[k] == ")":
            depth -= 1
            if depth == 0:
                return body[j + 1:k]
    return None


def _parse_signature(root: str) -> dict[str, tuple[object, int]]:
    out: dict[str, tuple[object, int]] = {}
    for path in glob.glob(os.path.join(root, "proofs", "eo", "**", "*.eo"),
                          recursive=True):
        with open(path, encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
        for m in _DECL.finditer(text):
            name, body = m.group(1), m.group(3)
            if ":premise-list" in body:
                prem: object = "variadic"
            else:
                pm = _field(body, ":premises")
                prem = _sexprs(pm) if pm is not None else 0
            am = _field(body, ":args")
            out[name] = (prem, _sexprs(am) if am is not None else 0)
    return out


def _parse_docs(root: str) -> dict[str, tuple[object, int]]:
    path = os.path.join(root, "include", "cvc5", "cvc5_proof_rule.h")
    with open(path, encoding="utf-8", errors="ignore") as fh:
        text = fh.read()
    out: dict[str, tuple[object, int]] = {}
    for m in _EVALUE_DOC.finditer(text):
        comment, name = m.group(1), m.group(2)
        im = _INFER.search(comment)
        if not im:
            continue
        prem_args = im.group(1)
        if "\\mid" not in prem_args:
            continue
        prem, args = prem_args.split("\\mid", 1)
        out[name] = (_premise_shape(prem), _arg_count(args))
    return out


_SK_EVALUE = re.compile(r"/\*\*(.*?)\*/\s*\n\s*EVALUE\((\w+)\)", re.S)
_SK_COUNT = re.compile(r"Number of skolem indices:\s*``(\d+)``")
_SK_MK = re.compile(r"mkSkolemFunction\(\s*SkolemId::(\w+)")
_SK_CASE = re.compile(r"case SkolemId::(\w+)")


def _parse_skolems(root: str) -> Skolems:
    """Skolem ids from the header, the construction sites, and the seam."""
    src = os.path.join(root, "src")
    hdr = os.path.join(root, "include", "cvc5", "cvc5_skolem_id.h")
    with open(hdr, encoding="utf-8", errors="ignore") as fh:
        h = fh.read()
    sk = Skolems(declared=re.findall(r"EVALUE\((\w+)\)", h))
    for m in _SK_EVALUE.finditer(h):
        c = _SK_COUNT.search(m.group(1))
        if c:
            sk.doc_indices[m.group(2)] = int(c.group(1))
    for dirpath, _d, files in os.walk(src):
        for fn in files:
            if not fn.endswith((".cpp", ".h")):
                continue
            with open(os.path.join(dirpath, fn), encoding="utf-8",
                      errors="ignore") as fh:
                text = fh.read()
            if "SkolemId::" in text:
                sk.constructed |= set(_SK_MK.findall(text))
    conv = os.path.join(src, "proof", "eo", "eo_node_converter.cpp")
    if os.path.exists(conv):
        with open(conv, encoding="utf-8", errors="ignore") as fh:
            body = re.search(r"bool EoNodeConverter::isHandledSkolemId.*?\n\}",
                             fh.read(), re.S)
        if body:
            sk.seam_handled = set(_SK_CASE.findall(body.group(0)))
    return sk


def scan(root: str) -> Signature:
    if not os.path.isdir(os.path.join(root, "proofs", "eo")):
        raise SystemExit(f"no proofs/eo signature under {root!r}")
    from ..ledger.build import build
    led = build(root)
    return Signature(
        sig=_parse_signature(root),
        doc=_parse_docs(root),
        printable={r.name for r in led.rows() if r.printed != "never"},
        skolems=_parse_skolems(root),
    )
