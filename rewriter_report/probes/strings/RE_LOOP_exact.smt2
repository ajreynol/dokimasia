; ((_ re.loop 2 2) (a|b)) ---> (a|b)(a|b)
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x ((_ re.loop 2 2) (re.union (str.to_re "a") (str.to_re "b")))) (str.in_re x (re.++ (re.union (str.to_re "a") (str.to_re "b")) (re.union (str.to_re "a") (str.to_re "b")))))))
(check-sat)
