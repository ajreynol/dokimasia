; proof of to_code constant folding at max code point
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(assert (= x "\u{2ffff}"))
(assert (not (= (str.to_code x) 196607)))
(check-sat)
