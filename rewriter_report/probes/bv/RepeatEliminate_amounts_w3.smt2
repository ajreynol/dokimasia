; proof: repeat 1,2,3 at width 3 (BV_REPEAT_ELIM)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 3))
(assert (or (not (= ((_ repeat 1) x) x)) (not (= ((_ repeat 2) x) (concat x x))) (not (= ((_ repeat 3) x) (concat x x x)))))
(check-sat)
