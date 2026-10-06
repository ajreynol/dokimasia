; differential: sdiv/srem/smod at INT_MIN,-1,0 with symbolic x at width 1
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(assert (or (not (= (bvsdiv #b1 #b1) #b1)) (not (= (bvsrem #b1 #b1) (_ bv0 1))) (not (= (bvsmod #b1 #b1) (_ bv0 1)))
  (not (= (bvsdiv x (_ bv0 1)) (ite (bvslt x (_ bv0 1)) (_ bv1 1) #b1)))
  (not (= (bvsrem x (_ bv0 1)) x)) (not (= (bvsmod x (_ bv0 1)) x))))
(check-sat)
