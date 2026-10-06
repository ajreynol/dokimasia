; proof+differential: rotate_left by 0,1,5 at width 1 vs independently computed concat
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(assert (or (not (= ((_ rotate_left 0) x) x)) (not (= ((_ rotate_left 1) x) x)) (not (= ((_ rotate_left 5) x) x))))
(check-sat)
