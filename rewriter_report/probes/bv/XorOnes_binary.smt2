; XorOnes: (bvxor x #xF) -> (bvnot x)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvxor x #xF) (bvnot x))))
(check-sat)
