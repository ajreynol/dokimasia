; proof+differential: (bvsaddo x y) vs an independent BV spec at width 4
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvsaddo x y) (not (= (bvadd ((_ sign_extend 1) x) ((_ sign_extend 1) y)) ((_ sign_extend 1) ((_ extract 3 0) (bvadd ((_ sign_extend 1) x) ((_ sign_extend 1) y)))))))))
(check-sat)
