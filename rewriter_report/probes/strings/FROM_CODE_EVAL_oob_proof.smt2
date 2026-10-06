; proof: from_code of out-of-range code point is empty
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const n Int)
(assert (= n 196608))
(assert (not (= (str.from_code n) "")))
(check-sat)
