; proof: (bvnand x y) = (bvnot (bvand x y)) at width 1
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(declare-const y (_ BitVec 1))
(assert (not (= (bvnand x y) (bvnot (bvand x y)))))
(check-sat)
