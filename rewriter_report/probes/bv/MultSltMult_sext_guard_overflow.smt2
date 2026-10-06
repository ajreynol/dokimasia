; Guard check: sext amount (1) < |a| (3) so the product can overflow; rule must NOT fire and the "rewritten" equation is invalid (sat).
; EXPECT: sat
(set-logic QF_BV)
(declare-const a (_ BitVec 3))
(declare-const x (_ BitVec 2))
(declare-const t (_ BitVec 2))
(assert (not (= (bvslt (bvmul ((_ sign_extend 1) a) ((_ sign_extend 2) (bvadd t x)))
                       (bvmul ((_ sign_extend 1) a) ((_ sign_extend 2) x)))
                (and (not (= t #b00)) (not (= a #b000)) (= (bvslt (bvadd t x) x) (bvsgt a #b000))))))
(check-sat)
