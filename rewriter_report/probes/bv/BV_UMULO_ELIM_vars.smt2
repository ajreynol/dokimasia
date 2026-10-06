; bvumulo on variables with an independent spec; exercises UmuloEliminate (BV_UMULO_ELIM) if cvc5 eliminates it.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const a (_ BitVec 4))
(declare-const b (_ BitVec 4))
(assert (not (= (bvumulo a b) (not (= ((_ extract 7 4) (bvmul ((_ zero_extend 4) a) ((_ zero_extend 4) b))) #x0)))))
(check-sat)
