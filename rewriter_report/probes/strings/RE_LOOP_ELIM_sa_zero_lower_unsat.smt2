; re.loop 0 2 of a: no string of length 3
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (str.in_re x ((_ re.loop 0 2) (str.to_re "a"))))
(assert (= (str.len x) 3))
(check-sat)
