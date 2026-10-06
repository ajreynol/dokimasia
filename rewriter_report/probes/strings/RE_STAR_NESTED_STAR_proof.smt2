; ((R)*)* ---> R*
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.* (re.* (str.to_re "a")))) (str.in_re x (re.* (str.to_re "a"))))))
(check-sat)
