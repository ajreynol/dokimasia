; MultSimplify: constants multiplied, negations pulled out (BV_POLY_NORM)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (or (not (= (bvmul (bvneg x) #b0011 y #b0101) (bvmul x y #b0001))) (not (= (bvmul x #b0100 #b0100) #b0000)) (not (= (bvmul (bvneg x) y) (bvneg (bvmul x y))))))
(check-sat)
