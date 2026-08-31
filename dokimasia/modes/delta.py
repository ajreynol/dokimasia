"""Extract the option changes cvc5 makes, and the conditions that guard them.

`src/smt/set_defaults.cpp` is where cvc5 decides what the solver actually is.
Every change goes through one of five macros:

    SET_AND_NOTIFY(domain, opt, value, reason)
    SET_AND_NOTIFY_IF_NOT_USER(domain, opt, value, reason)
    SET_AND_NOTIFY_VAL_SYM(domain, opt, value, reason)
    SET_AND_NOTIFY_IF_NOT_USER_VAL_SYM(domain, opt, value, reason)
    OPTION_EXCEPTION_IF_NOT(domain, opt, value, reason)   -- refuses instead

This module recovers each call together with the stack of `if` conditions
enclosing it, and tags the conditions that mention a mode.

What this is and is not
-----------------------
It is a **syntactic** extraction: it reports each change with the guards written
around it. It does not solve path conditions, so it cannot by itself decide
whether two guards are jointly satisfiable.

One implication is encoded because it is load-bearing and easy to get wrong:
under `--safe-mode=safe` with proofs on, `setDefaultsPre` upgrades `proofMode`
to `FULL_STRICT`, so everything guarded by `FULL_STRICT` (and by the local
`isFullPf`) is *also* reachable in safe mode. Those rows are marked
``implied_by_safe`` rather than being silently merged, so the inference stays
visible and arguable.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from ..sanity import expect

MACROS = (
    "SET_AND_NOTIFY_IF_NOT_USER_VAL_SYM",
    "SET_AND_NOTIFY_IF_NOT_USER",
    "SET_AND_NOTIFY_VAL_SYM",
    "SET_AND_NOTIFY",
    "OPTION_EXCEPTION_IF_NOT",
)

#: Condition fragments that identify which mode a guard is about.
MODE_TAGS = {
    "safe_or_stable": (r"safeMode\s*!=\s*options::SafeMode::UNRESTRICTED",),
    "safe": (r"safeMode\s*==\s*options::SafeMode::SAFE",),
    "stable": (r"safeMode\s*==\s*options::SafeMode::STABLE",),
    "proofs": (r"\bproduceProofs\b",),
    # FULL_STRICT only counts when the guard tests *for* it. A disjunction
    # that also accepts plain FULL is about enabling proofs, not about the
    # strict mode safe mode upgrades into.
    "full_strict": (r"FULL_STRICT",),
    "full_pf": (r"\bisFullPf\b",),
}


@dataclass
class OptionChange:
    """One option change, with the guards written around it."""

    macro: str
    domain: str
    option: str
    value: str
    reason: str
    line: int
    guards: list[str] = field(default_factory=list)
    tags: set[str] = field(default_factory=set)

    @property
    def refuses(self) -> bool:
        """True if this throws rather than silently changing the option."""
        return self.macro == "OPTION_EXCEPTION_IF_NOT"

    @property
    def respects_user(self) -> bool:
        """True if an explicit user setting wins over this change."""
        return "IF_NOT_USER" in self.macro

    def key(self) -> str:
        return f"{self.domain}.{self.option}"


def _split_args(text: str) -> list[str]:
    """Split a macro argument list on top-level commas."""
    out, depth, cur = [], 0, ""
    for ch in text:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def _tags_for(cond: str) -> set[str]:
    tags = {
        tag for tag, pats in MODE_TAGS.items()
        if any(re.search(p, cond) for p in pats)
    }
    # `ProofMode::FULL` with a word boundary matches only plain FULL, never
    # FULL_STRICT. If the guard offers plain FULL as an alternative, it is not
    # a test for strict mode.
    if "full_strict" in tags and re.search(r"ProofMode::FULL\b", cond):
        tags.discard("full_strict")
    return tags


def parse_set_defaults(src: str) -> list[OptionChange]:
    """Parse ``src/smt/set_defaults.cpp`` into a list of option changes."""
    path = os.path.join(src, "smt", "set_defaults.cpp")
    with open(path, encoding="utf-8", errors="ignore") as fh:
        text = fh.read()

    # Strip the macro *definitions* at the top; we want call sites only.
    body_start = text.find("void SetDefaults::")
    if body_start > 0:
        prefix_lines = text[:body_start].count("\n")
        text = text[body_start:]
    else:
        prefix_lines = 0

    lines = text.split("\n")
    changes: list[OptionChange] = []
    stack: list[tuple[int, str]] = []   # (depth at open, condition text)
    depth = 0
    pending = ""                        # text seen since last statement break

    i = 0
    while i < len(lines):
        raw = lines[i]
        line = re.sub(r"//.*$", "", raw)

        # A macro call may span lines: gather until parens balance.
        m = re.match(r"\s*(" + "|".join(MACROS) + r")\s*\(", line)
        if m:
            macro = m.group(1)
            start_line = i
            chunk = line[line.index("(", m.end(1) - 1):]
            bal = chunk.count("(") - chunk.count(")")
            while bal > 0 and i + 1 < len(lines):
                i += 1
                nxt = re.sub(r"//.*$", "", lines[i])
                chunk += " " + nxt
                bal += nxt.count("(") - nxt.count(")")
            inner = chunk[chunk.index("(") + 1: chunk.rindex(")")]
            args = _split_args(inner)
            if len(args) >= 4:
                guards = [c for _, c in stack if c]
                tags: set[str] = set()
                for gcond in guards:
                    tags |= _tags_for(gcond)
                changes.append(OptionChange(
                    macro=macro, domain=args[0], option=args[1],
                    value=args[2], reason=args[3].strip('"'),
                    line=prefix_lines + start_line + 1,
                    guards=guards, tags=tags,
                ))
            pending = ""
            i += 1
            continue

        # Track brace depth and remember the condition that opened each block.
        for ch in line:
            if ch == "{":
                cond = ""
                mm = re.search(r"\b(?:if|else if)\s*\((.*)\)\s*$", pending.strip(), re.S)
                if mm:
                    cond = " ".join(mm.group(1).split())
                elif pending.strip().endswith("else"):
                    cond = "else"
                depth += 1
                stack.append((depth, cond))
                pending = ""
            elif ch == "}":
                if stack and stack[-1][0] == depth:
                    stack.pop()
                depth -= 1
                pending = ""
            else:
                pending += ch
        # A bare `if (...)` with no brace still guards the next statement; we
        # deliberately ignore those -- every mode guard in this file uses braces.
        if ";" in line:
            pending = ""
        i += 1
    expect(len(changes), 100, "option changes in set_defaults.cpp",
           "the SET_AND_NOTIFY* macro calls in smt/set_defaults.cpp")
    return changes


@dataclass
class ModeDelta:
    """The option changes attributable to a mode."""

    changes: list[OptionChange]

    @classmethod
    def load(cls, src: str) -> "ModeDelta":
        return cls(changes=parse_set_defaults(src))

    def for_mode(self, mode: str, with_proofs: bool = True) -> list[OptionChange]:
        """Changes that apply in *mode* but not in unrestricted-without-proofs.

        ``safe`` includes the shared safe-or-stable block, the safe-only block,
        and -- when proofs are on -- the FULL_STRICT block that safe mode's own
        proofMode upgrade makes reachable.
        """
        want: set[str]
        if mode == "safe":
            want = {"safe", "safe_or_stable"}
            if with_proofs:
                want |= {"full_strict", "full_pf"}
        elif mode == "stable":
            want = {"stable", "safe_or_stable"}
        else:
            return []
        out = [c for c in self.changes if c.tags & want]
        return sorted(out, key=lambda c: (c.key(), c.line))

    def implied(self, c: OptionChange, mode: str) -> bool:
        """True if this row is reachable only via safe mode's proofMode upgrade."""
        return (
            mode == "safe"
            and not (c.tags & {"safe", "safe_or_stable"})
            and bool(c.tags & {"full_strict", "full_pf"})
        )


