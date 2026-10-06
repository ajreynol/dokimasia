; proof+differential: (bvumulo x y) vs an independent BV spec at width 5
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 5))
(declare-const y (_ BitVec 5))
(assert (not (= (bvumulo x y) (not (= ((_ extract 9 5) (bvmul ((_ zero_extend 5) x) ((_ zero_extend 5) y))) (_ bv0 5))))))
(check-sat)
