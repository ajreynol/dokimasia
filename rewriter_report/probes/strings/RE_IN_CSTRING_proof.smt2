; x in str.to_re y iff x = y
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (str.in_re x (str.to_re y)) (= x y))))
(check-sat)
