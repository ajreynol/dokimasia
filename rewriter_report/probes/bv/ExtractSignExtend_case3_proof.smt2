; ExtractSignExtend case low>=n, repeat of sign bit (bv-extract-sign-extend-3)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (not (= ((_ extract 6 5) ((_ sign_extend 3) x)) (concat ((_ extract 3 3) x) ((_ extract 3 3) x)))))
(check-sat)
