; inter (ac) & [a-b]*: none
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (str.in_re x (re.inter (str.to_re "ac") (re.* (re.range "a" "b")) (re.* (str.to_re "a")))))
(check-sat)
