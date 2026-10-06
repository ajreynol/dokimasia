; ExtractSignExtend case high<n (bv-extract-sign-extend-1)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (not (= ((_ extract 2 1) ((_ sign_extend 3) x)) ((_ extract 2 1) x))))
(check-sat)
