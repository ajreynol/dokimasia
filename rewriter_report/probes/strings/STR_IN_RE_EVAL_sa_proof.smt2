; constant membership evaluates to true
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (str.in_re "abbc" (re.++ (str.to_re "a") (re.* (re.range "b" "c")) (str.to_re "c")))))
(check-sat)
