; "" = replace(x,y,x) <=> x = ""
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= "" (str.replace x y x)) (= x ""))))
(check-sat)
