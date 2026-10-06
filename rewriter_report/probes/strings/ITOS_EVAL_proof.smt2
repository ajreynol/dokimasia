; proof: str.from_int of a negative constant is empty
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const n Int)
(assert (= n (- 7)))
(assert (not (= (str.from_int n) "")))
(check-sat)
