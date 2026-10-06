; inter (comp R1) R2 with R1 includes R2 ---> re.none
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.inter (re.comp (re.* (re.union (str.to_re "a") (str.to_re "b")))) (re.* (str.to_re "a")))) (str.in_re x re.none))))
(check-sat)
