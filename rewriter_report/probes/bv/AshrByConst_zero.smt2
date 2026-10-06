; AshrByConst: shift by 0 -> x
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvashr x #x0) x)))
(check-sat)
