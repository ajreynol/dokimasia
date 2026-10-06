; sat: a++x = ab++y is satisfiable (same-prefix, unequal length), must not be false
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (= (str.++ "a" x) (str.++ "ab" y)))
(check-sat)
