; replace(c++x++d, a++y++b, n) = c++replace(x,..)++d
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(declare-const z String)
(assert (not (= (str.replace (str.++ "c" x "d") (str.++ "a" y "b") z) (str.++ "c" (str.replace x (str.++ "a" y "b") z) "d"))))
(check-sat)
