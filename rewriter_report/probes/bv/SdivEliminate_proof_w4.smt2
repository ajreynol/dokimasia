; proof: bvsdiv elimination at width 4 (bv-sdiv-eliminate)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvsdiv x y) (ite (xor (= ((_ extract 3 3) x) #b1) (= ((_ extract 3 3) y) #b1)) (bvneg (bvudiv (ite (= ((_ extract 3 3) x) #b1) (bvneg x) x) (ite (= ((_ extract 3 3) y) #b1) (bvneg y) y))) (bvudiv (ite (= ((_ extract 3 3) x) #b1) (bvneg x) x) (ite (= ((_ extract 3 3) y) #b1) (bvneg y) y))))))
(check-sat)
