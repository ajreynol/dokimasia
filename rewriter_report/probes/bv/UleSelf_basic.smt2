; UleSelf: (bvule x x) -> true
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvule x x) true)))
(check-sat)
