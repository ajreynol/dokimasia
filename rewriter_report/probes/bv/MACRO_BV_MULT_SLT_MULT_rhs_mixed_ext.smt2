; Variant of #13039: left is zext(x+t)*sext(a) (correct), right swaps which operand is zero-extended: zext(a)*sext(x).
; EXPECT: sat
(set-logic QF_BV)
(declare-const x (_ BitVec 2))
(declare-const t (_ BitVec 2))
(declare-const a (_ BitVec 2))
(assert (distinct (bvslt (bvmul ((_ zero_extend 2) (bvadd x t)) ((_ sign_extend 2) a))
                         (bvmul ((_ zero_extend 2) a) ((_ sign_extend 2) x)))
                  (and (not (= t #b00)) (not (= a #b00))
                       (= (bvult (bvadd x t) x) (bvsgt a #b00)))))
(check-sat)
