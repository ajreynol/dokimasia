; to_lower distributes over concat
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)(declare-const y String)(declare-const z String)
(assert (not (= (str.to_lower (str.++ x y z)) (str.++ (str.to_lower x) (str.to_lower y) (str.to_lower z)))))
(check-sat)
