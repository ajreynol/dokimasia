; Proof probe: sound mixed form with sext(a) first and zext'd (bvadd t x) second on the left, zext(x) first on the right.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const a (_ BitVec 2))
(declare-const x (_ BitVec 2))
(declare-const t (_ BitVec 2))
(assert (not (= (bvslt (bvmul ((_ sign_extend 2) a) ((_ zero_extend 2) (bvadd t x)))
                       (bvmul ((_ zero_extend 2) x) ((_ sign_extend 2) a)))
                (and (not (= t #b00)) (not (= a #b00)) (= (bvult (bvadd t x) x) (bvsgt a #b00))))))
(check-sat)
