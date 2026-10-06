; XorSimplify: duplicate cancellation + constant merge (MACRO_BV_XOR_SIMPLIFY)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (not (= (bvxor x #b0110 y x #b0011 y z) (bvxor z #b0101))))
(check-sat)
