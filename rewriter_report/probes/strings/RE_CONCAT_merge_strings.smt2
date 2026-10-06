; consecutive str.to_re merge, incl. non-constant string y
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.++ (str.to_re "a") (str.to_re y) (str.to_re "b") (re.* (str.to_re "a")))) (str.in_re x (re.++ (str.to_re (str.++ "a" y "b")) (re.* (str.to_re "a")))))))
(check-sat)
