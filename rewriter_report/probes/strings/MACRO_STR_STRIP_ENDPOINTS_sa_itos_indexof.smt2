; indexof(x++from_int(n), y++b, 0) = indexof(x, y++b, 0)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.indexof (str.++ x (str.from_int n)) (str.++ y "b") 0) (str.indexof x (str.++ y "b") 0))))
(check-sat)
