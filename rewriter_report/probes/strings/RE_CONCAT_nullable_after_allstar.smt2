; nullable const regex after (re.* re.allchar) dropped
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.++ (re.* re.allchar) (re.* (str.to_re "b")) (re.union (str.to_re "") (str.to_re "cd")) (str.to_re "a"))) (str.in_re x (re.++ (re.* re.allchar) (str.to_re "a"))))))
(check-sat)
