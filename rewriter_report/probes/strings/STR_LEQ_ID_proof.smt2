; x <= x
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(assert (not (str.<= x x)))
(check-sat)
