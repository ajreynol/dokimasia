"""Compare literal proof-step lists to unconditional checker assertions.

Only single-rule if arms and leading, top-level Assert statements are used.
No index-based bound, nested assertion, or assertion after control flow is a
contract here. Dynamic lists and rule expressions remain unexamined.
"""
from __future__ import annotations

import os
import re
from collections import Counter
from dataclasses import dataclass, field

from .. import cpp, source
from ..sanity import expect


@dataclass(frozen=True)
class Bound:
    rule: str
    vector: str
    op: str
    count: int
    location: str

    def accepts(self, count):
        return {'==': count == self.count, '>=': count >= self.count,
                '>': count > self.count}[self.op]


@dataclass
class Result:
    contracts: list[Bound] = field(default_factory=list)
    issues: list[dict] = field(default_factory=list)
    calls: int = 0
    compared: int = 0
    unknown: int = 0
    ambiguous_rules: list[str] = field(default_factory=list)


def contracts(text: str, path: str) -> list[Bound]:
    out = []
    for fn in cpp.functions(text):
        if not fn.name.endswith('::checkInternal'):
            continue
        body = text[fn.start + 1:fn.end]
        # Braces are required. Shared/combined dispatch and switch arms are
        # unknown; this avoids attributing a nested rule test to another rule.
        for m in re.finditer(r'\bif\s*\(\s*id\s*==\s*ProofRule::(\w+)\s*\)\s*\{', body):
            if body[:m.start()].count('{') != body[:m.start()].count('}'):
                continue
            end = cpp.closing(body, m.end() - 1)
            if end is None:
                continue
            arm = body[m.end():end]
            pos = 0
            while pos < len(arm):
                # Consume only the straight-line prefix, before any nested
                # scope or branch. Parentheses can contain initializer calls.
                statement = re.match(r'\s*([^;{}]*);', arm[pos:])
                if not statement:
                    break
                stmt = statement[1].strip()
                if '#' in stmt or re.search(r'\b(if|for|while|switch|return|goto|throw)\b', stmt):
                    break
                exact = re.fullmatch(
                    r'Assert\s*\(\s*(children|args)\s*\.\s*'
                    r'(?:size\s*\(\s*\)\s*(==|>=|>)\s*(\d+)|empty\s*\(\s*\))\s*\)', stmt)
                if exact:
                    line = text.count('\n', 0, fn.start + 1 + m.end() + pos) + 1
                    # Locate the token rather than the preceding whitespace.
                    line += statement[0][:statement[0].index('Assert')].count('\n')
                    out.append(Bound(m[1], exact[1], exact[2] or '==',
                                     int(exact[3] or 0), f'{path}:{line}'))
                pos += statement.end()
    return out


def scan(root: str) -> Result:
    result = Result()
    files = [(os.path.relpath(p, root), cpp.mask(source.read(p)))
             for p in source.walk(os.path.join(root, 'src'), ('.cpp', '.h'))]
    for path, text in files:
        if 'checkInternal' in text:
            result.contracts.extend(contracts(text, path))
    expect(len({c.rule for c in result.contracts}), 80, 'rules with entry arity assertions',
           'single-rule if arms in checkInternal')
    by_rule = {}
    for c in result.contracts:
        by_rule.setdefault(c.rule, []).append(c)
    for rule, bounds in list(by_rule.items()):
        if max(Counter(c.vector for c in bounds).values()) > 1:
            result.ambiguous_rules.append(rule)
            del by_rule[rule]
    for path, text in files:
        for m, end, args in cpp.calls(text, r'(?:\.|->)\s*(addStep|mkNode)'):
            if args is None:
                if 'ProofRule::' in text[m.end():end]:
                    result.calls += 1
                    result.unknown += 1
                continue
            # ProofStepBuffer / ProofNodeManager put the rule first; CDProof
            # and BufferedProofGenerator put the conclusion first.
            slot = next((i for i in (0, 1) if i < len(args)
                         and re.fullmatch(r'ProofRule::\w+', args[i])), None)
            if slot is None or (m[1] == 'mkNode' and slot != 0):
                continue
            result.calls += 1
            if len(args) < slot + 3:
                result.unknown += 1
                continue
            rule = args[slot].split('::')[1]
            checked = False
            for contract in by_rule.get(rule, []):
                value = cpp.list_size(args[slot + (1 if contract.vector == 'children' else 2)])
                if value is None:
                    continue
                checked = True
                if not contract.accepts(value):
                    result.issues.append(dict(rule=rule, vector=contract.vector,
                        supplied=value, expected=f'{contract.op}{contract.count}',
                        location=f'{path}:{text.count(chr(10), 0, m.start()) + 1}',
                        checker=contract.location, api=m[1]))
            if checked:
                result.compared += 1
            else:
                result.unknown += 1
    expect(result.calls, 100, 'literal-rule proof construction calls',
           'addStep and mkNode member calls in src/')
    expect(result.compared, 100, 'calls with a comparable literal list',
           'proof construction lists and checker entry assertions')
    return result
