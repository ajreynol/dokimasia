; (a | _ | b)* ---> _*
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.* (re.union (str.to_re "a") re.allchar (re.++ (str.to_re "b") (str.to_re "a"))))) (str.in_re x (re.* re.allchar)))))
(check-sat)
