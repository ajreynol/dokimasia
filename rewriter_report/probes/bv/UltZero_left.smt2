; UltZero: (bvult 0 x) -> (distinct 0 x)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvult #x0 x) (not (= x #x0)))))
(check-sat)
