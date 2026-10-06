; const vs concat with differing first char
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const y String)
(assert (str.<= "b" (str.++ "a" y)))
(check-sat)
