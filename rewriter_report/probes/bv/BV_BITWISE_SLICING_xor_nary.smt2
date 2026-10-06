; BitwiseSlicing of an n-ary bvxor with constant #b1100 and two variables.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvxor x #b1100 y) (concat (bvnot ((_ extract 3 2) (bvxor x y))) ((_ extract 1 0) (bvxor x y))))))
(check-sat)
