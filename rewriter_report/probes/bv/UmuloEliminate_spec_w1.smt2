; proof+differential: (bvumulo x y) vs an independent BV spec at width 1
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(declare-const y (_ BitVec 1))
(assert (not (= (bvumulo x y) (not (= ((_ extract 1 1) (bvmul ((_ zero_extend 1) x) ((_ zero_extend 1) y))) (_ bv0 1))))))
(check-sat)
