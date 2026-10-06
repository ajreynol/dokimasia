; x++AB++z = A++x++y <=> x++A = A++x and B++z = y
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= (str.++ x "AB" z) (str.++ "A" x y)) (and (= (str.++ x "A") (str.++ "A" x)) (= (str.++ "B" z) y)))))
(check-sat)
