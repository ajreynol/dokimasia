; proof+differential: rotate_left by 7,4294967295 at width 5 vs independently computed concat
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 5))
(assert (or (not (= ((_ rotate_left 7) x) (concat ((_ extract 2 0) x) ((_ extract 4 3) x)))) (not (= ((_ rotate_left 4294967295) x) x))))
(check-sat)
