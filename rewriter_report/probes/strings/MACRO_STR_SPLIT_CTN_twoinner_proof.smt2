; contains split on inner constant with no overlap (4 components)
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (= (str.contains (str.++ x "a" y "d" z) "bc") (or (str.contains (str.++ x "a" y) "bc") (str.contains z "bc")))))
(check-sat)
