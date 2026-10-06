; XorSimplify: x cancels, y and (bvnot y) give ones, one constant; whole term is a constant #b1001.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvxor x y #b0110 x (bvnot y)) #b1001)))
(check-sat)
