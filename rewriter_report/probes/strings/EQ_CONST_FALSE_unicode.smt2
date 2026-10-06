; distinct constants incl. \u escapes are disequal; \u{61} equals a
; EXPECT: unsat
(set-logic QF_SLIA)
(assert (not (= "\u{61}b" "ab")))
(check-sat)
