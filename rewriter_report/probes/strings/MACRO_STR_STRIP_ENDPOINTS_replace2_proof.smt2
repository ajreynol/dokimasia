; replace strips non-matching const prefix a
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (= (str.replace (str.++ "ab" x) (str.++ "b" y) z) (str.++ "a" (str.replace (str.++ "b" x) (str.++ "b" y) z)))))
(check-sat)
