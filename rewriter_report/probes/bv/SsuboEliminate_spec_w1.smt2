; proof+differential: (bvssubo x y) vs an independent BV spec at width 1
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(declare-const y (_ BitVec 1))
(assert (not (= (bvssubo x y) (not (= (bvsub ((_ sign_extend 1) x) ((_ sign_extend 1) y)) ((_ sign_extend 1) ((_ extract 0 0) (bvsub ((_ sign_extend 1) x) ((_ sign_extend 1) y)))))))))
(check-sat)
