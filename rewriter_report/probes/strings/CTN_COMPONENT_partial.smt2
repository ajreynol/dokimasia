; component containment of const in middle of const
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (str.contains (str.++ x "abcd" y) "bc")))
(check-sat)
