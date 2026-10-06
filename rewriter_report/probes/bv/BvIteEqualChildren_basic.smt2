; BvIteEqualChildren: (bvite c x x) -> x
; EXPECT: unsat
(set-logic QF_BV)
(declare-const c (_ BitVec 1))
(declare-const x (_ BitVec 4))
(assert (not (= (bvite c x x) x)))
(check-sat)
