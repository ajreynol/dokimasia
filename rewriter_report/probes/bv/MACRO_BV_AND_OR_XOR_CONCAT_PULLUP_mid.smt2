; AndOrXorConcatPullUp with the constant in the middle of a 4-child concat (elaborator groups it for bv-and-concat-pullup3).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 10))
(declare-const y (_ BitVec 2))
(declare-const z (_ BitVec 2))
(declare-const w (_ BitVec 3))
(assert (not (= (bvand x (concat y z #b000 w))
                (concat (bvand ((_ extract 9 6) x) (concat y z)) #b000 (bvand ((_ extract 2 0) x) w)))))
(check-sat)
