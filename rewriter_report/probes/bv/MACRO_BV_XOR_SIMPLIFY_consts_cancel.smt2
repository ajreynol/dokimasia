; XorSimplify where constants cancel: (bvxor #b1010 x #b1010 (bvnot y) (bvnot y) y) = (bvxor x y).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvxor #b1010 x #b1010 (bvnot y) (bvnot y) y) (bvxor x y))))
(check-sat)
