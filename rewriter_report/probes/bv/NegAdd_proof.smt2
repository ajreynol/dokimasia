; NegAdd: -(x+y+z) -> -x + -y + -z (BV_POLY_NORM)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (not (= (bvneg (bvadd x y z)) (bvadd (bvneg x) (bvneg y) (bvneg z)))))
(check-sat)
