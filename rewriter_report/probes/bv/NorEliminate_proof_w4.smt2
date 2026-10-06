; proof: (bvnor x y) = (bvnot (bvor x y)) at width 4
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvnor x y) (bvnot (bvor x y)))))
(check-sat)
