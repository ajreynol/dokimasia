; Sound zext form with operands written sext-first on both sides; exercises the elaborator's swap steps.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const t (_ BitVec 4))
(declare-const a (_ BitVec 4))
(assert (not (= (bvslt (bvmul ((_ sign_extend 4) a) ((_ zero_extend 4) (bvadd t x)))
                       (bvmul ((_ sign_extend 4) a) ((_ zero_extend 4) x)))
                (and (not (= t #x0)) (not (= a #x0))
                     (= (bvult (bvadd x t) x) (bvsgt a #x0))))))
(check-sat)
