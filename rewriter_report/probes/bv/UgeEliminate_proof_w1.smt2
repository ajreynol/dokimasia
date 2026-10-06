; proof: (bvuge x y) = (bvule y x) at width 1
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(declare-const y (_ BitVec 1))
(assert (not (= (bvuge x y) (bvule y x))))
(check-sat)
