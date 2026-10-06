; str.< elimination
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)(declare-const y String)
(assert (not (= (str.< x y) (and (not (= x y)) (str.<= x y)))))
(check-sat)
