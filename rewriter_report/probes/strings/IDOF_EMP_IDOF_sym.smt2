; indexof x empty z with 0<=z<=len x
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.indexof (str.++ x y) "" (str.len x)) (str.len x))))
(check-sat)