# --- option defaults, read from src/options/*.toml -------------------------

_OPT_BLOCK = re.compile(r"\[\[option\]\](.*?)(?=\[\[|\Z)", re.S)
_FIELD = re.compile(r'^\s*(\w+)\s*=\s*(.+?)\s*$', re.M)


def parse_option_defaults(src: str) -> dict[str, dict[str, str]]:
    """Map option name -> {long, type, default, category} from the .toml files."""
    out: dict[str, dict[str, str]] = {}
    odir = os.path.join(src, "options")
    if not os.path.isdir(odir):
        return out
    for fn in sorted(os.listdir(odir)):
        if not fn.endswith(".toml"):
            continue
        with open(os.path.join(odir, fn), encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
        for block in _OPT_BLOCK.findall(text):
            fields = {}
            for k, v in _FIELD.findall(block):
                fields[k] = v.strip().strip('"').strip("'")
            name = fields.get("name")
            if name:
                out[name] = {
                    "no_support": fields.get("no_support", ""),
                    "long": fields.get("long", ""),
                    "type": fields.get("type", ""),
                    "default": fields.get("default", ""),
                    "category": fields.get("category", ""),
                    "file": fn,
                }
    return out



# --- the consistency check ------------------------------------------------

def unsupported_but_enabled(src: str, delta: "ModeDelta") -> list[dict]:
    """Options that declare no proof support yet survive safe mode's defaults.

    cvc5's option definitions carry a machine-readable ``no_support`` field;
    fifteen options declare ``no_support = ["proofs"]``. Safe mode promises no
    feature "that does not have full proof and model support", so every such
    option must be off in a safe-mode run.

    Two mechanisms enforce that today and neither is complete on its own:

    * ``SetDefaults::setDefaultsPre`` disables some of them **by name** -- a
      hand-maintained list;
    * ``SolverEngine`` throws if a user *sets* a regular option whose
      ``noSupports`` is non-empty -- but that fires on assignment only, so it
      says nothing about an option that is already on by default.

    The gap between them is what this returns: an option declaring no proof
    support, whose default is on, that safe mode never turns off.
    """
    defaults = parse_option_defaults(src)
    touched = {c.option for c in delta.for_mode("safe")}
    off_values = {"false", "off", "none", "0", ""}
    out = []
    for name, info in sorted(defaults.items()):
        ns = info.get("no_support", "")
        if "proofs" not in ns:
            continue
        default_on = info.get("default", "").strip().lower() not in off_values
        if default_on and name not in touched:
            out.append({
                "option": name,
                "long": info.get("long", ""),
                "default": info.get("default", ""),
                "no_support": ns,
                "file": info.get("file", ""),
            })
    return out
