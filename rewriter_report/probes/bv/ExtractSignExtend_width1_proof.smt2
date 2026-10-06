; ExtractSignExtend edge: width-1 extendee, extract exactly at boundary (low=n-1, high=n) and whole top
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(declare-const y (_ BitVec 1))
(assert (or (not (= ((_ extract 1 0) ((_ sign_extend 2) x)) (concat x x))) (not (= ((_ extract 2 1) ((_ sign_extend 2) x)) (concat x x)))))
(check-sat)
