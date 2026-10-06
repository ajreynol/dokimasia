; partial overlap of constant endpoint: contains(ab++x, b++y) must keep b
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (= (str.contains (str.++ "ab" x) (str.++ "b" y)) (str.contains (str.++ "b" x) (str.++ "b" y)))))
(check-sat)
