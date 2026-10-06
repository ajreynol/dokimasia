; split contains over constant middle not containing char
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.contains (str.++ x "AB" y) "C") (or (str.contains x "C") (str.contains y "C")))))
(check-sat)
