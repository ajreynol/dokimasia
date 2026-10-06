; MultDistribConst: (x+y)*c and (-x)*c distributed (BV_POLY_NORM)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (or (not (= (bvmul (bvadd x y) #b0011) (bvadd (bvmul x #b0011) (bvmul y #b0011)))) (not (= (bvmul (bvneg (bvadd x y)) #b0011) (bvadd (bvmul x #b1101) (bvmul y #b1101))))))
(check-sat)
