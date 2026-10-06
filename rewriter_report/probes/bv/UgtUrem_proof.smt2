; Proof probe: (bvugt (bvurem T x) x) -> (and (= x 0) (bvugt T 0)) (UgtUrem / bv-ugt-urem).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const t (_ BitVec 4))
(declare-const x (_ BitVec 4))
(assert (not (= (bvugt (bvurem t x) x) (and (= x #b0000) (bvugt t #b0000)))))
(check-sat)
