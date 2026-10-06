; XorSimplify: complement pair with one constant and constant result (issue 12336 corner; fixed in elaborator after binary)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const y (_ BitVec 4))
(assert (not (= (bvxor y (bvnot y) #b0101) #b1010)))
(check-sat)
