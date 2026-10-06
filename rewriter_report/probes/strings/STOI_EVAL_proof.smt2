; proof: str.to_int of leading-zero literal
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(assert (= x "0010"))
(assert (not (= (str.to_int x) 10)))
(check-sat)
