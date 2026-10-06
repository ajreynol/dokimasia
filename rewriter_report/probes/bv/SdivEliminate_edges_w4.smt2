; differential: sdiv/srem/smod at INT_MIN,-1,0 with symbolic x at width 4
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (or (not (= (bvsdiv #b1000 #b1111) #b1000)) (not (= (bvsrem #b1000 #b1111) (_ bv0 4))) (not (= (bvsmod #b1000 #b1111) (_ bv0 4)))
  (not (= (bvsdiv x (_ bv0 4)) (ite (bvslt x (_ bv0 4)) (_ bv1 4) #b1111)))
  (not (= (bvsrem x (_ bv0 4)) x)) (not (= (bvsmod x (_ bv0 4)) x))))
(check-sat)
