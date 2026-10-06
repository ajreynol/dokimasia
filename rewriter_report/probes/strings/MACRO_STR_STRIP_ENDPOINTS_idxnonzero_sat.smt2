; indexof with nonzero start: stripping end is still fine, but start nonzero must not strip front
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (= (str.indexof (str.++ "ab" x) (str.++ "b" y) 1) 1)))
(assert (= x ""))
(assert (= y ""))
(check-sat)
