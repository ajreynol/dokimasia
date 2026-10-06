; XorSimplify: complement pair y,~y with no constant, non-constant result (x ^ ones)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvxor x y (bvnot y)) (bvnot x))))
(check-sat)
