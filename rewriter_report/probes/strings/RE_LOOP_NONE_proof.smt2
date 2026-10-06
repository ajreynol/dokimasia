; ((_ re.loop 3 2) a) ---> re.none
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x ((_ re.loop 3 2) (str.to_re "a"))) (str.in_re x re.none))))
(check-sat)
