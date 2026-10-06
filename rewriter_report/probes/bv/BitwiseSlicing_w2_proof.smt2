; BitwiseSlicing edge: width 2, constants #b01 and #b10 for and/or
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 2))
(assert (or (not (= (bvand x #b01) (concat #b0 ((_ extract 0 0) x)))) (not (= (bvor x #b10) (concat #b1 ((_ extract 0 0) x))))))
(check-sat)
