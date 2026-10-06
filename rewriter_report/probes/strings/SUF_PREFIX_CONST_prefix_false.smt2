; constant prefixof false, longer prefix
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (str.prefixof "abcd" "abc"))
(check-sat)
