; BvIteConstChildren: (bvite c #b1 #b0) -> c
; EXPECT: unsat
(set-logic QF_BV)
(declare-const c (_ BitVec 1))
(assert (not (= (bvite c #b1 #b0) c)))
(check-sat)
