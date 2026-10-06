; BitwiseSlicing on bvand with mixed constant (BV_BITWISE_SLICING)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (not (= (bvand x y #b0110) (concat #b0 ((_ extract 2 1) (bvand x y)) #b0))))
(check-sat)
