; UltOne: width 1 (bvult b #b1) -> (= b #b0) (1 is also ones)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const b (_ BitVec 1))
(assert (not (= (bvult b #b1) (= b #b0))))
(check-sat)
