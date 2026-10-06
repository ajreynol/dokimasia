; equal common prefix must NOT be decided (ab++x vs abc)
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(assert (str.<= (str.++ "ab" x) "abc"))
(assert (not (= x "")))
(check-sat)
