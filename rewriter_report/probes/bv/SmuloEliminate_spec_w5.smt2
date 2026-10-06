; proof+differential: (bvsmulo x y) vs an independent BV spec at width 5
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 5))
(declare-const y (_ BitVec 5))
(assert (not (= (bvsmulo x y) (not (= (bvmul ((_ sign_extend 5) x) ((_ sign_extend 5) y)) ((_ sign_extend 5) ((_ extract 4 0) (bvmul ((_ sign_extend 5) x) ((_ sign_extend 5) y)))))))))
(check-sat)
