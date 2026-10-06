; str.to_int over concat with a non-digit constant component is -1
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)(declare-const y String)
(assert (not (= (str.to_int (str.++ x "1a" y)) (- 1))))
(check-sat)
