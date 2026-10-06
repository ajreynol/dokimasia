; x++y++z = x++w++z <=> y = w
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= (str.++ x y z) (str.++ x w z)) (= y w))))
(check-sat)
