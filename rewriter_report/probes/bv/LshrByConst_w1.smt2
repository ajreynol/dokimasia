; LshrByConst: width 1, amount 1 -> 0
; EXPECT: unsat
(set-logic QF_BV)
(declare-const b (_ BitVec 1))
(assert (not (= (bvlshr b #b1) #b0)))
(check-sat)
