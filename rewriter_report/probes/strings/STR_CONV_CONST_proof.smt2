; proof: to_upper constant folding
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(assert (= x "aZ`{"))
(assert (not (= (str.to_upper x) "AZ`{")))
(check-sat)
