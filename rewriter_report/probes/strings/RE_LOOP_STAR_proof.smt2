; ((_ re.loop 2 3) (a)*) ---> (a)*
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x ((_ re.loop 2 3) (re.* (str.to_re "a")))) (str.in_re x (re.* (str.to_re "a"))))))
(check-sat)
