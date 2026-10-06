; MultDistrib: z*(x+y), operand on either side (BV_POLY_NORM)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (or (not (= (bvmul z (bvadd x y)) (bvadd (bvmul x z) (bvmul y z)))) (not (= (bvmul (bvadd x y) z) (bvadd (bvmul z x) (bvmul z y))))))
(check-sat)
