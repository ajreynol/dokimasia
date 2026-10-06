; (a)*(a)* ---> (a)*
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.++ (re.* (str.to_re "a")) (re.* (str.to_re "a")) (str.to_re "b"))) (str.in_re x (re.++ (re.* (str.to_re "a")) (str.to_re "b"))))))
(check-sat)
