; NegIdemp: width 1 --b -> b
; EXPECT: unsat
(set-logic QF_BV)
(declare-const b (_ BitVec 1))
(assert (not (= (bvneg (bvneg b)) b)))
(check-sat)
