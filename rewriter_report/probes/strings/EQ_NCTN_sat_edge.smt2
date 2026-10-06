; sat edge: x++ab = ab is satisfiable (x empty) so must not become false
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (= (str.++ x "ab") "ab"))
(check-sat)
