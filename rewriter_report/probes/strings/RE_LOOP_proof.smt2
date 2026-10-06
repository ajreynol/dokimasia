; ((_ re.loop 1 3) ab) ---> ab ++ (""|ab)... expansion
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x ((_ re.loop 1 3) (str.to_re "ab"))) (str.in_re x (re.union (str.to_re "ab") (str.to_re "abab") (str.to_re "ababab"))))))
(check-sat)
