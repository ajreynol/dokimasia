; proof: bvsmod elimination at width 1 (bv-smod-eliminate)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(declare-const y (_ BitVec 1))
(assert (not (= (bvsmod x y) (ite (= (bvurem (ite (= ((_ extract 0 0) x) #b0) x (bvneg x)) (ite (= ((_ extract 0 0) y) #b0) y (bvneg y))) (_ bv0 1)) (bvurem (ite (= ((_ extract 0 0) x) #b0) x (bvneg x)) (ite (= ((_ extract 0 0) y) #b0) y (bvneg y))) (ite (and (= ((_ extract 0 0) x) #b0) (= ((_ extract 0 0) y) #b0)) (bvurem (ite (= ((_ extract 0 0) x) #b0) x (bvneg x)) (ite (= ((_ extract 0 0) y) #b0) y (bvneg y))) (ite (and (= ((_ extract 0 0) x) #b1) (= ((_ extract 0 0) y) #b0)) (bvadd (bvneg (bvurem (ite (= ((_ extract 0 0) x) #b0) x (bvneg x)) (ite (= ((_ extract 0 0) y) #b0) y (bvneg y)))) y) (ite (and (= ((_ extract 0 0) x) #b0) (= ((_ extract 0 0) y) #b1)) (bvadd (bvurem (ite (= ((_ extract 0 0) x) #b0) x (bvneg x)) (ite (= ((_ extract 0 0) y) #b0) y (bvneg y))) y) (bvneg (bvurem (ite (= ((_ extract 0 0) x) #b0) x (bvneg x)) (ite (= ((_ extract 0 0) y) #b0) y (bvneg y)))))))))))
(check-sat)
