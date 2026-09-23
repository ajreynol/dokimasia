"""Adversarial fixtures for the two proof-path checks, plus checkout smoke tests."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from dokimasia_analyzer import cpp, sanity, source
from dokimasia_analyzer.findings import collect
from dokimasia_analyzer.preprocess.scan import scan as preprocess
from dokimasia_analyzer.proofshape.scan import scan as proofshape

REAL = sys.argv.pop(1) if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else None

ENGINE = '''
TrustNode TheoryEngine::ppRewrite(Node n, std::vector<SkolemLemma>& lems) {
  for (SkolemLemma& sk : lems) {
    if (sk.d_lemma.getGenerator() == nullptr) {
      d_proof->addTrustedStep(n, TrustId::THEORY_PREPROCESS_LEMMA, {}, {});
    }
  }
  return TrustNode::null();
}
'''

CHECKER = '''
Node Checker::checkInternal(ProofRule id, const std::vector<Node>& children,
                            const std::vector<Node>& args) {
  if (id == ProofRule::EXACT) {
    Assert(children.size() == 2);
    Assert(args.empty());
    return children[0];
  } else if (id == ProofRule::MINIMUM) {
    Assert(children.size() > 0);
    Assert(args.size() >= 2);
    return args[0];
  }
  return Node::null();
}
'''


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'src/theory').mkdir(parents=True)
        self.write('src/theory/theory_engine.cpp', ENGINE)
        self.write('src/checker.cpp', CHECKER)
        source.clear()
        self.addCleanup(source.clear)

    def write(self, path, text):
        (self.root / path).write_text(text)
        source.clear()

    def scan_shape(self, text):
        self.write('src/caller.cpp', text)
        with sanity.disabled():
            return proofshape(str(self.root))

    def scan_pp(self, text):
        self.write('src/theory/test.cpp', text)
        with sanity.disabled():
            return preprocess(str(self.root))

    def test_both_addstep_conventions_and_node_manager(self):
        r = self.scan_shape('''
void f() {
  cdp.addStep(conclusion, ProofRule::EXACT, {p}, {});
  psb.addStep(ProofRule::EXACT, {p, q}, {extra}, conclusion);
  pnm->mkNode(ProofRule::MINIMUM, {}, {a, b});
  cdp.addStep(conclusion, ProofRule::MINIMUM, {p}, {a});
}
''')
        self.assertEqual([(r['vector'], r['supplied'], r['expected']) for r in r.issues],
                         [('children', 1, '==2'), ('args', 1, '==0'),
                          ('children', 0, '>0'), ('args', 1, '>=2')])
        self.assertTrue(all(row['checker'].startswith('src/checker.cpp:') for row in r.issues))
        self.assertEqual(r.compared, 4)

    def test_valid_calls_nested_commas_trailing_comma_and_literals(self):
        r = self.scan_shape('''
  cdp.addStep(n, ProofRule::EXACT, {nm->mkNode(k, a, b), p[0],}, {});
  psb.addStep(ProofRule::MINIMUM, {p}, {f("a,b"), g('}'), x});
  other.mkNode(Kind::FOO, {p}, {});
''')
        self.assertEqual((r.calls, r.compared, r.issues), (2, 2, []))

    def test_comments_raw_strings_and_continued_comments_do_not_emit(self):
        r = self.scan_shape('''
/* cdp.addStep(n, ProofRule::EXACT, {}, {}); */
auto x = R"tag(cdp.addStep(n, ProofRule::EXACT, {}, {}); })tag";
auto y = "escaped \\\" cdp.addStep(n, ProofRule::EXACT, {}, {});";
// hidden \\
cdp.addStep(n, ProofRule::EXACT, {}, {});
''')
        self.assertEqual(r.calls, 0)

    def test_dynamic_and_template_expressions_stay_unknown(self):
        r = self.scan_shape('''
  cdp.addStep(n, ProofRule::EXACT, children, args);
  cdp.addStep(n, ProofRule::EXACT, {make<A, B>()}, args);
  cdp.addStep(n, dynamicRule, {}, {});
  psb.addStep(ProofRule::UNKNOWN, {}, {});
''')
        self.assertEqual((r.calls, r.compared, r.unknown, r.issues), (3, 0, 3, []))

    def test_nested_and_late_assertions_are_not_entry_contracts(self):
        self.write('src/checker.cpp', '''
Node Checker::checkInternal(ProofRule id) {
  if (id == ProofRule::EXACT) {
    if (flag) { Assert(args.empty()); }
    Assert(children.empty());
  }
  if (flag) { if (id == ProofRule::MINIMUM) { Assert(args.empty()); } }
}
Node Other::helper(ProofRule id) {
  if (id == ProofRule::EXACT) { Assert(args.empty()); }
}
''')
        r = self.scan_shape('psb.addStep(ProofRule::EXACT, {p}, {a});')
        self.assertEqual(r.contracts, [])
        self.assertEqual(r.issues, [])

    def test_assert_after_unbraced_control_flow_or_preprocessor_is_unknown(self):
        for prefix in ('if (flag) return n;', '#ifdef SOMETHING\nAssert(flag);'):
            with self.subTest(prefix=prefix):
                self.write('src/checker.cpp', '''
Node Checker::checkInternal(ProofRule id) {
  if (id == ProofRule::EXACT) { ''' + prefix + ''' Assert(args.empty()); }
}
''')
                self.assertEqual(self.scan_shape('psb.addStep(ProofRule::EXACT, {}, {a});').issues, [])

    def test_duplicate_contract_is_unknown_not_a_false_disagreement(self):
        self.write('src/checker.cpp', CHECKER + CHECKER.replace('Checker::', 'Other::'))
        r = self.scan_shape('psb.addStep(ProofRule::EXACT, {}, {});')
        self.assertEqual(r.issues, [])
        self.assertIn('EXACT', r.ambiguous_rules)

    def test_contract_evidence_line_is_the_assertion(self):
        r = self.scan_shape('')
        for contract in r.contracts:
            path, line = contract.location.rsplit(':', 1)
            self.assertIn('Assert(', (self.root / path).read_text().splitlines()[int(line) - 1])

    def test_pp_adjacent_binding_and_local_call_chain(self):
        r = self.scan_pp('''
TrustNode Theory::ppRewrite(Node n, std::vector<SkolemLemma>& lems) {
  return this->expand(n, lems);
}
TrustNode Theory::expand(Node n, std::vector<SkolemLemma>& lems) {
  TrustNode tlem = TrustNode::mkTrustLemma(f(n, x), nullptr);
  lems.push_back(SkolemLemma(tlem, x));
}
''')
        self.assertEqual(len(r.issues), 1)
        self.assertEqual(r.issues[0]['call_path'], ['Theory::ppRewrite', 'Theory::expand'])
        self.assertEqual(r.issues[0]['location'], 'src/theory/test.cpp:7')

    def test_pp_inline_construction(self):
        r = self.scan_pp('''
TrustNode Theory::ppRewrite(Node n, std::vector<SkolemLemma>& lems) {
  lems.push_back(SkolemLemma(TrustNode::mkTrustLemma(n, nullptr), x));
}
''')
        self.assertEqual(len(r.issues), 1)

    def test_pp_generator_nonlocal_and_unrelated_methods_are_unknown(self):
        r = self.scan_pp('''
TrustNode Theory::ppRewrite(Node n, std::vector<SkolemLemma>& lems) {
  lems.push_back(SkolemLemma(TrustNode::mkTrustLemma(n, this), x));
  lems.push_back(SkolemLemma(eagerReduceTrusted(n), x));
  other.expand(n, lems);
  ptr->expand(n, lems);
  other. expand(n, lems);
  ptr -> expand(n, lems);
  return TrustNode::mkTrustRewrite(n, x, nullptr);
}
TrustNode Theory::expand(Node n, std::vector<SkolemLemma>& lems) {
  lems.push_back(SkolemLemma(TrustNode::mkTrustLemma(n, nullptr), x));
}
''')
        self.assertEqual(r.issues, [])

    def test_pp_reassigned_or_branch_local_binding_is_unknown(self):
        for middle in ('tlem = withProof();', 'touch(tlem);', '}'):
            r = self.scan_pp('''
TrustNode Theory::ppRewrite(Node n, std::vector<SkolemLemma>& lems) {
  { TrustNode tlem = TrustNode::mkTrustLemma(n, nullptr);
''' + middle + '''
  lems.push_back(SkolemLemma(tlem, x));
  }
}
''')
            self.assertEqual(r.issues, [])

    def test_proof_guard_at_root_or_helper_stays_unknown(self):
        for method in ('root', 'helper'):
            guard = 'if (d_env.isTheoryProofProducing()) return withProof();'
            r = self.scan_pp('''
TrustNode Theory::ppRewrite(Node n, std::vector<SkolemLemma>& lems) {
''' + (guard if method == 'root' else '') + '''
  return expand(n, lems);
}
TrustNode Theory::expand(Node n, std::vector<SkolemLemma>& lems) {
''' + (guard if method == 'helper' else '') + '''
  lems.push_back(SkolemLemma(TrustNode::mkTrustLemma(n, nullptr), x));
}
''')
            self.assertEqual((r.guarded, r.issues), (1, []))

    def test_missing_engine_fallback_fails_loudly(self):
        self.write('src/theory/theory_engine.cpp', ENGINE.replace('getGenerator', 'renamed'))
        with self.assertRaises(sanity.ExtractionError):
            self.scan_pp('')

    def test_missing_checker_dispatch_fails_loudly(self):
        self.write('src/checker.cpp', CHECKER.replace('checkInternal', 'renamed'))
        with self.assertRaises(sanity.ExtractionError):
            proofshape(str(self.root))

    def test_missing_producer_calls_fail_even_with_checker_contracts(self):
        self.write('src/checker.cpp', 'Node Checker::checkInternal(ProofRule id) {\n'
            + ''.join(f'if (id == ProofRule::R{i}) {{ Assert(args.empty()); }}\n'
                      for i in range(85)) + '}')
        with self.assertRaisesRegex(sanity.ExtractionError, 'proof construction calls'):
            proofshape(str(self.root))

    def test_observations_aggregate_sites_and_identity_ignores_line_shifts(self):
        self.write('src/caller.cpp', 'p.addStep(ProofRule::EXACT, {}, {});\n' * 2)
        with sanity.disabled():
            before = collect(str(self.root), ['proofshape'])
        self.assertEqual(len(before.dump()), 1)
        self.assertEqual(len(next(iter(before.evidence.values()))), 2)
        self.write('src/caller.cpp', '\n\n' + (self.root / 'src/caller.cpp').read_text())
        with sanity.disabled():
            after = collect(str(self.root), ['proofshape'])
        self.assertEqual(before.dump(), after.dump())
        self.assertNotEqual(before.evidence, after.evidence)


@unittest.skipUnless(REAL, 'provide a cvc5 checkout')
class Checkout(unittest.TestCase):
    def test_scan(self):
        result = collect(REAL, ['preprocess', 'proofshape'])
        self.assertGreater(result.measurements['proofshape']['compared_calls'], 300)
        for bug in result.dump():
            self.assertIn(bug['code'], ('INFER0001', 'API0005'))
        # Exact expectations belong to the reference revision only.
        import subprocess
        rev = subprocess.check_output(['git', '-C', REAL, 'rev-parse', 'HEAD'], text=True).strip()
        pin = json.loads((ROOT / 'scripts/cvc5.lock').read_text())['cvc5']['commit']
        if rev.startswith(pin):
            self.assertEqual({b['entity'] for b in result.dump()}, {
                'src/theory/sets/theory_sets_private.cpp#TheorySetsPrivate::expandChooseOperator',
                'src/theory/bags/theory_bags.cpp#TheoryBags::expandChooseOperator'})


if __name__ == '__main__':
    unittest.main()
