; x = replace(y,x,y) <=> x = y
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= x (str.replace y x y)) (= x y))))
(check-sat)
