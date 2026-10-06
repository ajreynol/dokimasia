; Sound sext/sext form of MultSltMult (bv-mult-slt-mult-1 shape); proof should have no trust.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const t (_ BitVec 4))
(declare-const a (_ BitVec 4))
(assert (not (= (bvslt (bvmul ((_ sign_extend 4) (bvadd x t)) ((_ sign_extend 4) a))
                       (bvmul ((_ sign_extend 4) x) ((_ sign_extend 4) a)))
                (and (not (= t #x0)) (not (= a #x0))
                     (= (bvslt (bvadd x t) x) (bvsgt a #x0))))))
(check-sat)
