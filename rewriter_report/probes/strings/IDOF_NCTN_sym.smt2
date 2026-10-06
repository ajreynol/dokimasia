; does not contain
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.indexof (str.++ "ab" x) (str.++ x "c" x "ab") n) (- 1))))
(check-sat)
