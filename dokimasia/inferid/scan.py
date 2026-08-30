"""Find every use of every InferenceId, and classify it.

An id can appear in four kinds of place, and only one of them creates the
ambiguity the contract is about:

``definition``
    The enum in ``theory/inference_id.h`` and the ``toString`` switch beside it.
    Every id appears here exactly once by construction; not a use.
``production``
    The id passed as a value -- ``d_im.lemma(lem, InferenceId::FOO)``. **This is
    the kind that must be unique.** Two production sites mean the id no longer
    identifies a program point.
``dispatch``
    A ``case InferenceId::FOO:`` label, switching on an id produced elsewhere.
    Does not create CFG ambiguity: it is a consumer, not a source.
``comparison``
    ``id == InferenceId::FOO``. Also a consumer.

The tool reports the strict count (everything outside the definition) and the
production count separately, so both readings of the contract are visible.
"""

from __future__ import annotations

import os
import re
from collections import defaultdict
from dataclasses import dataclass, field

_ENUM_HEADER = os.path.join("theory", "inference_id.h")
_ENUM_IMPL = os.path.join("theory", "inference_id.cpp")

_USE = re.compile(r"(?:(case)\s+|(==|!=)\s*)?\bInferenceId::([A-Z][A-Z0-9_]*)")
# The final member of the enum carries no trailing comma, so it must be
# optional -- otherwise the last id (UNKNOWN) is silently dropped.
_MEMBER = re.compile(r"^\s*([A-Z][A-Z0-9_]*)\s*(?:=[^,\n]*)?,?\s*(?://.*)?$", re.M)

#: Ids that are sentinels rather than inferences; excluded from the contract.
SENTINELS = frozenset({"NONE", "UNKNOWN", "LAST"})

SOURCE_EXT = (".cpp", ".h", ".cc", ".hpp")


@dataclass(frozen=True)
class Use:
    """One occurrence of an InferenceId."""

    ident: str
    path: str
    line: int
    kind: str          # definition | production | dispatch | comparison

    def where(self) -> str:
        return f"{self.path}:{self.line}"


@dataclass
class InferenceIds:
    """Every declared id, and every use of it."""

    declared: list[str] = field(default_factory=list)
    uses: dict[str, list[Use]] = field(default_factory=lambda: defaultdict(list))

    def production(self, ident: str) -> list[Use]:
        return [u for u in self.uses.get(ident, ()) if u.kind == "production"]

    def outside_definition(self, ident: str) -> list[Use]:
        return [u for u in self.uses.get(ident, ()) if u.kind != "definition"]

    def violations(self, strict: bool = False) -> list[tuple[str, list[Use]]]:
        """Ids used in more than one place, worst first.

        With ``strict``, every use outside the enum definition counts. By
        default only *production* sites count, since a ``case`` label consumes
        an id rather than being a place the id comes from.
        """
        out = []
        for ident in self.declared:
            if ident in SENTINELS:
                continue
            sites = self.outside_definition(ident) if strict else self.production(ident)
            if len(sites) > 1:
                out.append((ident, sites))
        return sorted(out, key=lambda r: (-len(r[1]), r[0]))

    def sentinel_uses(self) -> dict[str, list[Use]]:
        """Production sites of the sentinels.

        Excluded from the contract because they are not inferences -- but an
        anonymous inference is its own problem, so the count is reported rather
        than hidden.
        """
        return {i: self.production(i)
                for i in self.declared if i in SENTINELS and self.production(i)}

    def unused(self) -> list[str]:
        """Declared ids that nothing produces -- dead markers."""
        return [i for i in self.declared
                if i not in SENTINELS and not self.production(i)]

    def histogram(self, strict: bool = False) -> dict[int, int]:
        h: dict[int, int] = defaultdict(int)
        for ident in self.declared:
            if ident in SENTINELS:
                continue
            n = len(self.outside_definition(ident) if strict else self.production(ident))
            h[n] += 1
        return dict(sorted(h.items()))


def _declared(src: str) -> list[str]:
    """The enum members of InferenceId, in declaration order."""
    path = os.path.join(src, _ENUM_HEADER)
    with open(path, encoding="utf-8", errors="ignore") as fh:
        text = fh.read()
    start = text.find("enum class InferenceId")
    if start < 0:
        return []
    end = text.find("\n};", start)
    body = text[start:end]
    return _MEMBER.findall(body)


def scan(src: str, include_tests: bool = False) -> InferenceIds:
    """Scan a cvc5 source tree for InferenceId uses."""
    model = InferenceIds(declared=_declared(src))
    known = set(model.declared)

    roots = [src]
    if include_tests:
        parent = os.path.dirname(os.path.normpath(src))
        tdir = os.path.join(parent, "test")
        if os.path.isdir(tdir):
            roots.append(tdir)

    for root in roots:
        base = os.path.dirname(os.path.normpath(root)) if root != src else src
        for dirpath, _dirs, files in os.walk(root):
            for fn in files:
                if not fn.endswith(SOURCE_EXT):
                    continue
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, base if root != src else src)
                if root != src:
                    rel = os.path.join("..", os.path.relpath(full, base))
                try:
                    with open(full, encoding="utf-8", errors="ignore") as fh:
                        text = fh.read()
                except OSError:
                    continue
                if "InferenceId::" not in text:
                    continue
                is_def = rel in (_ENUM_HEADER, _ENUM_IMPL)
                for m in _USE.finditer(text):
                    is_case, cmp_op, ident = m.group(1), m.group(2), m.group(3)
                    if ident not in known:
                        continue
                    if is_def:
                        kind = "definition"
                    elif is_case:
                        kind = "dispatch"
                    elif cmp_op:
                        kind = "comparison"
                    else:
                        kind = "production"
                    line = text.count("\n", 0, m.start()) + 1
                    model.uses[ident].append(Use(ident, rel, line, kind))
    return model
