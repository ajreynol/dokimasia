; AndOrXorConcatPullUp (xor): concat child between two other children, const in middle; x = (bvxor x y)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 8))
(declare-const y (_ BitVec 8))
(declare-const a (_ BitVec 3))
(declare-const b (_ BitVec 1))
(assert (not (= (bvxor x (concat a #x0 b) y) (concat (bvxor ((_ extract 7 5) x) ((_ extract 7 5) y) a) ((_ extract 4 1) (bvxor x y)) (bvxor ((_ extract 0 0) x) ((_ extract 0 0) y) b)))))
(check-sat)
