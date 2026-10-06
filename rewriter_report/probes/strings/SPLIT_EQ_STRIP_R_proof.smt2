; A++x++y = x++AB++z <=> A++x = x++A and y = B++z
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= (str.++ "A" x y) (str.++ x "AB" z)) (and (= (str.++ "A" x) (str.++ x "A")) (= y (str.++ "B" z))))))
(check-sat)
