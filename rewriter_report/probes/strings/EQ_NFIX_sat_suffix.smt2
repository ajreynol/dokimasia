; sat: x++ba = y++a satisfiable
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (= (str.++ x "ba") (str.++ y "a")))
(assert (= x ""))
(check-sat)
