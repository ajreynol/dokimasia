; multiset reasoning
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (str.contains (str.++ x "b") (str.++ "a" x)))
(check-sat)
