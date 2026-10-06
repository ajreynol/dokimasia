; XorZero (after XorSimplify const fold): (bvxor x #x3 y #x3) -> (bvxor x y)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvxor x #x3 y #x3) (bvxor x y))))
(check-sat)
