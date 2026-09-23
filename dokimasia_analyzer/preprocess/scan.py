"""The narrow, textual subset of INFER0001 with an explicit null generator.

Follow local calls from ppRewrite through methods accepting SkolemLemma output
vectors. Recognize inline mkTrustLemma calls and adjacent TrustNode assignments.
Any proof-mode/generator handling in a method on the path makes it unknown.
This is intentionally not a general call graph or proof-generator analysis.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

from .. import cpp, source
from ..sanity import expect, ExtractionError


@dataclass
class Result:
    methods: int = 0
    reachable: int = 0
    guarded: int = 0
    issues: list[dict] = field(default_factory=list)
    fallback: str = ''


def _null_lemma(expr):
    m = re.fullmatch(r'TrustNode::mkTrustLemma\s*\(([\s\S]*)\)', expr.strip())
    args = cpp.split(m[1]) if m else None
    return args is not None and len(args) == 2 and args[1] == 'nullptr'


def scan(root: str) -> Result:
    result = Result()
    engine = 'src/theory/theory_engine.cpp'
    text = cpp.mask(source.read(os.path.join(root, engine)))
    anchor = next((f for f in cpp.functions(text) if f.name == 'TheoryEngine::ppRewrite'), None)
    if anchor is None:
        raise ExtractionError('missing TheoryEngine::ppRewrite fallback anchor')
    body = text[anchor.start:anchor.end]
    fallback = re.search(r'\bTrustId::THEORY_PREPROCESS_LEMMA\b', body)
    if fallback is None or not re.search(r'getGenerator\s*\(\s*\)\s*==\s*nullptr', body):
        raise ExtractionError('TheoryEngine::ppRewrite null-generator fallback changed; review INFER0001')
    result.fallback = f'{engine}:{text.count(chr(10), 0, anchor.start + fallback.start()) + 1}'
    for path in source.walk(os.path.join(root, 'src/theory'), ('.cpp',)):
        text = cpp.mask(source.read(path))
        methods = {}
        for fn in cpp.functions(text):
            param = re.search(r'\bstd::vector\s*<\s*(?:theory::)?SkolemLemma\s*>\s*&\s*(\w+)', fn.params)
            if param:
                methods[fn.name] = (fn, param[1])
        result.methods += len(methods)
        paths = {name: [name] for name in methods if name.endswith('::ppRewrite')
                 and name != 'TheoryEngine::ppRewrite'}
        pending = list(paths)
        while pending:
            name = pending.pop()
            fn, vector = methods[name]
            body = text[fn.start + 1:fn.end]
            result.reachable += 1
            if re.search(r'\b(?:isTheoryProofProducing|isProofEnabled|isProofProducing|getGenerator)\s*\(', body):
                result.guarded += 1
                continue
            # Follow only calls on this object with the same output vector.
            for target in methods:
                if target.rsplit('::', 1)[0] != name.rsplit('::', 1)[0] or target in paths:
                    continue
                short = target.rsplit('::', 1)[1]
                for call, _, args in cpp.calls(body, r'(?<![\w:.>])(?:this\s*->\s*)?' + re.escape(short)):
                    if body[:call.start()].rstrip().endswith(('.', '->', '::')):
                        continue
                    if args and vector in args:
                        paths[target] = paths[name] + [target]
                        pending.append(target)
                        break
            for m, end, args in cpp.calls(body, r'\b' + re.escape(vector) + r'\s*\.\s*push_back'):
                if args is None or len(args) != 1:
                    continue
                sk = re.fullmatch(r'SkolemLemma\s*\(([\s\S]*)\)', args[0])
                skargs = cpp.split(sk[1]) if sk else None
                if not skargs or len(skargs) != 2:
                    continue
                value = skargs[0]
                if re.fullmatch(r'\w+', value):
                    # Adjacent assignment only: no branch, reassignment, helper
                    # mutation, or unrelated call can intervene.
                    binding = re.search(r'\bTrustNode\s+' + re.escape(value)
                        + r'\s*=\s*([^;]+);\s*$', body[:m.start()])
                    value = binding[1] if binding else ''
                if _null_lemma(value):
                    result.issues.append(dict(function=name, call_path=paths[name],
                        location=f'{os.path.relpath(path, root)}:{text.count(chr(10), 0, fn.start + 1 + m.start()) + 1}',
                        fallback=result.fallback, generator='nullptr'))
    expect(result.methods, 5, 'SkolemLemma output methods', 'theory ppRewrite methods')
    expect(result.reachable, 3, 'ppRewrite paths', 'theory ppRewrite methods')
    return result
