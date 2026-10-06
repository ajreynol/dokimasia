; indexof strip endpoints
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.indexof (str.++ x "A") "B" 0) (str.indexof x "B" 0))))
(check-sat)
