; nullable const regex before (re.* re.allchar) dropped
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.++ (str.to_re "a") (re.* (str.to_re "b")) (re.opt (str.to_re "cd")) (re.* re.allchar))) (str.in_re x (re.++ (str.to_re "a") (re.* re.allchar))))))
(check-sat)
