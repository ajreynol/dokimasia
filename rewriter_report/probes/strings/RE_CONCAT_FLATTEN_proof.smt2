; nested re.++ and str.to_re "" flattening
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.++ (re.++ (str.to_re "a") (re.* (str.to_re "b"))) (str.to_re "") (re.* (str.to_re "a")))) (str.in_re x (re.++ (str.to_re "a") (re.* (str.to_re "b")) (re.* (str.to_re "a")))))))
(check-sat)
