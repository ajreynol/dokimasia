; BitwiseSlicing of (bvand x #b0110) into concat of slices.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvand x #b0110) (concat #b0 ((_ extract 2 1) x) #b0))))
(check-sat)
