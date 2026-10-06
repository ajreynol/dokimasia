; constant prefixes of unequal length with differing common part
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)(declare-const y String)
(assert (not (str.<= (str.++ "abd" x) (str.++ "ac" y))))
(check-sat)
