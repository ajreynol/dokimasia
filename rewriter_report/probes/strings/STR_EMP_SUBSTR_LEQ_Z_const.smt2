; "" = substr("abc",0,n) <=> n <= 0
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const n Int)
(assert (not (= (= "" (str.substr "abc" 0 n)) (<= n 0))))
(check-sat)
