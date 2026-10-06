; proof: repeat 1,2,5 at width 1 (BV_REPEAT_ELIM)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(assert (or (not (= ((_ repeat 1) x) x)) (not (= ((_ repeat 2) x) (concat x x))) (not (= ((_ repeat 5) x) (concat x x x x x)))))
(check-sat)
