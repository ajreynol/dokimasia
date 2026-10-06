; re.all ---> (re.* re.allchar)
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x re.all) (str.in_re x (re.* re.allchar)))))
(check-sat)
