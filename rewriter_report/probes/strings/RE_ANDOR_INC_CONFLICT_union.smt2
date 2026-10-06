; union R1 (comp R2) with R1 includes R2 ---> _*
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.union (re.* (re.union (str.to_re "a") (str.to_re "b"))) (re.comp (re.* (str.to_re "a"))))) (str.in_re x (re.* re.allchar)))))
(check-sat)
