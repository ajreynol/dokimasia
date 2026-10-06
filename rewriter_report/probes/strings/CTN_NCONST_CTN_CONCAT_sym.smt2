; const does not contain concat with chars not in const
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (str.contains "abc" (str.++ x "d" y)))
(check-sat)
