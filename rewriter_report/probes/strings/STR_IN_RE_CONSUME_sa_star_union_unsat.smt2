; a++x in (ab|b)* with x=a is not a member
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (str.in_re (str.++ "a" x) (re.* (re.union (str.to_re "ab") (str.to_re "b")))))
(assert (= x "a"))
(check-sat)
