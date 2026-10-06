; ((_ re.loop 0 0) a) ---> ""
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x ((_ re.loop 0 0) (str.to_re "a"))) (str.in_re x (str.to_re "")))))
(check-sat)
