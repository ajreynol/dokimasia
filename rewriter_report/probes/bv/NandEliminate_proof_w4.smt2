; proof: (bvnand x y) = (bvnot (bvand x y)) at width 4
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvnand x y) (bvnot (bvand x y)))))
(check-sat)
