; ExtractSignExtend case low<n<=high (bv-extract-sign-extend-2)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (not (= ((_ extract 5 2) ((_ sign_extend 3) x)) ((_ sign_extend 2) ((_ extract 3 2) x)))))
(check-sat)
