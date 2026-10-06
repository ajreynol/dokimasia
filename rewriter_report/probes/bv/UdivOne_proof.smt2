; Proof probe: (bvudiv x 1) -> x; in practice UdivPow2 (power 0) fires first, UdivOne is shadowed.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 3))
(declare-const y (_ BitVec 1))
(assert (or (not (= (bvudiv x #b001) x)) (not (= (bvudiv y #b1) y))))
(check-sat)
