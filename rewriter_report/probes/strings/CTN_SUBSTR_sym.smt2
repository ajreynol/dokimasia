; contains (substr x n len y) y
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.contains (str.substr x n (str.len y)) y) (= (str.substr x n (str.len y)) y))))
(check-sat)
