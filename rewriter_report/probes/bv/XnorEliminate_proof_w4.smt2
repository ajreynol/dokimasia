; proof: (bvxnor x y) = (bvnot (bvxor x y)) at width 4
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvxnor x y) (bvnot (bvxor x y)))))
(check-sat)
