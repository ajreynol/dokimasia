; x++ab++y = b is false: rhs cannot contain lhs
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= (str.++ x "ab" y) "b") false)))
(check-sat)
