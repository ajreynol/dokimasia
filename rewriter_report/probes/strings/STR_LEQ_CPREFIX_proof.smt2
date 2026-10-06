; differing constant prefixes decide str.<=
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)(declare-const y String)
(assert (or (not (str.<= (str.++ "ab" x) (str.++ "ac" y))) (str.<= (str.++ "b" x) (str.++ "ab" y))))
(check-sat)
