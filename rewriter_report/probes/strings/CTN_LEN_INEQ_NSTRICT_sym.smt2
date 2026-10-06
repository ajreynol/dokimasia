; rhs at least as long -> equality
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.contains x (str.++ y (str.substr x 0 (str.len x)))) (= x (str.++ y (str.substr x 0 (str.len x)))))))
(check-sat)
