; AndOrXorConcatPullUp for bvxor with an all-ones constant in the middle.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 8))
(declare-const y (_ BitVec 3))
(declare-const z (_ BitVec 3))
(assert (not (= (bvxor x (concat y #b11 z))
                (concat (bvxor ((_ extract 7 5) x) y) (bvnot ((_ extract 4 3) x)) (bvxor ((_ extract 2 0) x) z)))))
(check-sat)
