; AshrByConst: width 1, amount 1 -> x (sign repeated once)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const b (_ BitVec 1))
(assert (not (= (bvashr b #b1) b)))
(check-sat)
