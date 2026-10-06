; bvsmulo on variables with an independent spec; exercises SmuloEliminate (BV_SMULO_ELIM) if cvc5 eliminates it.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const a (_ BitVec 4))
(declare-const b (_ BitVec 4))
(define-fun p () (_ BitVec 8) (bvmul ((_ sign_extend 4) a) ((_ sign_extend 4) b)))
(assert (not (= (bvsmulo a b) (not (= p ((_ sign_extend 4) ((_ extract 3 0) p)))))))
(check-sat)
