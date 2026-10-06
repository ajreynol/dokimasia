; partial strip of constant prefix by overlap
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.indexof (str.++ "abc" x "cd") "cd" 0) (+ 2 (str.indexof (str.++ "c" x "cd") "cd" 0)))))
(check-sat)
