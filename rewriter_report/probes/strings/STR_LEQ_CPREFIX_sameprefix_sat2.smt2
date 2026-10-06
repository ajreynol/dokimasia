; equal common prefix, other polarity
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(assert (not (str.<= (str.++ "ab" x) "abc")))
(check-sat)
