; string equality orientation flip is eq-symm
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= (str.++ x y) z) (= z (str.++ x y)))))
(check-sat)
