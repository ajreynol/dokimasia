; "" = substr(x,0,5) <=> x = ""
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= "" (str.substr x 0 5)) (= x ""))))
(check-sat)
