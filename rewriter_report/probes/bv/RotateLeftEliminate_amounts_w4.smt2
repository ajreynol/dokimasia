; proof+differential: rotate_left by 0,1,3,4,6,9 at width 4 vs independently computed concat
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (or (not (= ((_ rotate_left 0) x) x)) (not (= ((_ rotate_left 1) x) (concat ((_ extract 2 0) x) ((_ extract 3 3) x)))) (not (= ((_ rotate_left 3) x) (concat ((_ extract 0 0) x) ((_ extract 3 1) x)))) (not (= ((_ rotate_left 4) x) x)) (not (= ((_ rotate_left 6) x) (concat ((_ extract 1 0) x) ((_ extract 3 2) x)))) (not (= ((_ rotate_left 9) x) (concat ((_ extract 2 0) x) ((_ extract 3 3) x))))))
(check-sat)
