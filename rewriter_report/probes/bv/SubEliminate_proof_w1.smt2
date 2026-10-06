; proof: (bvsub x y) = (bvadd x (bvneg y)) at width 1
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(declare-const y (_ BitVec 1))
(assert (not (= (bvsub x y) (bvadd x (bvneg y)))))
(check-sat)
