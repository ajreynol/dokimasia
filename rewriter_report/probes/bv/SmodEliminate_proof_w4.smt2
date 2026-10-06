; proof: bvsmod elimination at width 4 (bv-smod-eliminate)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvsmod x y) (ite (= (bvurem (ite (= ((_ extract 3 3) x) #b0) x (bvneg x)) (ite (= ((_ extract 3 3) y) #b0) y (bvneg y))) (_ bv0 4)) (bvurem (ite (= ((_ extract 3 3) x) #b0) x (bvneg x)) (ite (= ((_ extract 3 3) y) #b0) y (bvneg y))) (ite (and (= ((_ extract 3 3) x) #b0) (= ((_ extract 3 3) y) #b0)) (bvurem (ite (= ((_ extract 3 3) x) #b0) x (bvneg x)) (ite (= ((_ extract 3 3) y) #b0) y (bvneg y))) (ite (and (= ((_ extract 3 3) x) #b1) (= ((_ extract 3 3) y) #b0)) (bvadd (bvneg (bvurem (ite (= ((_ extract 3 3) x) #b0) x (bvneg x)) (ite (= ((_ extract 3 3) y) #b0) y (bvneg y)))) y) (ite (and (= ((_ extract 3 3) x) #b0) (= ((_ extract 3 3) y) #b1)) (bvadd (bvurem (ite (= ((_ extract 3 3) x) #b0) x (bvneg x)) (ite (= ((_ extract 3 3) y) #b0) y (bvneg y))) y) (bvneg (bvurem (ite (= ((_ extract 3 3) x) #b0) x (bvneg x)) (ite (= ((_ extract 3 3) y) #b0) y (bvneg y)))))))))))
(check-sat)
