; proof+differential: bvredor = (ite (= x 0) #b0 #b1) at width 4
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvredor x) (ite (= x (_ bv0 4)) #b0 #b1))))
(check-sat)
