; Differential edges: c high bits nonzero (rule must not fire) and width-1 x, zext by 1.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(declare-const y (_ BitVec 3))
(assert (or (not (bvult ((_ zero_extend 2) y) #b01000))
            (bvult #b01000 ((_ zero_extend 2) y))
            (not (= (bvult ((_ zero_extend 1) x) #b01) (= x #b0)))
            (not (= (bvult #b00 ((_ zero_extend 1) x)) (= x #b1)))))
(check-sat)
