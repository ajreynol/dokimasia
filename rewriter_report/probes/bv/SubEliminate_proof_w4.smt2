; proof: (bvsub x y) = (bvadd x (bvneg y)) at width 4
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvsub x y) (bvadd x (bvneg y)))))
(check-sat)
