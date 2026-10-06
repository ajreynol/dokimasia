; contains(c++x++d, a++y++b) = contains(x, a++y++b)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (= (str.contains (str.++ "c" x "d") (str.++ "a" y "b")) (str.contains x (str.++ "a" y "b")))))
(check-sat)
