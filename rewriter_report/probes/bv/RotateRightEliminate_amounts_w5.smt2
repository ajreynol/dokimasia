; proof+differential: rotate_right by 7,4294967295 at width 5 vs independently computed concat
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 5))
(assert (or (not (= ((_ rotate_right 7) x) (concat ((_ extract 1 0) x) ((_ extract 4 2) x)))) (not (= ((_ rotate_right 4294967295) x) x))))
(check-sat)
