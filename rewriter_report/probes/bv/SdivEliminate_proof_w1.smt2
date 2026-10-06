; proof: bvsdiv elimination at width 1 (bv-sdiv-eliminate)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(declare-const y (_ BitVec 1))
(assert (not (= (bvsdiv x y) (ite (xor (= ((_ extract 0 0) x) #b1) (= ((_ extract 0 0) y) #b1)) (bvneg (bvudiv (ite (= ((_ extract 0 0) x) #b1) (bvneg x) x) (ite (= ((_ extract 0 0) y) #b1) (bvneg y) y))) (bvudiv (ite (= ((_ extract 0 0) x) #b1) (bvneg x) x) (ite (= ((_ extract 0 0) y) #b1) (bvneg y) y))))))
(check-sat)
