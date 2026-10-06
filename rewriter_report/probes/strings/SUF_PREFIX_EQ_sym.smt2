; prefixof x x
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (str.prefixof (str.++ x y) (str.++ x y))))
(check-sat)
