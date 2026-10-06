; proof+differential: (bvsmulo x y) vs an independent BV spec at width 3
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 3))
(declare-const y (_ BitVec 3))
(assert (not (= (bvsmulo x y) (not (= (bvmul ((_ sign_extend 3) x) ((_ sign_extend 3) y)) ((_ sign_extend 3) ((_ extract 2 0) (bvmul ((_ sign_extend 3) x) ((_ sign_extend 3) y)))))))))
(check-sat)
