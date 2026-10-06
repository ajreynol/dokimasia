; NegMult: applies() tests node[0].isConst() on a bvneg, so never fires; -(x*3) stays (differential only)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (not (= (bvneg (bvmul x #b0011)) (bvmul x #b1101))))
(check-sat)
