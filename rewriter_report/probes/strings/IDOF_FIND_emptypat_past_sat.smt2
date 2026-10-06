; empty pattern past head constant is not -1 when x long
; EXPECT: sat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.indexof (str.++ "ab" x) "" 3) (- 1))))
(check-sat)
