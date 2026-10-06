; Free-variable form of the issue shape (zext a, sext x+t): z3 should find a model; cvc5 rewrites unsoundly.
; EXPECT: sat
(set-logic QF_BV)
(declare-const a (_ BitVec 2))
(declare-const x (_ BitVec 2))
(declare-const t (_ BitVec 2))
(assert (not (= (bvslt (bvmul ((_ zero_extend 2) a) ((_ sign_extend 2) (bvadd x t)))
                       (bvmul ((_ zero_extend 2) a) ((_ sign_extend 2) x)))
                (and (not (= t #b00)) (not (= a #b00)) (= (bvult (bvadd x t) x) (bvsgt a #b00))))))
(check-sat)
