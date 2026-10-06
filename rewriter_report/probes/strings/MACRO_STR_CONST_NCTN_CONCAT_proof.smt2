; contains("abc", b++x++a) ---> false (generalized regex b.*a not in abc)
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (= (str.contains "abc" (str.++ "b" x "a")) false)))
(check-sat)
