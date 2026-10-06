; normalize prefix before start
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.indexof (str.++ "ABCD" x) y 3) (str.indexof (str.++ "AAAD" x) y 3))))
(check-sat)
