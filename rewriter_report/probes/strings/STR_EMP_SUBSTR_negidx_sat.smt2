; sat: substr(x,-1,5) = "" with x nonempty (negative start not covered by LEQ_LEN)
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(assert (= "" (str.substr x (- 1) 5)))
(assert (= x "abc"))
(check-sat)
