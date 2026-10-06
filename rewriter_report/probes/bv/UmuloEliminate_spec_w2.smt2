; proof+differential: (bvumulo x y) vs an independent BV spec at width 2
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 2))
(declare-const y (_ BitVec 2))
(assert (not (= (bvumulo x y) (not (= ((_ extract 3 2) (bvmul ((_ zero_extend 2) x) ((_ zero_extend 2) y))) (_ bv0 2))))))
(check-sat)
