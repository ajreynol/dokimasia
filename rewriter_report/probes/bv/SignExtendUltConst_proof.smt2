; Proof probe: all four branches of SignExtendUltConst (lhs x<c_lo / msb=0; rhs c_lo<x / msb=1), n=3,m=2 (bv-sign-extend-ult-const-1..4).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 3))
(assert (or (not (= (bvult ((_ sign_extend 2) x) #b00011) (bvult x #b011)))
            (not (= (bvult ((_ sign_extend 2) x) #b01000) (= ((_ extract 2 2) x) #b0)))
            (not (= (bvult #b00010 ((_ sign_extend 2) x)) (bvult #b010 x)))
            (not (= (bvult #b01000 ((_ sign_extend 2) x)) (= ((_ extract 2 2) x) #b1)))))
(check-sat)
