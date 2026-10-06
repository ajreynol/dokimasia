; sat: contains(x++ab++y, b++y++a) is not entailed
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (str.contains (str.++ x "ab" y) (str.++ "b" y "a"))))
(check-sat)
