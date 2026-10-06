; BvIteConstCond: (bvite #b0 x y) -> y
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvite #b0 x y) y)))
(check-sat)
