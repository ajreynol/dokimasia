; proof: bvsrem elimination at width 1 (bv-srem-eliminate)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(declare-const y (_ BitVec 1))
(assert (not (= (bvsrem x y) (ite (= ((_ extract 0 0) x) #b1) (bvneg (bvurem (ite (= ((_ extract 0 0) x) #b1) (bvneg x) x) (ite (= ((_ extract 0 0) y) #b1) (bvneg y) y))) (bvurem (ite (= ((_ extract 0 0) x) #b1) (bvneg x) x) (ite (= ((_ extract 0 0) y) #b1) (bvneg y) y))))))
(check-sat)
