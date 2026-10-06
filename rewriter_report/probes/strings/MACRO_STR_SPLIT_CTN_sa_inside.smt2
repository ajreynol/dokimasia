; pattern inside middle constant: x++abc++y contains b always
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (str.contains (str.++ x "abc" y) "b")))
(check-sat)
