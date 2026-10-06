; AB++x++w++y = x++A++w++BC++z: strip across a symbolic middle w
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= (str.++ "AB" x w y) (str.++ x "A" w "BC" z)) (and (= (str.++ "AB" x w) (str.++ x "A" w "B")) (= y (str.++ "C" z))))))
(check-sat)
