; UleMax: (bvule x ones) -> true
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvule x #xF) true)))
(check-sat)
