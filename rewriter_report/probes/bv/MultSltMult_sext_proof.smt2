; Proof probe: sound sext/sext form, add on the left in both child orders (bv-mult-slt-mult-1 via MACRO_BV_MULT_SLT_MULT).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const a (_ BitVec 2))
(declare-const x (_ BitVec 2))
(declare-const t (_ BitVec 2))
(assert (not (= (bvslt (bvmul ((_ sign_extend 2) (bvadd x t)) ((_ sign_extend 2) a))
                       (bvmul ((_ sign_extend 2) x) ((_ sign_extend 2) a)))
                (and (not (= t #b00)) (not (= a #b00)) (= (bvslt (bvadd x t) x) (bvsgt a #b00))))))
(check-sat)
