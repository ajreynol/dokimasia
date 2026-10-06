; proof: str.<= constant folding on proper prefix
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(assert (= x "abc"))
(assert (str.<= x "ab"))
(check-sat)
