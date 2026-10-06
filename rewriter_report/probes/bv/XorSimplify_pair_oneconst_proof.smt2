; XorSimplify: complement pair y,~y with exactly one constant and non-constant result (elaboration returns false: consts<=1 and rhs not const)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (not (= (bvxor x y z (bvnot y) #b0101) (bvxor x z #b1010))))
(check-sat)
