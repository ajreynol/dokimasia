; proof: (bvxnor x y) = (bvnot (bvxor x y)) at width 1
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(declare-const y (_ BitVec 1))
(assert (not (= (bvxnor x y) (bvnot (bvxor x y)))))
(check-sat)
