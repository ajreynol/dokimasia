; indexof(x++c, a++y, 0) = indexof(x, a++y, 0) when c has no reverse overlap with pattern end
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (= (str.indexof (str.++ x "c") (str.++ y "a") 0) (str.indexof x (str.++ y "a") 0))))
(check-sat)
