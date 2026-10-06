; x <= "" iff x = ""; "" <= x
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(assert (or (not (= (str.<= x "") (= x ""))) (not (str.<= "" x))))
(check-sat)
