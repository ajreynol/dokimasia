; replace(c++x, a, z) = c++replace(x, a, z)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (= (str.replace (str.++ "c" x) "a" y) (str.++ "c" (str.replace x "a" y)))))
(check-sat)
