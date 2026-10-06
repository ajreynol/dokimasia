; z++a = replace("",x,y) <=> x="" and y=z++a
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= (str.++ z "a") (str.replace "" x y)) (and (= x "") (= y (str.++ z "a"))))))
(check-sat)
