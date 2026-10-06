; proof: (bvuge x y) = (bvule y x) at width 4
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvuge x y) (bvule y x))))
(check-sat)
