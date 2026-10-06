; re.union with _* ---> _*
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.union (str.to_re "a") (re.* re.allchar))) (str.in_re x (re.* re.allchar)))))
(check-sat)
