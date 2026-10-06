; len of \u-escaped constant: \u{10}b\u{2ffff} has length 3
; EXPECT: unsat
(set-logic QF_SLIA)
(assert (not (= (str.len "\u{10}b\u{2ffff}") 3)))
(check-sat)
