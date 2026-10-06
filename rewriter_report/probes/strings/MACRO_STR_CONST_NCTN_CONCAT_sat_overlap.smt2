; sat: contains("abab", ab++x++ab) holds with x empty
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (str.contains "abab" (str.++ "ab" x "ab")))
(check-sat)
