; UltOnes: (bvult x ones) -> (distinct x ones)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvult x #xF) (not (= x #xF)))))
(check-sat)
