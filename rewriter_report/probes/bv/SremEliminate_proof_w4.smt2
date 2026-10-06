; proof: bvsrem elimination at width 4 (bv-srem-eliminate)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvsrem x y) (ite (= ((_ extract 3 3) x) #b1) (bvneg (bvurem (ite (= ((_ extract 3 3) x) #b1) (bvneg x) x) (ite (= ((_ extract 3 3) y) #b1) (bvneg y) y))) (bvurem (ite (= ((_ extract 3 3) x) #b1) (bvneg x) x) (ite (= ((_ extract 3 3) y) #b1) (bvneg y) y))))))
(check-sat)
