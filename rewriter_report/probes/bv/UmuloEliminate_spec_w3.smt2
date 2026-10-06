; proof+differential: (bvumulo x y) vs an independent BV spec at width 3
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 3))
(declare-const y (_ BitVec 3))
(assert (not (= (bvumulo x y) (not (= ((_ extract 5 3) (bvmul ((_ zero_extend 3) x) ((_ zero_extend 3) y))) (_ bv0 3))))))
(check-sat)
