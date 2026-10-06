; BvIteConstCond: (bvite #b1 x y) -> x
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvite #b1 x y) x)))
(check-sat)
