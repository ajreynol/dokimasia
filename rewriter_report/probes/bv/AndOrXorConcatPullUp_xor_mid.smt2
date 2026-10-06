; AndOrXorConcatPullUp (xor): one constant in middle (macro + pullup3)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 8))
(declare-const a (_ BitVec 2))
(declare-const b (_ BitVec 2))
(declare-const y (_ BitVec 8))
(assert (not (= (bvxor x (concat a #x1 b)) (concat (bvxor ((_ extract 7 6) x) a) (bvxor ((_ extract 5 2) x) #x1) (bvxor ((_ extract 1 0) x) b)))))
(check-sat)
