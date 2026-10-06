; Proof probe: zext(m,x) <u c with c high bits 0 -> x <u c[n-1:0], both sides (ZeroExtendUltConst / bv-zero-extend-ult-const-1/2).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 3))
(assert (or (not (= (bvult ((_ zero_extend 2) x) #b00101) (bvult x #b101)))
            (not (= (bvult #b00110 ((_ zero_extend 2) x)) (bvult #b110 x)))))
(check-sat)
