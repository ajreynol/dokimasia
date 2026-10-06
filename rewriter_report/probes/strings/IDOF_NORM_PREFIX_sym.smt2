; normalize symbolic prefix by length
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.indexof (str.++ x "B" z) y (+ (str.len x) 1)) (str.indexof (str.++ x "A" z) y (+ (str.len x) 1)))))
(check-sat)
