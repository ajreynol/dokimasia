; ShlByConst: amount = width -> 0
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvshl x #x4) #x0)))
(check-sat)
