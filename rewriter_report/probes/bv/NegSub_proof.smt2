; NegSub: -(x - y) -> y - x, pre-rewrite (BV_POLY_NORM)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (not (= (bvneg (bvsub x y)) (bvsub y x))))
(check-sat)
