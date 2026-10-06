; ((_ re.loop 0 1) (a)*) ---> (a)*
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x ((_ re.loop 0 1) (re.* (str.to_re "a")))) (str.in_re x (re.* (str.to_re "a"))))))
(check-sat)
