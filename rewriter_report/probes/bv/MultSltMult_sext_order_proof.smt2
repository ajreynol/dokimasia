; Proof probe: sound sext/sext form with (bvadd t x) and swapped mult operands on both sides (bv-mult-slt-mult-1 after elaborator swaps).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const a (_ BitVec 2))
(declare-const x (_ BitVec 2))
(declare-const t (_ BitVec 2))
(assert (not (= (bvslt (bvmul ((_ sign_extend 2) a) ((_ sign_extend 2) (bvadd t x)))
                       (bvmul ((_ sign_extend 2) a) ((_ sign_extend 2) x)))
                (and (not (= t #b00)) (not (= a #b00)) (= (bvslt (bvadd t x) x) (bvsgt a #b00))))))
(check-sat)
