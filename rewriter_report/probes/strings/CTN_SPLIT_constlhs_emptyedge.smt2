; const lhs, len<=1 rhs that is empty: must be true
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (str.contains "ab" (str.substr x 0 1))))
(assert (= x ""))
(check-sat)
