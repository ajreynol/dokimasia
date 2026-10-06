; contains(c++x++d, a++y): leading c cannot start a match
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (= (str.contains (str.++ "c" x "d") (str.++ "a" y)) (str.contains (str.++ x "d") (str.++ "a" y)))))
(check-sat)
