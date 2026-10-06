; XorSimplify: two complement pairs, no constant, non-constant result (z ^ #b0000)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (not (= (bvxor x y z (bvnot y) (bvnot x)) z)))
(check-sat)
