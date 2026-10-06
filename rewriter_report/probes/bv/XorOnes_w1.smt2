; XorOnes: width 1 (bvxor b #b1) -> (bvnot b)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const b (_ BitVec 1))
(assert (not (= (bvxor b #b1) (bvnot b))))
(check-sat)
