; \u{10000} vs \u{ffff} distinct
; EXPECT: unsat
(set-logic QF_SLIA)
(assert (= "\u{10000}" "\u{ffff}"))
(check-sat)
