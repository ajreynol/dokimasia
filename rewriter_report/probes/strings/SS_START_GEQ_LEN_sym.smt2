; outer start >= inner length
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.substr (str.substr x n m) (+ m (str.len y)) 3) "")))
(check-sat)
