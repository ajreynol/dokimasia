; "" = substr(a++x,0,n) <=> n <= 0
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const n Int)
(assert (not (= (= "" (str.substr (str.++ "a" x) 0 n)) (<= n 0))))
(check-sat)
