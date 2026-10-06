; UltOne: (bvult x 1) -> (= x 0)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvult x #x1) (= x #x0))))
(check-sat)
