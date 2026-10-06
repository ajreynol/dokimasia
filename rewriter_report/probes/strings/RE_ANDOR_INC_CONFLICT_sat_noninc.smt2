; sat check: R1 does not include R2 so must not be re.none
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.inter (re.comp (re.* (str.to_re "a"))) (re.* (re.union (str.to_re "a") (str.to_re "b"))))) (str.in_re x re.none))))
(check-sat)
