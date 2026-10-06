; BvIteConstChildren: (bvite c #b0 #b1) -> (bvnot c)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const c (_ BitVec 1))
(assert (not (= (bvite c #b0 #b1) (bvnot c))))
(check-sat)
