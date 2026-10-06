; indexof(x++cd, y++a, 0) = indexof(x, y++a, 0)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (= (str.indexof (str.++ x "cd") (str.++ y "a") 0) (str.indexof x (str.++ y "a") 0))))
(check-sat)
