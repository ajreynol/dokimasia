; UltZero: (bvult x 0) -> false
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvult x #x0) false)))
(check-sat)
