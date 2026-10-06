; XorZero: (bvxor x y #x0) -> (bvxor x y)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvxor x y #x0) (bvxor x y))))
(check-sat)
