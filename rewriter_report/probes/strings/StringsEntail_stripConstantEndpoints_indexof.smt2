; indexof(x++"ab", "c"++y++"d", 0) = indexof(x, ...)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.indexof (str.++ x "ab") (str.++ "c" y "d") 0) (str.indexof x (str.++ "c" y "d") 0))))
(check-sat)
