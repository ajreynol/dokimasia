; indexof x x n normalizes to empty
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.indexof x x n) (str.indexof "" "" n))))
(check-sat)
