; AndOrXorConcatPullUp (xor): 1-bit constant #b1 in middle
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const a (_ BitVec 2))
(declare-const b (_ BitVec 1))
(assert (not (= (bvxor x (concat a #b1 b)) (concat (bvxor ((_ extract 3 2) x) a) (bvnot ((_ extract 1 1) x)) (bvxor ((_ extract 0 0) x) b)))))
(check-sat)
