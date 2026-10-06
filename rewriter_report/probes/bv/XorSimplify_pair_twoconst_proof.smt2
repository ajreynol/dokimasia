; XorSimplify: complement pair with two constants (elaboration path with const grouping)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvxor #b0011 x y (bvnot y) #b0110) (bvxor x #b1010))))
(check-sat)
