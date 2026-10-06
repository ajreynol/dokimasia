; XorSimplify with two constants and a cancelling pair: (bvxor x #b1100 y #b1010 x) = (bvxor #b0110 y).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvxor x #b1100 y #b1010 x) (bvxor #b0110 y))))
(check-sat)
