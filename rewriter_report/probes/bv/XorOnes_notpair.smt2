; XorOnes (via XorSimplify): (bvxor x (bvnot x) y) -> (bvnot y)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvxor x (bvnot x) y) (bvnot y))))
(check-sat)
