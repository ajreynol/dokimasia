; sat: contains("aba", ab++x++a)?? needs x such that ab x a in aba: false; and contains("aba", a++x++a) sat
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (str.contains "aba" (str.++ "a" x "a")))
(check-sat)
