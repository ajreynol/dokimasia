; ("" | a | bc)* ---> (a | bc)*
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.* (re.union (str.to_re "") (str.to_re "a") (str.to_re "bc")))) (str.in_re x (re.* (re.union (str.to_re "a") (str.to_re "bc")))))))
(check-sat)
