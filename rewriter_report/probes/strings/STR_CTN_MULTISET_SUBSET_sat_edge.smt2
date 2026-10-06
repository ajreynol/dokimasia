; sat: contains(ab++x, x++b) can hold (x = "")
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (str.contains (str.++ "ab" x) (str.++ x "b")))
(check-sat)
