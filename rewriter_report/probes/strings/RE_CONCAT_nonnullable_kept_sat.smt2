; sat check: non-nullable b before _* must NOT be dropped
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.++ (str.to_re "b") (re.* re.allchar))) (str.in_re x (re.* re.allchar)))))
(check-sat)
