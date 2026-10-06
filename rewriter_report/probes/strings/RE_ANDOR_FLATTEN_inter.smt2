; inter flattening, dedup, drop _*
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.inter (re.inter (re.* (str.to_re "a")) (re.* (re.union (str.to_re "a") (str.to_re "b")))) (re.* re.allchar) (re.* (str.to_re "a")))) (str.in_re x (re.inter (re.* (str.to_re "a")) (re.* (re.union (str.to_re "a") (str.to_re "b"))))))))
(check-sat)
