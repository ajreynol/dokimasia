; "" = substr(x,2,5) <=> len x <= 2
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= "" (str.substr x 2 5)) (<= (str.len x) 2))))
(check-sat)
