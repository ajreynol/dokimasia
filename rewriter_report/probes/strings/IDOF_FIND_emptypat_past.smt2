; empty pattern, start past head constant; x empty gives -1
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.indexof (str.++ "ab" x) "" 3) (- 1))))
(assert (= (str.len x) 0))
(check-sat)
