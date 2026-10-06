; contains(x++abc++y++z, bc++y) ---> true by component containment
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (= (str.contains (str.++ x "abc" y z) (str.++ "bc" y)) true)))
(check-sat)
