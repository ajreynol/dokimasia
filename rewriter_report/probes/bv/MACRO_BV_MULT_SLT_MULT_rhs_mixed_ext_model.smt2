; z3 model of _rhs_mixed_ext fixed (x=t=#b11, a=#b01): LHS is false, the C++ rewrite's RHS is true.
; EXPECT: sat
(set-logic QF_BV)
(declare-const x (_ BitVec 2))
(declare-const t (_ BitVec 2))
(declare-const a (_ BitVec 2))
(assert (and (= x #b11) (= t #b11) (= a #b01)))
(assert (not (bvslt (bvmul ((_ zero_extend 2) (bvadd x t)) ((_ sign_extend 2) a))
                    (bvmul ((_ zero_extend 2) a) ((_ sign_extend 2) x)))))
(assert (and (not (= t #b00)) (not (= a #b00))
             (= (bvult (bvadd x t) x) (bvsgt a #b00))))
(check-sat)
