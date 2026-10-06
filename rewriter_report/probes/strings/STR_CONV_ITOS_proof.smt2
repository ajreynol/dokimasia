; to_upper(from_int n) = from_int n
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const n Int)
(assert (not (= (str.to_upper (str.from_int n)) (str.from_int n))))
(check-sat)
