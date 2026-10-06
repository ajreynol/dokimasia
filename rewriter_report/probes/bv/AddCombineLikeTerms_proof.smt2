; AddCombineLikeTerms: x + 3x + y - y + 2 + 5 combined (BV_POLY_NORM)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (not (= (bvadd x (bvmul x #b0011) y (bvneg y) #b0010 #b0101) (bvadd (bvmul x #b0100) #b0111))))
(check-sat)
