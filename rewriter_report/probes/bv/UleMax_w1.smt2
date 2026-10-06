; UleMax: width 1 (bvule b #b1) -> true
; EXPECT: unsat
(set-logic QF_BV)
(declare-const b (_ BitVec 1))
(assert (not (= (bvule b #b1) true)))
(check-sat)
