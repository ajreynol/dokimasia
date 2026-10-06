; proof+differential: (bvsmulo x y) vs an independent BV spec at width 2
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 2))
(declare-const y (_ BitVec 2))
(assert (not (= (bvsmulo x y) (not (= (bvmul ((_ sign_extend 2) x) ((_ sign_extend 2) y)) ((_ sign_extend 2) ((_ extract 1 0) (bvmul ((_ sign_extend 2) x) ((_ sign_extend 2) y)))))))))
(check-sat)
