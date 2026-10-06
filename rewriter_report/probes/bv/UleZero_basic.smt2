; UleZero: (bvule x 0) -> (= x 0)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvule x #x0) (= x #x0))))
(check-sat)
