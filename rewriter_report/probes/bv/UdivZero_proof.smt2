; Proof probe: (bvudiv x 0) -> ones (UdivZero / bv-udiv-zero), widths 1 and 3.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 3))
(declare-const y (_ BitVec 1))
(assert (or (not (= (bvudiv x #b000) #b111)) (not (= (bvudiv y #b0) #b1))))
(check-sat)
