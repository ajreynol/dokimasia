; proof+differential: bvredand = (ite (= x ones) #b1 #b0) at width 4
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvredand x) (ite (= x #b1111) #b1 #b0))))
(check-sat)
