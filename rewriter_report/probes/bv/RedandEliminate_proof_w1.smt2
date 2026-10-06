; proof+differential: bvredand = (ite (= x ones) #b1 #b0) at width 1
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(assert (not (= (bvredand x) (ite (= x #b1) #b1 #b0))))
(check-sat)
