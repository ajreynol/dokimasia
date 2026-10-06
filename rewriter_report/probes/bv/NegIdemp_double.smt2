; NegIdemp: --x -> x
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvneg (bvneg x)) x)))
(check-sat)
