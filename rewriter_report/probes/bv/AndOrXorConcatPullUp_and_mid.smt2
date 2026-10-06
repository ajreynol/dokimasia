; AndOrXorConcatPullUp (and): one constant in middle (macro + pullup3)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 8))
(declare-const a (_ BitVec 2))
(declare-const b (_ BitVec 2))
(declare-const y (_ BitVec 8))
(assert (not (= (bvand x (concat a #x1 b)) (concat (bvand ((_ extract 7 6) x) a) (bvand ((_ extract 5 2) x) #x1) (bvand ((_ extract 1 0) x) b)))))
(check-sat)
