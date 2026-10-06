; is_digit elimination
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(assert (not (= (str.is_digit x) (and (<= 48 (str.to_code x)) (<= (str.to_code x) 57)))))
(check-sat)
