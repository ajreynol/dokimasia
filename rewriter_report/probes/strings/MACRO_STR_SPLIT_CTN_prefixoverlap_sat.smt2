; inner const ca vs pattern bc (pattern suffix c = const prefix): must not split
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (str.contains (str.++ x "ca" y) "bc"))
(assert (not (str.contains x "bc")))
(assert (not (str.contains y "bc")))
(check-sat)
