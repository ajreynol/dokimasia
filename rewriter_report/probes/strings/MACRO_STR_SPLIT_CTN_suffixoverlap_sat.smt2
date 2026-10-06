; inner const ab overlaps pattern bc at boundary: must not split
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (str.contains (str.++ x "ab" y) "bc"))
(assert (not (str.contains x "bc")))
(assert (not (str.contains y "bc")))
(check-sat)
