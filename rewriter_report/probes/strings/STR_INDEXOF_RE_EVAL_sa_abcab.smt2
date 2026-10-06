; indexof_re abcab (ab) from 1 is 3 (z3 lacks str.indexof_re: ignore z3)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (= (str.indexof_re "abcab" (str.to_re "ab") 1) 3)))
(check-sat)
