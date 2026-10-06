; "a" = replace("",x,y) <=> x="" and y="a"
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= "a" (str.replace "" x y)) (and (= x "") (= y "a")))))
(check-sat)
