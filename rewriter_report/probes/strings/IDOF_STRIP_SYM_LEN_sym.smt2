; strip symbolic length prefix
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.indexof (str.++ x "ab" y) "b" (str.len x)) (+ (str.len x) (str.indexof (str.++ "ab" y) "b" 0)))))
(check-sat)
