; XorSimplify: three copies of x, two copies of (bvnot y), one constant; = (bvxor x #b0011).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvxor x (bvnot y) x #b0011 (bvnot y) x) (bvxor x #b0011))))
(check-sat)
