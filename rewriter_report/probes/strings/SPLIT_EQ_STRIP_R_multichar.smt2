; AB++x++y = x++ABC++z <=> AB++x = x++AB and y = C++z
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= (str.++ "AB" x y) (str.++ x "ABC" z)) (and (= (str.++ "AB" x) (str.++ x "AB")) (= y (str.++ "C" z))))))
(check-sat)
