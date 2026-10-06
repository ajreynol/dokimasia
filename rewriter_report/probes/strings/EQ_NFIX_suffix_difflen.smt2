; x++abc = y++bd: suffix clash with different const lengths
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= (str.++ x "abc") (str.++ y "bd")) false)))
(check-sat)
